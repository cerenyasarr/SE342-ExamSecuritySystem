# tests/test_requirements.py
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app import create_app, db
from models import User, Course, Room, Exam, StudentExam, Violation
from flask_jwt_extended import create_access_token


class TestRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup once for the class"""
        cls.app = create_app('development')
        cls.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///test_suite.db',
            JWT_SECRET_KEY='test-secret'
        )
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()
        if os.path.exists('test_suite.db'):
            os.remove('test_suite.db')

    def setUp(self):
        """Reset database before each test"""
        db.drop_all()
        db.create_all()
        self.create_mock_data()
        self.create_tokens()

    def create_mock_data(self):
        # --- Users ---
        self.admin = User(username='admin', password_hash='hash', full_name='Admin User', role='Admin')
        self.proctor = User(username='proctor', password_hash='hash', full_name='Proctor User', role='Proctor')
        self.student = User(
            username='student', password_hash='hash', full_name='Student User',
            role='Student', reference_photo_url='ref.jpg'
        )
        db.session.add_all([self.admin, self.proctor, self.student])

        # --- Room ---
        self.room = Room(name='Room 101', capacity=20)
        db.session.add(self.room)

        # --- Course ---
        self.course = Course(code='CS101', name='Intro to CS', instructor_id=1)
        db.session.add(self.course)
        db.session.commit()  # Commit here to get IDs

        # --- Exam ---
        self.exam = Exam(
            name='Midterm', course_id=self.course.id, room_id=self.room.id,
            start_time='2025-01-01 10:00:00', end_time='2025-01-01 12:00:00', status='Active'
        )
        db.session.add(self.exam)
        db.session.commit()

        # --- StudentExam ---
        self.se = StudentExam(
            student_id=self.student.id, exam_id=self.exam.id,
            seat_number='A1', status='Registered'
        )
        db.session.add(self.se)
        db.session.commit()

    def create_tokens(self):
        """Generate JWT tokens for Admin and Proctor"""
        admin_identity = {'user_id': self.admin.id, 'username': 'admin', 'role': 'Admin'}
        proctor_identity = {'user_id': self.proctor.id, 'username': 'proctor', 'role': 'Proctor'}

        self.admin_token = create_access_token(identity=admin_identity)
        self.proctor_token = create_access_token(identity=proctor_identity)

        self.admin_headers = {'Authorization': f'Bearer {self.admin_token}'}
        self.proctor_headers = {'Authorization': f'Bearer {self.proctor_token}'}

    # --- TC-01: Rol Tabanlı Erişim ---
    def test_tc01_role_based_access(self):
        data = {
            'name': 'Hacker Exam', 
            'start_time': '2025-01-01 10:00:00', 
            'end_time': '2025-01-01 12:00:00',
            'course_id': self.course.id, 
            'room_id': self.room.id
        }
        # Proctor erişemez
        res = self.client.post('/api/exams', json=data, headers=self.proctor_headers)
        self.assertEqual(res.status_code, 403)
        self.assertIn('Access denied', res.json['error'])

        # Admin erişir
        res_admin = self.client.post('/api/exams', json=data, headers=self.admin_headers)
        self.assertEqual(res_admin.status_code, 201)

    # --- TC-02: Geçerli Eşleşme ---
    @patch('services.checkin_service.get_face_service')
    def test_tc02_valid_match(self, mock_get_service):
        mock_service = MagicMock()
        mock_service.verify_face.return_value.is_match = True
        mock_service.verify_face.return_value.confidence = 0.95
        mock_get_service.return_value = mock_service

        data = {
            'student_id': self.student.id,
            'exam_id': self.exam.id,
            'captured_image_path': 'b64',
            'current_seat': 'A1'
        }
        res = self.client.post('/api/student-exams/checkin', json=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('successful', res.json['message'].lower())

    # --- TC-03: Kimlik Uyuşmazlığı ---
    @patch('services.checkin_service.get_face_service')
    def test_tc03_face_mismatch(self, mock_get_service):
        mock_service = MagicMock()
        mock_service.verify_face.return_value.is_match = False
        mock_service.verify_face.return_value.confidence = 0.40
        mock_get_service.return_value = mock_service

        data = {'student_id': self.student.id, 'exam_id': self.exam.id,
                'captured_image_path': 'b64', 'current_seat': 'A1'}
        res = self.client.post('/api/student-exams/checkin', json=data)
        self.assertEqual(res.status_code, 400)

        violation = Violation.query.filter_by(student_exam_id=self.se.id, violation_type='face_mismatch').first()
        self.assertIsNotNone(violation)

    # --- TC-05: Hatalı Koltuk ---
    @patch('services.checkin_service.get_face_service')
    def test_tc05_seat_violation(self, mock_get_service):
        mock_service = MagicMock()
        mock_service.verify_face.return_value.is_match = True
        mock_get_service.return_value = mock_service

        data = {'student_id': self.student.id, 'exam_id': self.exam.id,
                'captured_image_path': 'b64', 'current_seat': 'B5'}
        res = self.client.post('/api/student-exams/checkin', json=data)
        self.assertEqual(res.status_code, 400)

        violation = Violation.query.filter_by(student_exam_id=self.se.id, violation_type='wrong_seat').first()
        self.assertIsNotNone(violation)

    # --- TC-06: Mükerrer Kontrol ---
    def test_tc06_duplicate_checkin(self):
        self.se.status = 'Present'
        db.session.commit()
        data = {'student_id': self.student.id, 'exam_id': self.exam.id,
                'captured_image_path': 'b64', 'current_seat': 'A1'}
        res = self.client.post('/api/student-exams/checkin', json=data)
        self.assertEqual(res.status_code, 400)
        self.assertIn('already checked-in', res.json['message'].lower())

    # --- TC-07: Çoklu Yüz ---
    @patch('services.checkin_service.get_face_service')
    def test_tc07_multi_face(self, mock_get_service):
        mock_service = MagicMock()
        mock_service.verify_face.return_value.is_match = False
        mock_service.verify_face.return_value.message = 'Multiple faces detected'
        mock_get_service.return_value = mock_service

        data = {'student_id': self.student.id, 'exam_id': self.exam.id,
                'captured_image_path': 'b64', 'current_seat': 'A1'}
        res = self.client.post('/api/student-exams/checkin', json=data)
        self.assertEqual(res.status_code, 400)
        violation = Violation.query.filter_by(student_exam_id=self.se.id, violation_type='face_mismatch').first()
        self.assertIsNotNone(violation)

    # --- TC-08: Fotoğraf Zorunluluğu ---
    def test_tc08_missing_image(self):
        data = {'student_id': self.student.id, 'exam_id': self.exam.id,
                'captured_image_path': '', 'current_seat': 'A1'}
        res = self.client.post('/api/student-exams/checkin', json=data)
        self.assertEqual(res.status_code, 400)
        self.assertIn('photo required', res.json['message'].lower())

    # --- TC-09: Manuel İhlal ---
    def test_tc09_manual_violation(self):
        data = {'student_exam_id': self.se.id, 'violation_type': 'talking', 'description': 'Chatting'}
        res = self.client.post('/api/violations', json=data, headers=self.proctor_headers)
        self.assertEqual(res.status_code, 201)

    # --- TC-10: ML Mock ---
    def test_tc10_ml_wrapper_mock(self):
        from services.face_verification import FaceVerificationService
        service = FaceVerificationService()

        with patch.object(service, '_detect_faces') as mock_detect, \
             patch.object(service, '_compare_faces') as mock_compare:
            mock_detect.return_value = (1, MagicMock())
            mock_compare.return_value = 0.95
            res = service.verify_face('data:image...', 'path/to/ref')
            self.assertTrue(res.is_match)

if __name__ == '__main__':
    unittest.main()
