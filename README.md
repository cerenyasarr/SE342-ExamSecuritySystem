# Exam Security System

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

A comprehensive Exam Security System featuring face recognition check-in, automated seating plans, and violation monitoring.

## 🌐 Live Demo

🔗 **[https://se342-examsecuritysystem-4.onrender.com/login.html](https://se342-examsecuritysystem-4.onrender.com/login.html)**

---

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

### Database
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Tools & Documentation
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![UML](https://img.shields.io/badge/UML-FABD14?style=for-the-badge&logo=uml&logoColor=black)
![Jira](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white)

---

## 📁 Directory Structure
- `analysis/` - System requirements and business rules
- `diagrams/` - UML diagrams (Use Case, ERD, Sequence, Activity)
- `database/` - SQL schema and dummy data
- `backend/` - Flask API & Core Logic
- `frontend/` - Static HTML/CSS/JS interface
- `tests/` - Unit tests
- `test-docs/` - Test scenarios

## 🚀 Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
> 🌐 Server runs on `http://localhost:5000`

### Frontend
```bash
cd frontend
python -m http.server 8080
```
> 🌐 Open `http://localhost:8080/login.html`

---

## ✅ Tests

```bash
python -m unittest discover tests/unit
```

---

## 🎬 Demo Scenario

| Step | Actor | Action |
|:----:|:------|:-------|
| 1️⃣ | **Admin** | Logs in and creates exam "SE342 Final" in "Hall A" |
| 2️⃣ | **Student (Alice)** | Approaches the check-in kiosk |
| 3️⃣ | **System** | Captures photo and verifies against database |
| 4️⃣ | **System** | Displays "Success! Seat A1" |
| 5️⃣ | **Proctor** | Monitors dashboard for real-time violations |

---

## 👥 Team Members

| Name | Role | Responsibilities |
|:-----|:-----|:-----------------|
| 👩‍💻 **Ceren Yaşar** | Project Lead / Documentation | Jira project management, Sprint planning, Technical Documentation |
| 👨‍💻 **Mehmet Şenadlı** | Backend / Database Design | Database architecture, Schema design, Data management |
| 👨‍🎨 **Bilal Çifteci** | Frontend & Analyst | UI Design, Prototyping, Creating UML Diagrams |

---

## 📅 Sprint Planning & Epic Roadmap

Development follows **Agile/Scrum methodology** structured into **4 main sprints**, each aligned with a corresponding **JIRA Epic**.

<details>
<summary><b>🔹 Sprint 1: Infrastructure & Analysis (Epic 1)</b></summary>

- **Focus:** System foundation and requirement analysis  
- **Key Tasks:** Defining functional/non-functional requirements, business rules, and core diagrams (Use Case, ERD, Sequence)  
- **Goal:** Initializing the repository with the required project structure
</details>

<details>
<summary><b>🔹 Sprint 2: Core Development & Database (Epic 2)</b></summary>

- **Focus:** Core system implementation and data modeling  
- **Key Tasks:** PostgreSQL schema setup, dummy data import, exam, room, and seating plan modules  
- **Goal:** Enforcing role-based access for Admin and Proctor roles
</details>

<details>
<summary><b>🔹 Sprint 3: Check-in Workflow & ML Integration (Epic 3)</b></summary>

- **Focus:** Check-in process and ML-based identity verification  
- **Key Tasks:** ML service wrapper implementation and automated seating compliance checks  
- **Goal:** Recording check-in results, timestamps, and violation triggers
</details>

<details>
<summary><b>🔹 Sprint 4: Reporting, Testing & Validation (Epic 4)</b></summary>

- **Focus:** System validation and documentation completion  
- **Key Tasks:** Test case creation (functional, negative, edge cases) and unit tests for seating and ML mocks  
- **Goal:** Generating analytical reports for check-ins, mismatches, and violations
</details>

---

<p align="center">
  Made with ❤️ for SE342 Software Engineering Course
</p>
