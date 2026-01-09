# SE342 Exam Security System

A comprehensive Exam Security System featuring face recognition check-in, automated seating plans, and violation monitoring.

## Directory Structure
- `analysis/`: System requirements and business rules.
- `diagrams/`: UML diagrams (Use Case, ERD, Sequence, Activity).
- `database/`: SQL schema and dummy data.
- `backend/`: Source code for the application core (API & Logic).
  - `auth/`: RBAC logic.
  - `checkin/`: Face recognition workflow.
  - `management/`: Exam and room administration.
  - `ml_wrapper/`: Interface for ML models.
  - `violations/`: Reporting logic.
- `frontend/`: Static HTML/CSS/JS interface.
- `test-docs/`: Detailed test scenarios.

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL
- Node.js (if using web frontend)

### Installation
1. Clone the repository.
   ```bash
   git clone https://github.com/your-repo/SE342-ExamSecuritySystem.git
   ```
2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database.
   ```bash
   psql -U postgres -d exam_db -f database/schema.sql
   psql -U postgres -d exam_db -f database/dummy_data.sql
   ```

## Running the Application
To run the main service (example):
```bash
python main.py
```

## Running Tests
To execute unit tests:
```bash
python -m unittest discover tests/unit
```

## Demo Scenario
1. **Admin** creates an exam "SE342 Final" in "Hall A".
2. **Student** (Alice) approaches the kiosk.
3. **System** captures photo, verifies against DB.
4. **System** displays "Success! Seat A1".
5. **Proctor** monitors the dashboard for real-time violations.
