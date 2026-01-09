# Exam Security System

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

A comprehensive Exam Security System featuring face recognition check-in, automated seating plans, and violation monitoring.

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

## 👥 Contributors

<table>
  <tr>
    <td align="center">
      <b>SE342 Team</b>
    </td>
  </tr>
</table>

---

<p align="center">
  Made with ❤️ for SE342 Software Engineering Course
</p>
