# Test Cases and Scenarios

## 1. Authentication & RBAC
| ID | Scenario | Input | Expected Output | Status |
|----|----------|-------|-----------------|--------|
| TC01 | Admin login | Valid credentials | Dashboard with 'Create User' button | |
| TC02 | Student Access Denied | Student tries to delete exam | Access Denied Error | |

## 2. Check-in Process
| ID | Scenario | Input | Expected Output | Status |
|----|----------|-------|-----------------|--------|
| TC03 | Successful Check-in | Valid Student Photo, Correct Time | "Access Granted", Seat Assigned | |
| TC04 | Face Mismatch | Wrong Student | "Verification Failed", Retry Prompt | |
| TC05 | Early Arrival | >30 mins before exam | "Check-in not yet open" | |
| TC06 | Late Arrival | >30 mins after start | "Check-in closed", Refer to Admin | |

## 3. Exam Management
| ID | Scenario | Input | Expected Output | Status |
|----|----------|-------|-----------------|--------|
| TC07 | Create Exam | Valid details | Exam created in DB | |
| TC08 | Room Conflict | Room already booked | Error: "Room Unavailable" | |

## 4. Violation Detection
| ID | Scenario | Input | Expected Output | Status |
|----|----------|-------|-----------------|--------|
| TC09 | Multiple Faces | Second face in frame | Warning: "Multiple people detected" | |
| TC10 | Phone Detection | Phone in hand | Violation Logged: "Unauthorized Object" | |
