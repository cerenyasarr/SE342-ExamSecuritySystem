"""
Check-in Service
Orchestrates the complete check-in workflow including:
- Face verification
- Seating compliance check
- Violation recording
"""

from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

from src.models import db, Student, Exam, ExamEnrollment, Violation, CheckInLog
from src.services.face_verification import get_face_service, VerificationResult


@dataclass
class CheckInResult:
    """Result of check-in process"""
    success: bool
    message: str
    student_name: Optional[str] = None
    seat_label: Optional[str] = None
    face_verified: bool = False
    seat_correct: bool = False
    violations: list = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'message': self.message,
            'student_name': self.student_name,
            'seat_label': self.seat_label,
            'face_verified': self.face_verified,
            'seat_correct': self.seat_correct,
            'violations': self.violations or []
        }


class CheckInService:
    """
    Service for processing student check-ins at exams.
    """
    
    def __init__(self):
        self.face_service = get_face_service()
    
    def process_checkin(
        self,
        student_id: str,
        exam_id: str,
        captured_image_path: Optional[str] = None,
        current_row: Optional[int] = None,
        current_col: Optional[int] = None
    ) -> CheckInResult:
        """Process a student check-in for an exam."""
        violations = []
        
        # Get student
        student = Student.query.get(student_id)
        if not student:
            return CheckInResult(success=False, message="Student not found")
        
        # Get exam
        exam = Exam.query.get(exam_id)
        if not exam:
            return CheckInResult(success=False, message="Exam not found")
        
        # Check exam status
        if exam.status not in ['scheduled', 'active']:
            return CheckInResult(success=False, message=f"Exam is not active (status: {exam.status})")
        
        # Find enrollment
        enrollment = ExamEnrollment.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not enrollment:
            return CheckInResult(success=False, message="Student not registered for this exam")
        
        # Face verification (mock for now)
        face_verified = True
        if captured_image_path and student.reference_image_path:
            verification = self.face_service.verify_face(
                captured_image_path,
                student.reference_image_path
            )
            face_verified = verification.is_match
            
            if not face_verified:
                self._create_violation(
                    enrollment.enrollment_id,
                    'face_mismatch',
                    f"Face verification failed (confidence: {verification.confidence:.2f})"
                )
                violations.append({
                    'type': 'face_mismatch',
                    'description': f"Confidence: {verification.confidence:.2f}"
                })
        
        # Seating check
        seat_correct = True
        if current_row and current_col and enrollment.assigned_row and enrollment.assigned_col:
            seat_correct = (
                current_row == enrollment.assigned_row and
                current_col == enrollment.assigned_col
            )
            
            if not seat_correct:
                self._create_violation(
                    enrollment.enrollment_id,
                    'wrong_seat',
                    f"Student at R{current_row}C{current_col}, should be at R{enrollment.assigned_row}C{enrollment.assigned_col}"
                )
                violations.append({
                    'type': 'wrong_seat',
                    'description': f"At R{current_row}C{current_col}, should be at R{enrollment.assigned_row}C{enrollment.assigned_col}"
                })
        
        # Create check-in log
        log = CheckInLog(
            enrollment_id=enrollment.enrollment_id,
            captured_image_path=captured_image_path,
            confidence_score=1.0 if face_verified else 0.5,
            is_verified=face_verified,
            is_seat_correct=seat_correct
        )
        db.session.add(log)
        
        # Update enrollment status
        if face_verified and seat_correct:
            enrollment.status = 'attended'
        
        db.session.commit()
        
        seat_label = f"R{enrollment.assigned_row}C{enrollment.assigned_col}" if enrollment.assigned_row else None
        success = face_verified and seat_correct
        
        if success:
            message = f"Check-in successful! Seat: {seat_label}"
        elif not face_verified:
            message = "Face verification failed"
        else:
            message = f"Wrong seat! Your seat is {seat_label}"
        
        return CheckInResult(
            success=success,
            message=message,
            student_name=student.full_name,
            seat_label=seat_label,
            face_verified=face_verified,
            seat_correct=seat_correct,
            violations=violations
        )
    
    def _create_violation(self, enrollment_id: str, violation_type: str, description: str) -> Violation:
        """Create and persist a violation record"""
        violation = Violation(
            enrollment_id=enrollment_id,
            violation_type=violation_type,
            description=description
        )
        db.session.add(violation)
        return violation


# Singleton instance
_checkin_service: Optional[CheckInService] = None


def get_checkin_service() -> CheckInService:
    """Get the check-in service instance"""
    global _checkin_service
    if _checkin_service is None:
        _checkin_service = CheckInService()
    return _checkin_service
