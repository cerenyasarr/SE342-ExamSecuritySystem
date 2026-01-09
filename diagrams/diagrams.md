# System Diagrams

## Use Case Diagram

```mermaid
usecaseDiagram
    actor Student
    actor Instructor
    actor Proctor
    actor Admin

    package "Exam Security System" {
        usecase "Login" as UC1
        usecase "View Exam Schedule" as UC2
        usecase "Check-in (Face Rec.)" as UC3
        usecase "Create Exam" as UC4
        usecase "Upload Seating Plan" as UC5
        usecase "Monitor Exam" as UC6
        usecase "Report Violation" as UC7
        usecase "View Reports" as UC8
    }

    Student --> UC1
    Student --> UC2
    Student --> UC3

    Instructor --> UC1
    Instructor --> UC4
    Instructor --> UC5
    Instructor --> UC8

    Proctor --> UC1
    Proctor --> UC3
    Proctor --> UC6
    Proctor --> UC7

    Admin --> UC1
    Admin --> UC8
```

## ER Diagram

```mermaid
erDiagram
    Users {
        int id PK
        string username
        string role "Student, Instructor, Admin"
        string photo_url
    }
    Courses {
        int id PK
        string code
        string name
        int instructor_id FK
    }
    Exams {
        int id PK
        int course_id FK
        datetime start_time
        datetime end_time
        int room_id FK
    }
    Rooms {
        int id PK
        string name
        int capacity
    }
    StudentExams {
        int id PK
        int student_id FK
        int exam_id FK
        string status "Registered, Present, Absent"
        datetime checkin_time
    }
    Violations {
        int id PK
        int student_exam_id FK
        string type
        string evidence_url
        datetime timestamp
    }

    Users ||--o{ Courses : "teaches"
    Users ||--o{ StudentExams : "attends"
    Courses ||--o{ Exams : "has"
    Exams ||--o{ StudentExams : "enrollment"
    Rooms ||--o{ Exams : "hosts"
    StudentExams ||--o{ Violations : "has"
```

## Sequence Diagram (Check-in)

```mermaid
sequenceDiagram
    participant Student
    participant Kiosk as Check-in Kiosk
    participant Backend
    participant ML as ML Wrapper
    participant DB as Database

    Student->>Kiosk: Approaches Camera
    Kiosk->>Kiosk: Capture Photo
    Kiosk->>Backend: POST /checkin (image, student_id)
    Backend->>DB: Get Student Reference Photo
    DB-->>Backend: photo_url
    Backend->>ML: Compare(captured, reference)
    activate ML
    ML-->>Backend: Match Score & Confidence
    deactivate ML
    
    alt Match > Threshold
        Backend->>DB: Update Attendance (Status=Present)
        Backend-->>Kiosk: Success Response
        Kiosk-->>Student: Display "Access Granted"
    else Match < Threshold
        Backend-->>Kiosk: Failure Response
        Kiosk-->>Student: Display "Please see Proctor"
    end
```

## Activity Diagram (Decision Flow)

```mermaid
flowchart TD
    A[Start Check-in] --> B{Face Detected?}
    B -- No --> C[Retry Capture]
    C --> B
    B -- Yes --> D[Send to Server]
    D --> E{Match Identity?}
    E -- Yes --> F{Is Time Valid?}
    F -- Yes --> G[Mark Present]
    G --> H[Show Seat Number]
    H --> I[End]
    
    E -- No --> J[Log Failed Attempt]
    J --> K{Attempts >= 3?}
    K -- Yes --> L[Trigger Alert to Proctor]
    L --> M[Manual Verification]
    M --> I
    K -- No --> C
    
    F -- No --> N[Deny: Wrong Time]
    N --> I
```
