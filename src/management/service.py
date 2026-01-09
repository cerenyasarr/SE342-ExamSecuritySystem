class ExamManagementService:
    def __init__(self, db_connection):
        self.db = db_connection

    def create_exam(self, course_id, name, start_time, end_time, room_id):
        """
        Creates a new exam record in the database.
        """
        # Logic to insert into Exams table
        print(f"Creating exam '{name}' for course {course_id}...")
        pass

    def assign_seating(self, exam_id, student_list):
        """
        Generates and assigns seats to students for an exam.
        """
        # Logic to fetch room layout and assign seats
        print(f"Assigning seats for exam {exam_id}...")
        pass

    def get_exam_details(self, exam_id):
        return {"id": exam_id, "name": "Sample Exam"}
