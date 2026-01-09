import unittest
from src.auth.rbac import RoleBasedAccess
from src.ml_wrapper.client import FaceRecognitionClient

class TestRBAC(unittest.TestCase):
    def setUp(self):
        self.rbac = RoleBasedAccess()

    def test_instructor_permissions(self):
        self.assertTrue(self.rbac.has_permission('Instructor', 'create_exam'))
        self.assertFalse(self.rbac.has_permission('Instructor', 'manage_users'))

    def test_student_permissions(self):
        self.assertTrue(self.rbac.has_permission('Student', 'check_in'))
        self.assertFalse(self.rbac.has_permission('Student', 'create_exam'))

class TestMLWrapper(unittest.TestCase):
    def setUp(self):
        self.ml = FaceRecognitionClient()

    def test_verify_face_mock(self):
        result = self.ml.verify_face("img1", "img2")
        self.assertTrue(result['match'])
        self.assertGreater(result['confidence'], 0.8)

if __name__ == '__main__':
    unittest.main()
