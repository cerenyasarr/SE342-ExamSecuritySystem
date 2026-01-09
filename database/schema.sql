-- 1. ROLES (Bağımsız Tablo)
CREATE TABLE roles (
    role_id VARCHAR(50) PRIMARY KEY, -- 'admin' veya 'proctor' gibi string ID
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. ROOMS (Bağımsız Tablo)
CREATE TABLE rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    total_rows INTEGER,
    total_columns INTEGER
);

-- 3. STUDENTS (Bağımsız Tablo - Öğrenci Giriş Yapmaz, Veridir)
CREATE TABLE students (
    student_id VARCHAR(50) PRIMARY KEY, -- UUID veya Okul Numarası olabilir
    student_number VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    reference_image_path TEXT, -- Dosya yolu uzun olabilir, TEXT uygundur
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. SYSTEM USERS (Roles tablosuna bağımlı)
CREATE TABLE system_users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id VARCHAR(50) REFERENCES roles(role_id) ON DELETE RESTRICT, -- Rol silinirse kullanıcı boşa düşmesin, hata versin
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. EXAMS (Rooms ve SystemUsers tablosuna bağımlı)
CREATE TABLE exams (
    exam_id VARCHAR(50) PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL,
    exam_title VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, active, completed
    room_id VARCHAR(50) REFERENCES rooms(room_id) ON DELETE SET NULL,
    proctor_id VARCHAR(50) REFERENCES system_users(user_id) ON DELETE SET NULL, -- Gözetmen
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. EXAM ENROLLMENTS (Exams ve Students tablolarını bağlayan köprü)
CREATE TABLE exam_enrollments (
    enrollment_id VARCHAR(50) PRIMARY KEY,
    exam_id VARCHAR(50) REFERENCES exams(exam_id) ON DELETE CASCADE, -- Sınav silinirse kayıt da silinsin
    student_id VARCHAR(50) REFERENCES students(student_id) ON DELETE CASCADE, -- Öğrenci silinirse kayıt da silinsin
    assigned_row INTEGER,
    assigned_col INTEGER,
    status VARCHAR(20) DEFAULT 'registered', -- registered, attended, absent
    UNIQUE(exam_id, student_id) -- Bir öğrenci aynı sınava iki kere kayıt olamaz
);

-- 7. CHECK-IN LOGS (ExamEnrollments tablosuna bağımlı)
CREATE TABLE check_in_logs (
    log_id VARCHAR(50) PRIMARY KEY,
    enrollment_id VARCHAR(50) REFERENCES exam_enrollments(enrollment_id) ON DELETE CASCADE,
    captured_image_path TEXT,
    confidence_score FLOAT, -- 0.0 ile 1.0 arası
    is_verified BOOLEAN DEFAULT FALSE,
    is_seat_correct BOOLEAN DEFAULT FALSE,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. VIOLATIONS (ExamEnrollments tablosuna bağımlı)
CREATE TABLE violations (
    violation_id VARCHAR(50) PRIMARY KEY,
    enrollment_id VARCHAR(50) REFERENCES exam_enrollments(enrollment_id) ON DELETE CASCADE,
    violation_type VARCHAR(50), -- 'wrong_seat', 'face_mismatch' vb.
    description TEXT,
    evidence_image_path TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);