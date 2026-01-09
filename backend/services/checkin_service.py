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

from models import db, User, Exam, StudentExam, Violation
from services.face_verification import get_face_service, VerificationResult


@dataclass
class CheckInResult:
    """Result of check-in process"""
    success: bool
    message: str
    student_name: Optional[str] = None
    seat_number: Optional[str] = None
    face_verified: bool = False
    seat_correct: bool = False
    violations: list = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'message': self.message,
            'student_name': self.student_name,
            'seat_number': self.seat_number,
            'face_verified': self.face_verified,
            'seat_correct': self.seat_correct,
            'violations': self.violations or []
        }


class CheckInService:
    """
    Service for processing student check-ins at exams.
    
    Workflow:
    1. Verify student is registered for the exam
    2. Verify face matches reference photo
    3. Verify student is at correct seat
    4. Record any violations
    5. Update attendance status
    """
    
    def __init__(self):
        self.face_service = get_face_service()
    
    def process_checkin(
        self,
        student_id: int,
        exam_id: int,
        captured_image_path: Optional[str] = None,
        current_seat: Optional[str] = None
    ) -> CheckInResult:
        """
        Process a student check-in for an exam.
        
        Args:
            student_id: ID of the student checking in
            exam_id: ID of the exam
            captured_image_path: Path to captured photo (for face verification)
            current_seat: Current seat where student is sitting
            
        Returns:
            CheckInResult with status and any violations
        """
        violations = []
        
        # Step 1: Get student and exam
        student = User.query.get(student_id)
        if not student:
            return CheckInResult(
                success=False,
                message="Student not found"
            )
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return CheckInResult(
                success=False,
                message="Exam not found"
            )
        
        # Step 2: Check exam status
        if exam.status not in ['Scheduled', 'Active']:
            return CheckInResult(
                success=False,
                message=f"Exam is not active (status: {exam.status})"
            )
        
        # Step 3: Find student-exam registration
        student_exam = StudentExam.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not student_exam:
            return CheckInResult(
                success=False,
                message="Student not registered for this exam"
            )
        
        # Step 4: Face Verification
        face_verified = True
        face_confidence = 1.0
        
        if captured_image_path and student.reference_photo_url:
            verification = self.face_service.verify_face(
                captured_image_path,
                student.reference_photo_url
            )
            face_verified = verification.is_match
            face_confidence = verification.confidence
            
            if not face_verified:
                # Create violation for face mismatch
                violation = self._create_violation(
                    student_exam.id,
                    'face_mismatch',
                    f"Face verification failed (confidence: {verification.confidence:.2f})"
                )
                violations.append({
                    'type': 'face_mismatch',
                    'description': f"Confidence: {verification.confidence:.2f}"
                })
        
        # Step 5: Seating Compliance Check
        seat_correct = True
        assigned_seat = student_exam.seat_number
        
        if current_seat and assigned_seat:
            seat_correct = current_seat.upper() == assigned_seat.upper()
            
            if not seat_correct:
                # Create violation for wrong seat
                violation = self._create_violation(
                    student_exam.id,
                    'wrong_seat',
                    f"Student at seat {current_seat}, should be at {assigned_seat}"
                )
                violations.append({
                    'type': 'wrong_seat',
                    'description': f"At {current_seat}, should be at {assigned_seat}"
                })
        
        # Step 6: Update attendance status
        if face_verified and seat_correct:
            student_exam.status = 'Present'
            student_exam.checkin_time = datetime.utcnow()
        elif violations:
            student_exam.status = 'Flagged'
            student_exam.checkin_time = datetime.utcnow()
        
        db.session.commit()
        
        # Determine overall success
        success = face_verified and seat_correct
        
        if success:
            message = f"Check-in successful! Seat: {assigned_seat}"
        elif not face_verified:
            message = "Face verification failed"
        elif not seat_correct:
            message = f"Wrong seat! Your seat is {assigned_seat}"
        else:
            message = "Check-in completed with warnings"
        
        return CheckInResult(
            success=success,
            message=message,
            student_name=student.full_name,
            seat_number=assigned_seat,
            face_verified=face_verified,
            seat_correct=seat_correct,
            violations=violations
        )
    
    def _create_violation(
        self, 
        student_exam_id: int, 
        violation_type: str, 
        description: str
    ) -> Violation:
        """Create and persist a violation record"""
        violation = Violation(
            student_exam_id=student_exam_id,
            violation_type=violation_type,
            description=description,
            status='Pending Review'
        )
        db.session.add(violation)
        return violation
    
    def verify_seat(
        self,
        student_id: int,
        exam_id: int,
        current_seat: str
    ) -> Dict[str, Any]:
        """
        Quick seat verification without full check-in.
        
        Returns:
            Dict with seat_correct, assigned_seat, and message
        """
        student_exam = StudentExam.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not student_exam:
            return {
                'seat_correct': False,
                'assigned_seat': None,
                'message': 'Student not registered for this exam'
            }
        
        assigned = student_exam.seat_number
        is_correct = current_seat.upper() == assigned.upper() if assigned else True
        
        return {
            'seat_correct': is_correct,
            'assigned_seat': assigned,
            'current_seat': current_seat,
            'message': 'Correct seat' if is_correct else f'Wrong seat! Go to {assigned}'
        }


# Singleton instance
_checkin_service: Optional[CheckInService] = None


def get_checkin_service() -> CheckInService:
    """Get the check-in service instance"""
    global _checkin_service
    if _checkin_service is None:
        _checkin_service = CheckInService()
    return _checkin_service
