-- School Management System Database Schema
-- SQLite Database

-- Schools Table
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    established_year INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    last_login TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Staff Table
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_no TEXT UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    id_number TEXT,
    gender TEXT,
    date_of_birth TEXT,
    employment_date TEXT,
    department TEXT,
    position TEXT,
    is_teaching INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_no TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    date_of_birth TEXT,
    birth_cert_no TEXT,
    health_conditions TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    guardian_name TEXT,
    guardian_phone TEXT,
    guardian_relation TEXT,
    previous_school TEXT,
    admission_date TEXT,
    class_id INTEGER,
    stream_id INTEGER,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Classes Table
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    level INTEGER,
    stream_id INTEGER,
    class_teacher_id INTEGER,
    capacity INTEGER DEFAULT 40,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Streams Table
CREATE TABLE IF NOT EXISTS streams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

-- Subjects Table
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE,
    is_core INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1
);

-- Class Subjects Table
CREATE TABLE IF NOT EXISTS class_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    subject_id INTEGER,
    teacher_id INTEGER,
    is_active INTEGER DEFAULT 1
);

-- Academic Terms Table
CREATE TABLE IF NOT EXISTS academic_terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    is_current INTEGER DEFAULT 0
);

-- Grade Schemes Table
CREATE TABLE IF NOT EXISTS grade_schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade TEXT NOT NULL,
    min_score INTEGER,
    max_score INTEGER,
    points INTEGER,
    remarks TEXT
);

-- Exam Results Table
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_id INTEGER,
    subject_id INTEGER,
    exam_id INTEGER,
    score REAL,
    grade TEXT,
    remarks TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Fee Structure Table
CREATE TABLE IF NOT EXISTS fee_structure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    frequency TEXT,
    is_active INTEGER DEFAULT 1
);

-- Fee Payments Table
CREATE TABLE IF NOT EXISTS fee_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    amount REAL NOT NULL,
    payment_date TEXT,
    payment_method TEXT,
    receipt_no TEXT UNIQUE,
    recorded_by INTEGER,
    notes TEXT
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_id INTEGER,
    date TEXT,
    status TEXT,
    remarks TEXT
);

-- Library Books Table
CREATE TABLE IF NOT EXISTS library_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT,
    title TEXT NOT NULL,
    author TEXT,
    publisher TEXT,
    category TEXT,
    copies INTEGER DEFAULT 1,
    available INTEGER DEFAULT 1
);

-- Transport Routes Table
CREATE TABLE IF NOT EXISTS transport_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_name TEXT NOT NULL,
    description TEXT,
    fare REAL
);

-- Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_no TEXT UNIQUE,
    vehicle_type TEXT,
    capacity INTEGER,
    driver_id INTEGER,
    route_id INTEGER
);

-- Insert Default Data
INSERT INTO schools (name, address, phone, email) VALUES ('Demo Academy', '123 Education Lane', '+254 712 345 678', 'info@demoacademy.edu');

INSERT INTO users (username, password_hash, role) VALUES 
    ('Jordan', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'SUPER_ADMIN'),
    ('Teacher', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'CLASS_TEACHER'),
    ('Bursar', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'BURSAR');

-- Default login: Jordan / admin123
-- Password hash is SHA256 of "admin123"

INSERT INTO streams (name, description) VALUES 
    ('North', 'North stream'),
    ('South', 'South stream'),
    ('East', 'East stream'),
    ('West', 'West stream');

INSERT INTO grade_schemes (grade, min_score, max_score, points, remarks) VALUES
    ('A', 80, 100, 12, 'Excellent'),
    ('A-', 75, 79, 11, 'Very Good'),
    ('B+', 70, 74, 10, 'Good'),
    ('B', 65, 69, 9, 'Above Average'),
    ('B-', 60, 64, 8, 'Average'),
    ('C+', 55, 59, 7, 'Pass'),
    ('C', 50, 54, 6, 'Pass'),
    ('C-', 45, 49, 5, 'Pass (Condoned)'),
    ('D+', 40, 44, 4, 'Below Pass'),
    ('D', 35, 39, 3, 'Fail'),
    ('E', 0, 34, 0, 'Fail');

INSERT INTO academic_terms (name, start_date, end_date, is_current) VALUES
    ('Term 1 2024', '2024-01-15', '2024-04-15', 1),
    ('Term 2 2024', '2024-05-05', '2024-08-05', 0),
    ('Term 3 2024', '2024-09-01', '2024-11-30', 0);
