## 2.2 Functional Requirements (FR)

This section defines the core functionalities that the **Exam Security System (ESS)** must provide to support secure and controlled examination operations.

---

### FR1: Authentication & Authorization
The system must support **role-based authentication and authorization**, providing distinct permission levels for **Admin** and **Proctor** roles.

---

### FR2: Exam & Venue Definition
Users with the **Admin** role must be able to create, edit, and manage exam details, including:
- Exam date and time  
- Assigned examination room  
- Associated seating plan  

---

### FR3: Student Roster Management
The system must allow **student roster creation and management** through:
- Manual student data entry  
- Basic roster import functionality (e.g., file-based uploads)

---

### FR4: Dynamic Seating Plans
Admins must be able to define and generate **dynamic seating arrangements** using:
- Row and column structures  
- Explicit seat codes (e.g., A1, B2)

---

### FR5: ML-Based Check-in Workflow
During the student check-in process, the system must:
- Capture or upload a live student photo  
- Perform **ML-based identity verification**  
- Validate seating compliance against the assigned seat  

---

### FR6: Violation Logging
The system must automatically log violations for:
- Seat mismatches  
- Identity verification failures  

Additionally, **Proctors** must be able to:
- Add manual notes  
- Attach optional evidence (e.g., images)

---

### FR7: Analytical Reporting
The system must provide **basic analytical reports**, including:
- Total check-in counts  
- Identity mismatch statistics  
- Logged seating and identity violations  

---

### FR8: Status Recording
Every check-in attempt must be recorded with:
- A result status (**Success**, **Rejected**, or **Violation**)  
- An exact timestamp  

---

### FR9: Violation Detail Management
Each violation record must include:
- A **mandatory violation reason**  
- Optional descriptive notes  
- An optional supporting evidence image  

---

### FR10: ML Service Error Handling
If the ML identity verification service fails to respond:
- The check-in attempt must be flagged for **Manual Review**  
- The technical failure must be logged for audit and troubleshooting purposes  

---

## 2.3 Non-Functional Requirements (NFR)

This section specifies the quality attributes and system constraints required to ensure reliability, security, and operational effectiveness.

---

### NFR1: Data Accuracy
The ML-based identity verification component must provide **consistent, repeatable, and verifiable** identity match decisions.

---

### NFR2: Traceability
All system transactions, including:
- Check-ins  
- Violation logs  
- Administrative edits  

must be **permanently stored** with precise timestamps.

---

### NFR3: Reliability
Critical business rules must be enforced using **database-level constraints**, such as:
- Preventing duplicate check-in records  
- Enforcing referential integrity  

---

### NFR4: Auditability
All system outputs, including:
- Event logs  
- Violation records  
- ML test results  

must be accessible for **post-exam auditing and review**.

---

### NFR5: Performance
The complete check-in workflow, including:
- Image capture or upload  
- ML-based identity verification  

should complete within an **acceptable timeframe** to support high-volume exam entry scenarios.

---

### NFR6: Privacy & Security
Student identity data and images must:
- Be stored using secure storage mechanisms  
- Be accessible **only to authorized roles**  
- Comply with applicable data protection and privacy regulations  