-- Users Table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('Student', 'Instructor', 'Admin', 'Proctor')),
    reference_photo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rooms Table
CREATE TABLE Rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    layout_config JSONB -- Stores grid or coordinates for seating
);

-- Courses Table
CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    instructor_id INT REFERENCES Users(id)
);

-- Exams Table
CREATE TABLE Exams (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES Courses(id),
    room_id INT REFERENCES Rooms(id),
    name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled' -- Scheduled, Active, Completed
);

-- StudentExams (Attendance/Registration)
CREATE TABLE StudentExams (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Users(id),
    exam_id INT REFERENCES Exams(id),
    seat_number VARCHAR(10),
    checkin_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Registered', -- Registered, Present, Absent, Flagged
    UNIQUE(student_id, exam_id)
);

-- Violations Table
CREATE TABLE Violations (
    id SERIAL PRIMARY KEY,
    student_exam_id INT REFERENCES StudentExams(id),
    violation_type VARCHAR(50) NOT NULL,
    description TEXT,
    evidence_url VARCHAR(255),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending Review'
);
