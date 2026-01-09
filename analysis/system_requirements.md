# System Requirements

## Functional Requirements
1. **User Authentication & Authorization**
   - The system must support role-based login (Student, Instructor, Admin).
   - Only authorized personnel can modify seating plans.

2. **Exam Management**
   - Instructors must be able to create exams, assign rooms, and upload student lists.
   - The system must generate a random or specified seating plan.

3. **Check-in Process**
   - The system must verify student identity via face recognition against their registered photo.
   - The system must record the check-in timestamp and status (Success, Failed, Pending).

4. **Violation Detection**
   - The system must detect unauthorized objects (e.g., phones) or person substitution (if continuous monitoring is active).
   - Violations must be logged with a timestamp and visual evidence.

5. **Reporting**
   - The system must generate attendance reports.
   - The system must provide a violation summary for each exam.

## Non-Functional Requirements
1. **Performance**
   - Face recognition verification must complete within 2 seconds.
   - The system should support at least 50 concurrent check-ins.

2. **Security**
   - All personal data (images, student IDs) must be encrypted at rest.
   - Communications must use TLS/SSL.

3. **Reliability**
   - The system must be available 99.9% during scheduled exam periods.

4. **Usability**
   - The interface should be responsive and accessible on tablets/mobile devices for proctors.
