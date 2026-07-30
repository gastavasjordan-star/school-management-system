"""
School Management System - Database Models
Enterprise-grade SQLAlchemy models for all school entities
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.automap import automap_base

Base = declarative_base()

class School(Base):
    """School configuration and branding"""
    __tablename__ = 'schools'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    phone = Column(String(50))
    email = Column(String(100))
    website = Column(String(200))
    logo_path = Column(String(500))
    stamp_path = Column(String(500))
    principal_signature_path = Column(String(500))
    motto = Column(String(200))
    founded_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AcademicTerm(Base):
    """Academic terms/periods"""
    __tablename__ = 'academic_terms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # e.g., "Term 1 2024"
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)  # Locked when published
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    students = relationship("Student", back_populates="current_term")
    results = relationship("ExamResult", back_populates="term")

class GradeScheme(Base):
    """Custom grading schemes"""
    __tablename__ = 'grade_schemes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    
    # Grade definitions stored as JSON-like string
    # Format: "A:90-100,B:80-89,C:70-79,D:60-69,E:50-59,F:0-49"
    grade_definitions = Column(Text)
    
    grades = relationship("GradeDefinition", back_populates="scheme")

class GradeDefinition(Base):
    """Individual grade definitions"""
    __tablename__ = 'grade_definitions'
    
    id = Column(Integer, primary_key=True)
    scheme_id = Column(Integer, ForeignKey('grade_schemes.id'))
    letter = Column(String(5))
    min_score = Column(Float)
    max_score = Column(Float)
    points = Column(Float)
    description = Column(String(100))
    
    scheme = relationship("GradeScheme", back_populates="grades")

class Stream(Base):
    """School streams (e.g., North, South, Arts, Sciences)"""
    __tablename__ = 'streams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    classes = relationship("Class", back_populates="stream")

class Class(Base):
    """School classes (e.g., Primary 5, Form 3)"""
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # e.g., "Primary 5"
    level = Column(Integer)  # Numeric level for ordering
    stream_id = Column(Integer, ForeignKey('streams.id'))
    class_teacher_id = Column(Integer, ForeignKey('staff.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    stream = relationship("Stream", back_populates="classes")
    class_teacher = relationship("Staff", foreign_keys=[class_teacher_id])
    students = relationship("Student", back_populates="class_obj")
    subjects = relationship("ClassSubject", back_populates="class_obj")

class Subject(Base):
    """Subjects offered by the school"""
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20))
    is_compulsory = Column(Boolean, default=False)
    category = Column(String(50))  # Science, Arts, Humanities, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    class_subjects = relationship("ClassSubject", back_populates="subject")
    teacher_assignments = relationship("SubjectTeacher", back_populates="subject")

class ClassSubject(Base):
    """Association between classes and subjects"""
    __tablename__ = 'class_subjects'
    
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    is_active = Column(Boolean, default=True)
    
    class_obj = relationship("Class", back_populates="subjects")
    subject = relationship("Subject", back_populates="class_subjects")
    results = relationship("ExamResult", back_populates="class_subject")

class Staff(Base):
    """Staff members (teachers, admin, etc.)"""
    __tablename__ = 'staff'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(50))
    id_number = Column(String(50))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    address = Column(Text)
    photo_path = Column(String(500))
    employment_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Role - will be in User table, but useful for quick reference
    role = Column(String(50))  # SUPER_ADMIN, ADMIN, DOS, CLASS_TEACHER, SUBJECT_TEACHER, BURSAR, SECRETARY
    
    # Relationships
    taught_classes = relationship("Class", foreign_keys="Class.class_teacher_id", overlaps="class_teacher")
    subject_teaching = relationship("SubjectTeacher", back_populates="teacher")
    attendance = relationship("StaffAttendance", back_populates="staff")
    payroll = relationship("Payroll", back_populates="staff")

class SubjectTeacher(Base):
    """Subject-teacher assignments"""
    __tablename__ = 'subject_teachers'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('staff.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    is_active = Column(Boolean, default=True)
    
    teacher = relationship("Staff", back_populates="subject_teaching")
    class_obj = relationship("Class")
    subject = relationship("Subject", back_populates="teacher_assignments")

class Student(Base):
    """Student records"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), unique=True, nullable=False)  # e.g., SCH/2026/001
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    place_of_birth = Column(String(100))
    nationality = Column(String(50))
    religion = Column(String(50))
    photo_path = Column(String(500))
    admission_date = Column(Date)
    status = Column(String(20), default='active')  # active, suspended, expelled, graduated, transferred
    medical_conditions = Column(Text)
    allergies = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Current enrollment
    class_id = Column(Integer, ForeignKey('classes.id'))
    current_term_id = Column(Integer, ForeignKey('academic_terms.id'))
    
    # Relationships
    class_obj = relationship("Class", back_populates="students")
    current_term = relationship("AcademicTerm", back_populates="students")
    parent_info = relationship("Parent", back_populates="student", uselist=False)
    results = relationship("ExamResult", back_populates="student")
    attendance = relationship("StudentAttendance", back_populates="student")
    fee_records = relationship("FeePayment", back_populates="student")
    disciplinary = relationship("DisciplinaryRecord", back_populates="student")
    medical = relationship("MedicalRecord", back_populates="student")
    library = relationship("LibraryRecord", back_populates="student")

class Parent(Base):
    """Parent/Guardian information"""
    __tablename__ = 'parents'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    relationship_type = Column(String(50))  # Father, Mother, Guardian
    primary_phone = Column(String(50), nullable=False)  # Used for login
    secondary_phone = Column(String(50))
    email = Column(String(100))
    occupation = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="parent_info")

class User(Base):
    """System users with role-based access"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # SUPER_ADMIN, ADMIN, DOS, CLASS_TEACHER, SUBJECT_TEACHER, BURSAR, SECRETARY
    staff_id = Column(Integer, ForeignKey('staff.id'))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    staff = relationship("Staff")

class ExamResult(Base):
    """Student exam results"""
    __tablename__ = 'exam_results'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    class_subject_id = Column(Integer, ForeignKey('class_subjects.id'))
    term_id = Column(Integer, ForeignKey('academic_terms.id'))
    cat_score = Column(Float)  # Continuous Assessment
    exam_score = Column(Float)
    total_score = Column(Float)
    grade = Column(String(5))
    remarks = Column(Text)
    entered_by = Column(Integer, ForeignKey('staff.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("Student", back_populates="results")
    class_subject = relationship("ClassSubject", back_populates="results")
    term = relationship("AcademicTerm", back_populates="results")
    entered_by_staff = relationship("Staff")

class StudentAttendance(Base):
    """Daily student attendance"""
    __tablename__ = 'student_attendance'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # present, absent, late, excused
    remarks = Column(Text)
    marked_by = Column(Integer, ForeignKey('staff.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="attendance")
    marked_by_staff = relationship("Staff")

class StaffAttendance(Base):
    """Staff attendance records"""
    __tablename__ = 'staff_attendance'
    
    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.id'))
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    staff = relationship("Staff", back_populates="attendance")

class Payroll(Base):
    """Staff payroll records"""
    __tablename__ = 'payroll'
    
    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.id'))
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    basic_salary = Column(Float)
    allowances = Column(Float)
    deductions = Column(Float)
    net_salary = Column(Float)
    status = Column(String(20), default='pending')  # pending, approved, paid
    paid_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    staff = relationship("Staff", back_populates="payroll")

class FeeStructure(Base):
    """Fee structure definitions"""
    __tablename__ = 'fee_structures'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)  # e.g., "Tuition Fee Term 1"
    description = Column(Text)
    amount = Column(Float, nullable=False)
    due_date = Column(Date)
    is_recurring = Column(Boolean, default=True)
    applicable_to_all = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    exemptions = relationship("FeeExemption", back_populates="fee_structure")

class FeeExemption(Base):
    """Fee exemptions for specific students"""
    __tablename__ = 'fee_exemptions'
    
    id = Column(Integer, primary_key=True)
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    exempted_amount = Column(Float)
    reason = Column(Text)
    approved_by = Column(Integer, ForeignKey('staff.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    fee_structure = relationship("FeeStructure", back_populates="exemptions")
    student = relationship("Student")

class FeePayment(Base):
    """Fee payment records"""
    __tablename__ = 'fee_payments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50))  # cash, bank, mobile money
    reference = Column(String(100))
    received_by = Column(Integer, ForeignKey('staff.id'))
    receipt_number = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="fee_records")
    received_by_staff = relationship("Staff")

class DisciplinaryRecord(Base):
    """Student disciplinary records"""
    __tablename__ = 'disciplinary_records'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    incident_date = Column(Date, nullable=False)
    incident_type = Column(String(100))
    description = Column(Text)
    action_taken = Column(Text)
    severity = Column(String(20))  # minor, moderate, severe
    recorded_by = Column(Integer, ForeignKey('staff.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="disciplinary")
    recorded_by_staff = relationship("Staff")

class MedicalRecord(Base):
    """Student medical/health records"""
    __tablename__ = 'medical_records'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    record_date = Column(Date, nullable=False)
    record_type = Column(String(100))  # checkup, illness, vaccination, etc.
    description = Column(Text)
    treatment = Column(Text)
    doctor_name = Column(String(100))
    next_appointment = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="medical")

class LibraryRecord(Base):
    """Library book borrowing records"""
    __tablename__ = 'library_records'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    book_title = Column(String(200), nullable=False)
    book_id = Column(String(50))
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date)
    return_date = Column(Date)
    status = Column(String(20), default='borrowed')  # borrowed, returned, overdue
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="library")

class Book(Base):
    """Library book inventory"""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(String(50), unique=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100))
    isbn = Column(String(50))
    publisher = Column(String(100))
    category = Column(String(50))
    quantity = Column(Integer, default=1)
    available = Column(Integer, default=1)
    location = Column(String(100))  # Shelf location
    created_at = Column(DateTime, default=datetime.utcnow)

class Announcement(Base):
    """School announcements"""
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    target_audience = Column(String(50))  # all, parents, students, staff
    is_active = Column(Boolean, default=True)
    valid_from = Column(Date)
    valid_until = Column(Date)
    created_by = Column(Integer, ForeignKey('staff.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    creator = relationship("Staff")

class AuditLog(Base):
    """System audit trail"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    details = Column(Text)
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

class License(Base):
    """Software licensing information with subscription support"""
    __tablename__ = 'licenses'
    
    id = Column(Integer, primary_key=True)
    license_key = Column(String(500), unique=True)
    machine_id = Column(String(255))
    client_name = Column(String(200))
    
    # Subscription tier
    tier = Column(String(50))  # bronze, silver, gold, platinum
    
    # Limits
    max_students = Column(Integer, default=100)
    max_staff = Column(Integer, default=20)
    max_classes = Column(Integer, default=5)
    terms_included = Column(Integer, default=1)
    
    # Expiry and status
    expiry_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    # Feature flags (JSON)
    features = Column(Text)  # JSON: {"student_photos": true, ...}
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    activated_at = Column(DateTime)
    
    # Subscription metadata
    auto_renew = Column(Boolean, default=False)
    billing_email = Column(String(100))
    notes = Column(Text)

class FeatureToggle(Base):
    """Premium feature toggles controlled by Super Admin"""
    __tablename__ = 'feature_toggles'
    
    id = Column(Integer, primary_key=True)
    feature_name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200))
    description = Column(Text)
    is_enabled = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BackupRecord(Base):
    """Backup history records"""
    __tablename__ = 'backup_records'
    
    id = Column(Integer, primary_key=True)
    backup_type = Column(String(50))  # usb, cloud
    file_path = Column(String(500))
    file_size = Column(Integer)
    status = Column(String(20), default='pending')  # pending, completed, failed
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alumni(Base):
    """Alumni records"""
    __tablename__ = 'alumni'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    graduation_year = Column(Integer)
    graduation_class = Column(String(100))
    current_occupation = Column(String(100))
    current_employer = Column(String(200))
    contact_email = Column(String(100))
    contact_phone = Column(String(50))
    address = Column(Text)
    achievements = Column(Text)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student")


def init_database(db_path=None):
    """Initialize database and return engine"""
    if db_path is None:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'school_data.db')
    
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Get a new database session"""
    Session = sessionmaker(bind=engine)
    return Session()
