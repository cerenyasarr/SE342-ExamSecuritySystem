-- Dummy Users
INSERT INTO Users (username, password_hash, full_name, role) VALUES
('admin', 'hash123', 'System Admin', 'Admin'),
('inst1', 'hash123', 'John Doe', 'Instructor'),
('std1', 'hash123', 'Alice Smith', 'Student'),
('std2', 'hash123', 'Bob Jones', 'Student'),
('proc1', 'hash123', 'Jane Guard', 'Proctor');

-- Dummy Rooms
INSERT INTO Rooms (name, capacity) VALUES
('Hall A', 50),
('Lab 101', 30);

-- Dummy Courses
INSERT INTO Courses (code, name, instructor_id) VALUES
('CS101', 'Intro to CS', 2),
('SE342', 'Software Engineering', 2);

-- Dummy Exams
INSERT INTO Exams (course_id, room_id, name, start_time, end_time) VALUES
(1, 1, 'CS101 Midterm', '2023-11-10 10:00:00', '2023-11-10 12:00:00'),
(2, 2, 'SE342 Final', '2024-01-15 14:00:00', '2024-01-15 16:00:00');

-- Dummy Registrations (StudentExams)
INSERT INTO StudentExams (student_id, exam_id, seat_number, status) VALUES
(3, 1, 'A1', 'Present'),
(4, 1, 'A2', 'Absent'),
(3, 2, 'L1', 'Registered');
