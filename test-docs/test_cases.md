# 6. Testing & Validation

## 6.1 Test Strategy and Objectives
The testing phase evaluates the system’s ability to handle exam-day workflows and ensures all business rules are enforced. The primary focus is on validating the check-in process, identity verification via the ML wrapper, and seating compliance logic.

## 6.2 Test Cases and Procedures

### TC-01: Role-Based Access Control (Functional)
- **Status:** ✅ Completed
- **Description:** Admin role validation added to the `create_exam` function in `exam_routes.py`. Proctors are denied access with 403 Forbidden.
- **Precondition:** User is logged in with a “Proctor” account.
- **Procedure:** Attempt to access the Admin-only exam creation page.
- **Input:** Proctor credentials and Admin URL.
- **Expected Result:** Access is denied, and the system enforces role permissions.

### TC-02: Valid Identity Match (Functional)
- **Status:** ✅ Completed
- **Description:** Identity verification is performed using OpenCV-based histogram matching (SSIM/Correlation) with a threshold score greater than 60%.
- **Precondition:** Student is registered in the roster.
- **Procedure:** Capture a live photo for verification during check-in.
- **Input:** Live face photo matching the registered student.
- **Expected Result:** The ML component returns a “Match” decision, and the check-in is recorded with a timestamp.

### TC-03: Identity Mismatch (Negative)
- **Status:** ✅ Completed
- **Description:** If face matching fails, `CheckInService` automatically creates a `face_mismatch_violation`.
- **Precondition:** Student is registered.
- **Procedure:** Capture a photo of an unauthorized person.
- **Input:** Photo of a different person.
- **Expected Result:** System identifies the mismatch and flags the entry for review.

### TC-04: Seating Compliance (Functional)
- **Status:** ✅ Completed
- **Description:** When the correct seat is entered, check-in succeeds and the student is marked as Present.
- **Precondition:** Student is assigned to a specific seat in the plan.
- **Procedure:** Enter the correct seat code during the check-in workflow.
- **Input:** Correct seat code/coordinates.
- **Expected Result:** System confirms seat compliance and completes the check-in.

### TC-05: Incorrect Seat Entry (Negative)
- **Status:** ✅ Completed
- **Description:** If an incorrect seat is entered, a `wrong_seat` violation is created and the system issues a warning.
- **Precondition:** Student is assigned to a specific seat.
- **Procedure:** Enter an incorrect seat code during check-in.
- **Input:** Mismatched seat code.
- **Expected Result:** System triggers a seating violation and logs the result.

### TC-06: Duplicate Check-in Prevention (Edge Case)
- **Status:** ✅ Completed
- **Description:** `checkin_service.py` was updated to prevent students with status Present or Flagged from checking in again.
- **Precondition:** Student has already completed a successful check-in.
- **Procedure:** Attempt to check in the same student ID a second time.
- **Input:** Already processed student ID.
- **Expected Result:** System blocks the duplicate entry based on business rules.

# backend/services/checkin_service.py
if student_exam.status in ['Present', 'Flagged']:
    return CheckInResult(False, "Student has already checked in")
    
### TC-07: Multiple Faces Detection (Edge Case)
- **Status:** ✅ Completed
- **Description:** `face_verification.py` was updated to reject check-in attempts if more than one face is detected in the frame.
- **Precondition:** Camera/upload interface is active.
- **Procedure:** Provide a photo containing more than one face.
- **Input:** Image with multiple faces.
- **Expected Result:** The system rejects the image and prompts for a valid single-face photo.

# backend/services/face_verification.py
if count_cap > 1:
    return VerificationResult(False, 0.0, "Multiple faces detected!")

### TC-08: Missing Image Validation (Negative)
- **Status:** ✅ Completed
- **Description:** The system rejects the operation if no photo is submitted and returns “Photo is required”.
- **Precondition:** Check-in form is open.
- **Procedure:** Submit the check-in form without capturing or uploading a photo.
- **Input:** Null image input.
- **Expected Result:** System prevents submission and displays a “Photo Required” error.

# backend/services/checkin_service.py
if not captured_image_path:
    return CheckInResult(False, "Photo is required")

### TC-09: Manual Violation Logging (Functional)
- **Status:** ✅ Completed
- **Description:** The `/api/violations` endpoint and the frontend Report Violation interface are active.
- **Precondition:** Proctor identifies an incident during the exam.
- **Procedure:** Open the violation log and enter the reason and notes.
- **Input:** Violation reason and proctor notes.
- **Expected Result:** The record is saved in the database for reporting.

### TC-10: ML Service Wrapper Mocking (Unit Test)
- **Status:** ⚠️ Partially Completed
- **Description:** A unit test was written in `tests/test_requirements.py`. However, the test environment currently throws a configuration error. The business logic is fully implemented.
- **Precondition:** Unit testing environment is active.
- **Procedure:** Test the integration logic using mock inputs instead of the actual ML model.
- **Input:** Mocked “No Match” signal to the service wrapper.
- **Expected Result:** The wrapper correctly processes the signal and triggers the appropriate system logic.