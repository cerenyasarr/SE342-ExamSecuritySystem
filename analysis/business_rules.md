# Business Rules & Validations

## Business Rules
1. **Exam Eligibility**
   - A student can only check in if they are registered for the specific course and exam.
   - Check-in is allowed from 30 minutes before until 30 minutes after the exam start time.

2. **Seating Rules**
   - Students must check in at their assigned seat or check in at the door and be directed to their seat.
   - If a student is not found in the list, they must be directed to the main supervisor.

3. **Violation Handling**
   - Three consecutive face mismatch alerts during an exam (if monitoring) trigger a manual review by a proctor.
   - Confirmed violations result in an immediate "Flagged" status for the exam attempt.

## Data Validations
1. **Student Data**
   - Student ID must be unique and follow the format `202XXXXX`.
   - Uploaded reference photos must be in JPG/PNG format, < 5MB, and contain exactly one face.

2. **Exam Data**
   - Exam end time must be strictly after the start time.
   - Room capacity cannot be exceeded by the student list size.
