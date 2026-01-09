"""
Database Models for Exam Security System
Compatible with schema.sql
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


class Role(db.Model):
    """Roles table - admin, proctor"""
    __tablename__ = 'roles'
    
    role_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    users = db.relationship('SystemUser', back_populates='role')
    
    def to_dict(self):
        return {
            'role_id': self.role_id,
            'name': self.name
        }


class Room(db.Model):
    """Rooms table"""
    __tablename__ = 'rooms'
    
    room_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    room_name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    total_rows = db.Column(db.Integer)
    total_columns = db.Column(db.Integer)
    
    # Relationships
    exams = db.relationship('Exam', back_populates='room')
    
    def to_dict(self):
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'capacity': self.capacity,
            'total_rows': self.total_rows,
            'total_columns': self.total_columns
        }


class Student(db.Model):
    """Students table - exam takers"""
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    student_number = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    reference_image_path = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('ExamEnrollment', back_populates='student')
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'student_number': self.student_number,
            'full_name': self.full_name,
            'email': self.email,
            'reference_image_path': self.reference_image_path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SystemUser(db.Model):
    """System users table - admins and proctors who log in"""
    __tablename__ = 'system_users'
    
    user_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.String(50), db.ForeignKey('roles.role_id'))
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    role = db.relationship('Role', back_populates='users')
    proctored_exams = db.relationship('Exam', back_populates='proctor')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Exam(db.Model):
    """Exams table"""
    __tablename__ = 'exams'
    
    exam_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    course_code = db.Column(db.String(20), nullable=False)
    exam_title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, active, completed
    room_id = db.Column(db.String(50), db.ForeignKey('rooms.room_id'))
    proctor_id = db.Column(db.String(50), db.ForeignKey('system_users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    room = db.relationship('Room', back_populates='exams')
    proctor = db.relationship('SystemUser', back_populates='proctored_exams')
    enrollments = db.relationship('ExamEnrollment', back_populates='exam')
    
    def to_dict(self):
        return {
            'exam_id': self.exam_id,
            'course_code': self.course_code,
            'exam_title': self.exam_title,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'room_id': self.room_id,
            'room_name': self.room.room_name if self.room else None,
            'proctor_id': self.proctor_id,
            'proctor_name': self.proctor.full_name if self.proctor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ExamEnrollment(db.Model):
    """Exam enrollments - links students to exams"""
    __tablename__ = 'exam_enrollments'
    
    enrollment_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    exam_id = db.Column(db.String(50), db.ForeignKey('exams.exam_id', ondelete='CASCADE'))
    student_id = db.Column(db.String(50), db.ForeignKey('students.student_id', ondelete='CASCADE'))
    assigned_row = db.Column(db.Integer)
    assigned_col = db.Column(db.Integer)
    status = db.Column(db.String(20), default='registered')  # registered, attended, absent
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('exam_id', 'student_id'),)
    
    # Relationships
    exam = db.relationship('Exam', back_populates='enrollments')
    student = db.relationship('Student', back_populates='enrollments')
    check_in_logs = db.relationship('CheckInLog', back_populates='enrollment')
    violations = db.relationship('Violation', back_populates='enrollment')
    
    def to_dict(self):
        return {
            'enrollment_id': self.enrollment_id,
            'exam_id': self.exam_id,
            'exam_title': self.exam.exam_title if self.exam else None,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_number': self.student.student_number if self.student else None,
            'assigned_row': self.assigned_row,
            'assigned_col': self.assigned_col,
            'seat_label': f"R{self.assigned_row}C{self.assigned_col}" if self.assigned_row and self.assigned_col else None,
            'status': self.status
        }


class CheckInLog(db.Model):
    """Check-in logs - records of check-in attempts"""
    __tablename__ = 'check_in_logs'
    
    log_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    enrollment_id = db.Column(db.String(50), db.ForeignKey('exam_enrollments.enrollment_id', ondelete='CASCADE'))
    captured_image_path = db.Column(db.Text)
    confidence_score = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)
    is_seat_correct = db.Column(db.Boolean, default=False)
    attempt_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollment = db.relationship('ExamEnrollment', back_populates='check_in_logs')
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'enrollment_id': self.enrollment_id,
            'captured_image_path': self.captured_image_path,
            'confidence_score': self.confidence_score,
            'is_verified': self.is_verified,
            'is_seat_correct': self.is_seat_correct,
            'attempt_time': self.attempt_time.isoformat() if self.attempt_time else None
        }


class Violation(db.Model):
    """Violations table - recorded violations"""
    __tablename__ = 'violations'
    
    violation_id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    enrollment_id = db.Column(db.String(50), db.ForeignKey('exam_enrollments.enrollment_id', ondelete='CASCADE'))
    violation_type = db.Column(db.String(50))  # wrong_seat, face_mismatch, etc.
    description = db.Column(db.Text)
    evidence_image_path = db.Column(db.Text)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollment = db.relationship('ExamEnrollment', back_populates='violations')
    
    def to_dict(self):
        enrollment = self.enrollment
        student = enrollment.student if enrollment else None
        return {
            'violation_id': self.violation_id,
            'enrollment_id': self.enrollment_id,
            'student_name': student.full_name if student else None,
            'student_number': student.student_number if student else None,
            'violation_type': self.violation_type,
            'description': self.description,
            'evidence_image_path': self.evidence_image_path,
            'reported_at': self.reported_at.isoformat() if self.reported_at else None
        }
