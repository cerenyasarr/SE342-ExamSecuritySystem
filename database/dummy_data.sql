-- ==========================================
-- 1. BAĞIMSIZ VERİLER (INDEPENDENT DATA)
-- ==========================================

-- A) Roles (Technical Codes - English)
INSERT INTO roles (name) VALUES 
('admin'), 
('proctor');

-- B) Rooms (Generic Names - English)
INSERT INTO rooms (room_name, capacity, total_rows, total_columns) VALUES 
('Computer Lab-101', 30, 5, 6),
('Lecture Hall-A', 100, 10, 10);

-- C) Students (Turkish Names - Specific Data)
INSERT INTO students (student_number, full_name, email, reference_image_path) VALUES 
('220706028', 'Mehmet Şenadlı', 'mehmetsenadli44@gmail.com', '/refs/mehmet.jpg'),
('220706059', 'Ceren Yaşar', 'cerenysr1@gmail.com', '/refs/ceren.jpg'),
('220706018', 'Bilal Çifteci', 'ciftecibilal@gmail.com', '/refs/bilal.jpg');

-- ==========================================
-- 2. SYSTEM USERS (Admin & Proctor)
-- ==========================================

-- Not: password_hash alanına şimdilik düz metin yazdık. 
-- Prodüksiyonda burası bcrypt ile hashlenmiş olmalı.
INSERT INTO system_users (username, password_hash, full_name, role_id) VALUES 
('emre_admin', 'emre_admin', 'Sistem Yöneticisi', (SELECT role_id FROM roles WHERE name = 'admin')),
('gozetmen_ahmet', 'gozetmen_ahmet', 'Prof. Ahmet Kadayıfçı', (SELECT role_id FROM roles WHERE name = 'proctor'));

-- ==========================================
-- 3. EXAMS (Sınav Oluşturma)
-- ==========================================

-- Gözetmen Ahmet Hoca tarafından yönetilen CS101 sınavı
INSERT INTO exams (course_code, exam_title, start_time, end_time, status, room_id, proctor_id) VALUES 
('CS101', 'Intro to Algorithms Midterm', NOW(), NOW() + INTERVAL '2 hours', 'active', 
    (SELECT room_id FROM rooms WHERE room_name = 'Computer Lab-101'),
    (SELECT user_id FROM system_users WHERE username = 'gozetmen_ahmet')
);

-- ==========================================
-- 4. EXAM ENROLLMENTS (Kayıtlar)
-- ==========================================

INSERT INTO exam_enrollments (exam_id, student_id, assigned_row, assigned_col, status) VALUES 
-- 1. Mehmet Şenadlı: Sıra 1, Sütun 1
(
    (SELECT exam_id FROM exams WHERE course_code = 'CS101'),
    (SELECT student_id FROM students WHERE student_number = '220706028'),
    1, 1, 'attended'
),
-- 2. Ceren Yaşar: Sıra 1, Sütun 2
(
    (SELECT exam_id FROM exams WHERE course_code = 'CS101'),
    (SELECT student_id FROM students WHERE student_number = '220706059'),
    1, 2, 'attended'
),
-- 3. Bilal Çifteci: Sıra 1, Sütun 3
(
    (SELECT exam_id FROM exams WHERE course_code = 'CS101'),
    (SELECT student_id FROM students WHERE student_number = '220706018'),
    1, 3, 'attended'
);

-- ==========================================
-- 5. LOGS & VIOLATIONS (SENARYOLAR)
-- ==========================================

-- SENARYO 1: MEHMET ŞENADLI (SORUNSUZ)
-- Yüzü eşleşti (%98), Yeri doğru.
INSERT INTO check_in_logs (enrollment_id, captured_image_path, confidence_score, is_verified, is_seat_correct) 
VALUES (
    (SELECT enrollment_id FROM exam_enrollments WHERE student_id = (SELECT student_id FROM students WHERE student_number = '220706028')),
    '/caps/exam1_mehmet_ok.jpg', 0.98, TRUE, TRUE
);

-- SENARYO 2: CEREN YAŞAR (YANLIŞ YER)
-- Yüzü eşleşti (%95), ama atanmış yeri (1,2) yerine başka yere oturdu.
INSERT INTO check_in_logs (enrollment_id, captured_image_path, confidence_score, is_verified, is_seat_correct) 
VALUES (
    (SELECT enrollment_id FROM exam_enrollments WHERE student_id = (SELECT student_id FROM students WHERE student_number = '220706059')),
    '/caps/exam1_ceren_wrong.jpg', 0.95, TRUE, FALSE
);

-- Ceren için İhlal Kaydı
INSERT INTO violations (enrollment_id, violation_type, description, evidence_image_path)
VALUES (
    (SELECT enrollment_id FROM exam_enrollments WHERE student_id = (SELECT student_id FROM students WHERE student_number = '220706059')),
    'wrong_seat', -- Teknik kod (EN)
    'Student detected in wrong seat coordinates.', -- Teknik açıklama (EN)
    '/caps/exam1_ceren_wrong.jpg'
);

-- SENARYO 3: BİLAL ÇİFTECİ (YÜZ EŞLEŞMEDİ / BAŞKASI)
-- Güven skoru düşük (%42), Bilal yerine başkası gelmiş gibi.
INSERT INTO check_in_logs (enrollment_id, captured_image_path, confidence_score, is_verified, is_seat_correct) 
VALUES (
    (SELECT enrollment_id FROM exam_enrollments WHERE student_id = (SELECT student_id FROM students WHERE student_number = '220706018')),
    '/caps/exam1_bilal_fake.jpg', 0.42, FALSE, TRUE
);

-- Bilal için İhlal Kaydı
INSERT INTO violations (enrollment_id, violation_type, description, evidence_image_path)
VALUES (
    (SELECT enrollment_id FROM exam_enrollments WHERE student_id = (SELECT student_id FROM students WHERE student_number = '220706018')),
    'face_mismatch', -- Teknik kod (EN)
    'Face verification failed. Confidence score: 0.42', -- Teknik açıklama (EN)
    '/caps/exam1_bilal_fake.jpg'
);