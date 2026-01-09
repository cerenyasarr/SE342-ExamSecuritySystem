## 5.2 Sprint Planning & Epic Roadmap

Development was structured into **four main sprints**, each aligned with a corresponding **JIRA Epic** to ensure systematic delivery and validation of the Exam Security System.

---

### 5.2.1 Sprint 1: Infrastructure & Analysis (Epic 1)
- **Focus:** System foundation and requirement analysis  
- **Key Tasks:** Defining functional/non-functional requirements, business rules, and core diagrams (Use Case, ERD, Sequence)  
- **Goal:** Initializing the Bitbucket repository with the required project structure  

---

### 5.2.2 Sprint 2: Core Development & Database (Epic 2)
- **Focus:** Core system implementation and data modeling  
- **Key Tasks:** PostgreSQL schema setup, dummy data import, exam, room, and seating plan modules  
- **Goal:** Enforcing role-based access for Admin and Proctor roles  

---

### 5.2.3 Sprint 3: Check-in Workflow & ML Integration (Epic 3)
- **Focus:** Check-in process and ML-based identity verification  
- **Key Tasks:** ML service wrapper implementation and automated seating compliance checks  
- **Goal:** Recording check-in results, timestamps, and violation triggers  

---

### 5.2.4 Sprint 4: Reporting, Testing & Validation (Epic 4)
- **Focus:** System validation and documentation completion  
- **Key Tasks:** Test case creation (functional, negative, edge cases) and unit tests for seating and ML mocks  
- **Goal:** Generating analytical reports for check-ins, mismatches, and violations  