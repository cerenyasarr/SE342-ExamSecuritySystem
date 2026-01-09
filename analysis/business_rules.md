## 2.1 Business Rules & Validations (BRV)

This section defines the logical rules governing the **Exam Security System (ESS)**. These rules ensure data integrity, operational consistency, and system reliability throughout the examination process.

---

### 2.1.1 Identity & Verification Rules (ML Logic)

- **BR1: Identity Match Threshold**  
  The ML-based identity verification service must return a **"Match"** result only if the similarity score between the live captured photo and the student's official ID photo exceeds a predefined threshold.

- **BR2: Single Face Detection**  
  The check-in process must fail if the captured image contains **zero faces or more than one face**, in order to prevent proxy or impersonation-based check-ins.

- **BR3: Manual Review Override**  
  If the ML service produces a **"No Match"** result, the **Proctor** must have the ability to manually review the student’s identity and override the decision.  
  A **mandatory justification note** must be recorded for audit purposes.

---

### 2.1.2 Seating & Compliance Rules

- **BR4: Correct Seat Requirement**  
  A student must be seated in the **exact seat code or coordinate (row/column)** assigned to them in the official Seating Plan.

- **BR5: Automatic Violation Trigger**  
  Any discrepancy between the **assigned seat** and the **entered seat during check-in** must automatically generate a **"Seating Violation"** record.

- **BR6: Duplicate Check-in Prevention**  
  Each student is permitted **only one successful check-in per exam session**.  
  Any subsequent check-in attempts must be **blocked by the system**.

---

### 2.1.3 Role-Based Access Control Rules (RBAC)

- **BR7: Admin Exclusive Rights**  
  Only users assigned the **Admin** role are authorized to:
  - Create exams  
  - Define or modify room layouts  
  - Import or manage student rosters

- **BR8: Proctor Operational Scope**  
  Users with the **Proctor** role are limited to:
  - Performing student check-ins  
  - Logging exam violations  
  - Viewing examination reports  

  Proctors are **not permitted** to delete exam records or modify student information.

---

### 2.1.4 Data Validation Rules (VR)

- **VR1: Duplicate Check-in Prevention**  
  A student must not have more than **one check-in record** for the same exam session.

- **VR2: ML Service Testability**  
  The ML identity verification component must be implemented using a **service wrapper architecture** that supports testing with **mock inputs**.

- **VR3: Mandatory Field Validation**  
  A check-in request must be rejected if:
  - No photo is captured  
  - No seat number is provided

- **VR4: Invalid Seat Code Prevention**  
  The system must reject any check-in attempt that references a **seat code not defined** in the active room seating plan.

- **VR5: Multi-Face or Invalid Image Detection**  
  If **multiple faces** or **no faces** are detected in the captured image, the check-in process must be halted and **flagged for manual proctor review**.

- **VR6: Role-Based Restriction Enforcement**  
  Only **Admin** users are authorized to create exams or seating plans.  
  **Proctors** are strictly limited to check-in operations and reporting functionalities.