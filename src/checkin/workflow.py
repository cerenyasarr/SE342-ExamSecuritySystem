from datetime import datetime

class CheckInWorkflow:
    def __init__(self, ml_wrapper, db):
        self.ml_wrapper = ml_wrapper
        self.db = db

    def process_checkin(self, student_id, exam_id, captured_image):
        """
        Orchestrates the check-in process:
        1. Validate exam time
        2. Verify identity via ML
        3. Record attendance
        """
        # 1. Validation
        if not self._is_checkin_window_open(exam_id):
            return {"status": "error", "message": "Check-in closed"}

        # 2. Face Recognition
        reference_image = self.db.get_reference_photo(student_id)
        match_result = self.ml_wrapper.verify_face(captured_image, reference_image)

        if not match_result['match']:
            return {"status": "failed", "message": "Face verification failed"}

        # 3. Record
        self.db.update_attendance(student_id, exam_id, "Present")
        return {"status": "success", "seat": "A1"}

    def _is_checkin_window_open(self, exam_id):
        # Check current time vs exam start/end window
        return True
