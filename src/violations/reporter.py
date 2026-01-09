class ViolationReporter:
    def __init__(self, db_connection):
        self.db = db_connection

    def log_violation(self, student_exam_id, violation_type, evidence_path):
        """
        Logs a detected violation into the database.
        """
        print(f"Logging violation: {violation_type} for exam instance {student_exam_id}")
        # Insert into Violations table
        pass

    def generate_report(self, exam_id):
        """
        Summarizes violations for a specific exam.
        """
        return [
            {"student_id": 101, "type": "Phone Detected", "time": "10:15"},
            {"student_id": 105, "type": "Absence", "time": "12:00"}
        ]
