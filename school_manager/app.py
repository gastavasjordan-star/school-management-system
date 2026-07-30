"""
School Management System - Main Application Entry Point
Enterprise-grade offline school management with hardware licensing
"""
import os
import sys
import logging
from datetime import datetime

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("School Manager")
    app.setOrganizationName("SchoolManager")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Database setup
    from school_manager.models.database import init_database, get_session, School, AcademicTerm, GradeScheme, User, Staff, Subject, Class, Stream
    from school_manager.utils.auth import AuthManager
    from school_manager.utils.hardware import LicenseManager
    from school_manager.views.main_window import MainWindow, LoginDialog, ActivationScreen
    
    # Initialize database
    db_path = os.path.join(os.path.dirname(__file__), 'school_data.db')
    engine = init_database(db_path)
    session = get_session(engine)
    
    # Initialize managers
    auth_manager = AuthManager(session)
    license_manager = LicenseManager(session)
    
    # Check activation
    if not license_manager.is_activated():
        logger.warning("Software not activated - showing activation screen")
        activation = ActivationScreen(license_manager)
        if activation.exec() != activation.Accepted:
            QApplication.quit()
            return
    
    # Check for demo data
    create_demo_data(session)
    
    # Show login dialog
    login = LoginDialog(auth_manager)
    if login.exec() != login.Accepted:
        QApplication.quit()
        return
    
    # Create and show main window
    logger.info(f"User logged in: {auth_manager.current_user.username}")
    
    main_window = MainWindow(session, auth_manager, license_manager)
    main_window.show()
    
    # Run application
    exit_code = app.exec()
    
    # Cleanup
    session.close()
    logger.info("Application closed")
    
    return exit_code


def create_demo_data(session):
    """Create demo data if database is empty"""
    from school_manager.utils.auth import AuthManager, Role
    from school_manager.models.database import School, AcademicTerm, GradeScheme, User, Staff, Subject, Class, Stream
    
    # Check if data exists
    if session.query(School).count() > 0:
        return
    
    logger.info("Creating demo data...")
    
    # Create school
    school = School(
        name="Greenfield Academy",
        address="123 Education Street, Academic City",
        phone="+254 700 123 456",
        email="info@greenfieldacademy.edu",
        website="www.greenfieldacademy.edu",
        motto="Excellence Through Knowledge"
    )
    session.add(school)
    
    # Create demo Super Admin user
    admin_user, _ = AuthManager(session).create_user(
        username="Jordan",
        password="admin123",
        role=Role.SUPER_ADMIN
    )
    
    # Create admin user
    admin_staff = Staff(
        employee_id="STF001",
        first_name="Admin",
        last_name="User",
        email="admin@school.com",
        phone="+254 700 000 001",
        role=Role.ADMIN
    )
    session.add(admin_staff)
    session.commit()
    
    AuthManager(session).create_user(
        username="admin",
        password="admin123",
        role=Role.ADMIN,
        staff_id=admin_staff.id
    )
    
    # Create streams
    primary = Stream(name="Primary")
    secondary = Stream(name="Secondary")
    session.add_all([primary, secondary])
    session.commit()
    
    # Create classes
    classes_data = [
        ("Grade 1", 1), ("Grade 2", 2), ("Grade 3", 3),
        ("Grade 4", 4), ("Grade 5", 5), ("Grade 6", 6),
        ("Form 1", 7), ("Form 2", 8), ("Form 3", 9), ("Form 4", 10)
    ]
    
    classes = []
    for name, level in classes_data:
        stream = primary if level <= 6 else secondary
        class_obj = Class(name=name, level=level, stream_id=stream.id)
        classes.append(class_obj)
    
    session.add_all(classes)
    session.commit()
    
    # Create subjects
    subjects_data = [
        ("Mathematics", "MATH", True),
        ("English", "ENG", True),
        ("Kiswahili", "KIS", True),
        ("Science", "SCI", True),
        ("Social Studies", "SST", True),
        ("Religious Education", "CRE", False),
        ("Art & Craft", "ART", False),
        ("Physical Education", "PE", False),
        ("Computer Studies", "ICT", False),
        ("Physics", "PHY", False),
        ("Chemistry", "CHEM", False),
        ("Biology", "BIO", False),
        ("History", "HIST", False),
        ("Geography", "GEO", False),
        ("Business Studies", "BUS", False),
    ]
    
    subjects = []
    for name, code, compulsory in subjects_data:
        subject = Subject(name=name, code=code, is_compulsory=compulsory)
        subjects.append(subject)
    
    session.add_all(subjects)
    session.commit()
    
    # Create academic terms
    current_year = datetime.now().year
    terms = [
        AcademicTerm(name=f"Term 1 {current_year}", start_date=datetime(current_year, 1, 10).date(), 
                      end_date=datetime(current_year, 4, 10).date(), is_current=True),
        AcademicTerm(name=f"Term 2 {current_year}", start_date=datetime(current_year, 5, 5).date(),
                      end_date=datetime(current_year, 8, 10).date()),
        AcademicTerm(name=f"Term 3 {current_year}", start_date=datetime(current_year, 9, 1).date(),
                      end_date=datetime(current_year, 11, 30).date()),
    ]
    session.add_all(terms)
    session.commit()
    
    # Create grade scheme
    grade_scheme = GradeScheme(
        name="Standard Grading",
        description="Standard A-F grading scale",
        is_default=True,
        grade_definitions="A:90-100,B:80-89,C:70-79,D:60-69,E:50-59,F:0-49"
    )
    session.add(grade_scheme)
    
    # Create demo students
    student_count = 0
    for class_obj in classes[:3]:  # Create students in first 3 classes
        for i in range(10):
            student_count += 1
            student = Staff(
                employee_id=f"STU{student_count:04d}",
                first_name=f"Student{i+1}",
                last_name=f"Demo",
                role="student"  # This will be moved to Student table in full implementation
            )
            session.add(student)
    
    # Create demo staff
    staff_roles = [
        (Role.DOS, "Director", "Studies"),
        (Role.BURSAR, "Chief", "Bursar"),
        (Role.SECRETARY, "School", "Secretary"),
        (Role.CLASS_TEACHER, "Class", "Teacher"),
        (Role.SUBJECT_TEACHER, "Subject", "Teacher"),
    ]
    
    for idx, (role, first, last) in enumerate(staff_roles):
        staff = Staff(
            employee_id=f"STF{idx+2:03d}",
            first_name=first,
            last_name=last,
            email=f"{first.lower()}@school.com",
            phone=f"+254 700 000 0{idx+2}",
            role=role
        )
        session.add(staff)
        session.flush()
        
        # Create user for staff
        username = f"{first.lower()}{last.lower()}"
        AuthManager(session).create_user(username, "staff123", role, staff_id=staff.id)
    
    session.commit()
    
    # Create default users with various roles
    # Already created Jordan (Super Admin) and Admin
    
    # Create feature toggles
    from school_manager.models.database import FeatureToggle
    
    features = [
        ("photo_processing", "Student Photo Processing", "Upload and manage student photos", True),
        ("pdf_engine", "High-Res PDF Engine", "Generate branded PDF documents", True),
        ("email_letters", "Automated Email Letters", "Send fee demand letters via email", True),
        ("cloud_backup", "Cloud Backup Sync", "Automatically backup data to Google Drive", True),
    ]
    
    for name, display, desc, enabled in features:
        toggle = FeatureToggle(
            feature_name=name,
            display_name=display,
            description=desc,
            is_enabled=enabled,
            is_premium=True
        )
        session.add(toggle)
    
    session.commit()
    
    logger.info("Demo data created successfully")


if __name__ == "__main__":
    # Check for PyQt6
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("PyQt6 is required. Install it with: pip install PyQt6")
        sys.exit(1)
    
    sys.exit(main())
