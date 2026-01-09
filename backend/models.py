from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20))  # Student, Instructor, Admin, Proctor
    reference_photo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses = db.relationship('Course', back_populates='instructor')
    student_exams = db.relationship('StudentExam', back_populates='student')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role,
            'reference_photo_url': self.reference_photo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    layout_config = db.Column(db.JSON)  # JSONB in PostgreSQL
    
    # Relationships
    exams = db.relationship('Exam', back_populates='room')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
            'layout_config': self.layout_config
        }


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    instructor = db.relationship('User', back_populates='courses')
    exams = db.relationship('Exam', back_populates='course')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor.full_name if self.instructor else None
        }


class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Active, Completed
    
    # Relationships
    course = db.relationship('Course', back_populates='exams')
    room = db.relationship('Room', back_populates='exams')
    student_exams = db.relationship('StudentExam', back_populates='exam')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_code': self.course.code if self.course else None,
            'course_name': self.course.name if self.course else None,
            'room_id': self.room_id,
            'room_name': self.room.name if self.room else None,
            'name': self.name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status
        }


class StudentExam(db.Model):
    __tablename__ = 'studentexams'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    seat_number = db.Column(db.String(10))
    checkin_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Registered')  # Registered, Present, Absent, Flagged
    
    # Relationships
    student = db.relationship('User', back_populates='student_exams')
    exam = db.relationship('Exam', back_populates='student_exams')
    violations = db.relationship('Violation', back_populates='student_exam')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'exam_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_number': self.student.username if self.student else None,
            'exam_id': self.exam_id,
            'exam_name': self.exam.name if self.exam else None,
            'seat_number': self.seat_number,
            'checkin_time': self.checkin_time.isoformat() if self.checkin_time else None,
            'status': self.status
        }


class Violation(db.Model):
    __tablename__ = 'violations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_exam_id = db.Column(db.Integer, db.ForeignKey('studentexams.id'))
    violation_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    evidence_url = db.Column(db.String(255))
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending Review')
    
    # Relationships
    student_exam = db.relationship('StudentExam', back_populates='violations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_exam_id': self.student_exam_id,
            'student_name': self.student_exam.student.full_name if self.student_exam and self.student_exam.student else None,
            'violation_type': self.violation_type,
            'description': self.description,
            'evidence_url': self.evidence_url,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
            'status': self.status
        }
