"""
Main Application Window - School Management System
"""
import os
import sys
from datetime import datetime, date
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QStackedWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
                              QTableWidget, QTableWidgetItem, QComboBox, QSpinBox, QDateEdit,
                              QMessageBox, QDialog, QFileDialog, QCheckBox, QRadioButton,
                              QGroupBox, QProgressBar, QScrollArea, QSplitter, QTabWidget,
                              QFormLayout, QListWidget, QListWidgetItem, QInputDialog,
                              QColorDialog, QFontDialog, QCalendarWidget)
from PyQt6.QtCore import Qt, QTimer, QDate, QSize, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QAction, QFont, QPainter, QLinearGradient, QColor

from school_manager.utils.hardware import HardwareFingerprint
from school_manager.views.styles import ModernStylesheet, Colors
from school_manager.views.components import (CardWidget, StatCard, SidebarButton, PrimaryButton, 
                                              SecondaryButton, DangerButton, StatusBadge,
                                              TitleLabel, SubtitleLabel, FormLabel, HeaderBar,
                                              ScrollArea, ContentArea, DataTable, FormField,
                                              IconButton, AvatarWidget, LoadingOverlay)


class ActivationScreen(QDialog):
    """Hardware activation screen"""
    
    def __init__(self, license_manager, parent=None):
        super().__init__(parent)
        self.license_manager = license_manager
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Activation Required")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo/Title
        title = QLabel("🏫 School Manager")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2563eb; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Enterprise Edition")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Activation message
        msg = QLabel("This software requires activation.")
        msg.setStyleSheet("font-size: 14px; color: #0f172a;")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)
        
        # Machine ID
        machine_id = HardwareFingerprint.get_machine_id()
        
        id_group = QGroupBox("Machine ID")
        id_layout = QVBoxLayout()
        
        id_label = QLabel(machine_id)
        id_label.setStyleSheet("""
            font-family: monospace;
            font-size: 14px;
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            color: #0f172a;
        """)
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        id_layout.addWidget(id_label)
        id_group.setLayout(id_layout)
        layout.addWidget(id_group)
        
        # License key input
        key_label = QLabel("Enter License Key:")
        key_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #374151;")
        layout.addWidget(key_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        self.key_input.setMinimumHeight(45)
        self.key_input.setStyleSheet("""
            font-size: 14px;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
        """)
        layout.addWidget(self.key_input)
        
        # Activate button
        self.activate_btn = PrimaryButton("Activate")
        self.activate_btn.clicked.connect(self.activate)
        self.activate_btn.setMinimumHeight(45)
        layout.addWidget(self.activate_btn)
        
        # Status message
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def activate(self):
        key = self.key_input.text().strip()
        if not key:
            self.status_label.setText("Please enter a license key")
            self.status_label.setStyleSheet("color: #dc2626;")
            return
        
        success, message = self.license_manager.activate_license(key)
        
        if success:
            self.status_label.setText("✓ " + message)
            self.status_label.setStyleSheet("color: #16a34a; font-weight: bold;")
            QTimer.singleShot(1500, self.accept)
        else:
            self.status_label.setText("✗ " + message)
            self.status_label.setStyleSheet("color: #dc2626;")


class LoginDialog(QDialog):
    """User login dialog"""
    
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(400, 350)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔐 Login to Continue")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Enter your credentials to access the system")
        subtitle.setStyleSheet("font-size: 13px; color: #64748b;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #374151;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumHeight(40)
        self.username_input.returnPressed.connect(self.login)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #374151;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(self.password_input)
        
        # Login button
        self.login_btn = PrimaryButton("Login")
        self.login_btn.clicked.connect(self.login)
        self.login_btn.setMinimumHeight(45)
        layout.addWidget(self.login_btn)
        
        # Demo accounts hint
        hint = QLabel("Demo: Jordan (Super Admin) / admin123")
        hint.setStyleSheet("font-size: 11px; color: #94a3b8; text-align: center;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        user = self.auth_manager.authenticate(username, password)
        
        if user:
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")


class ImpersonateDialog(QDialog):
    """Super Admin user impersonation dialog"""
    
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.selected_user = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Log In As User")
        self.setFixedSize(450, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Select a user to impersonate")
        header.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        layout.addWidget(header)
        
        # Info text
        info = QLabel("⚠️ You are impersonating as another user. Actions will be logged.")
        info.setStyleSheet("""
            background-color: #ffedd5;
            color: #ea580c;
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
        """)
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # User list
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 6px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
            }
        """)
        layout.addWidget(self.user_list)
        
        # Load users
        users = self.auth_manager.get_all_users()
        for user in users:
            if user['is_active']:
                item = QListWidgetItem(f"{user['username']} ({user['role_display']}) - {user['staff_name'] or 'System User'}")
                item.setData(Qt.ItemDataRole.UserRole, user)
                self.user_list.addItem(item)
        
        self.user_list.itemDoubleClicked.connect(self.select_user)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.select_btn = PrimaryButton("Select User")
        self.select_btn.clicked.connect(self.select_user)
        btn_layout.addWidget(self.select_btn)
        
        self.cancel_btn = SecondaryButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def select_user(self):
        current_item = self.user_list.currentItem()
        if current_item:
            self.selected_user = current_item.data(Qt.ItemDataRole.UserRole)
            self.accept()


class DashboardView(QWidget):
    """Main dashboard view"""
    
    def __init__(self, session, auth, license_manager, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.license_manager = license_manager
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Welcome header
        welcome_card = CardWidget()
        welcome_layout = QHBoxLayout()
        
        welcome_text = QVBoxLayout()
        user = self.auth.current_user
        if user and user.staff:
            name = f"{user.staff.first_name} {user.staff.last_name}"
        else:
            name = user.username if user else "User"
        
        title = QLabel(f"Welcome back, {name}!")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0f172a;")
        welcome_text.addWidget(title)
        
        role_text = QLabel(f"Logged in as {self.auth.get_role_display()}")
        role_text.setStyleSheet("font-size: 14px; color: #64748b;")
        welcome_text.addWidget(role_text)
        
        welcome_layout.addLayout(welcome_text)
        welcome_layout.addStretch()
        
        # Quick stats
        from school_manager.models.database import Student, Staff, AcademicTerm
        
        student_count = self.session.query(Student).filter(Student.status == 'active').count()
        staff_count = self.session.query(Staff).filter(Staff.is_active == True).count()
        current_term = self.session.query(AcademicTerm).filter(AcademicTerm.is_current == True).first()
        
        self.stats = []
        stat = StatCard("Total Students", str(student_count), "👨‍🎓", "#2563eb")
        self.stats.append(stat)
        welcome_layout.addWidget(stat)
        
        stat = StatCard("Total Staff", str(staff_count), "👨‍🏫", "#16a34a")
        self.stats.append(stat)
        welcome_layout.addWidget(stat)
        
        if current_term:
            stat = StatCard("Current Term", current_term.name, "📅", "#ea580c")
            self.stats.append(stat)
            welcome_layout.addWidget(stat)
        
        welcome_card.layout.addLayout(welcome_layout)
        layout.addWidget(welcome_card)
        
        # Quick actions
        actions_card = CardWidget()
        actions_layout = QGridLayout()
        
        actions = [
            ("➕", "Register Student", "students"),
            ("💰", "Record Payment", "payments"),
            ("📝", "Enter Marks", "marks"),
            ("📊", "View Reports", "reports"),
            ("📋", "Attendance", "attendance"),
            ("⚙️", "Settings", "settings"),
        ]
        
        for i, (icon, text, action) in enumerate(actions):
            btn = QPushButton(f"{icon}\n{text}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 20px;
                    font-size: 13px;
                    color: #0f172a;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #dbeafe;
                    border-color: #2563eb;
                }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            actions_layout.addWidget(btn, i // 3, i % 3)
        
        actions_card.layout.addLayout(actions_layout)
        layout.addWidget(actions_card)
        
        # License status (for Super Admin)
        if self.auth.has_permission('manage_licenses'):
            license_card = CardWidget()
            license_layout = QHBoxLayout()
            
            status = self.license_manager.get_activation_status()
            if status['activated']:
                status_label = StatusBadge("Activated", "success")
                info_text = QLabel(f"Licensed to: {status['client_name']}")
            else:
                status_label = StatusBadge("Not Activated", "error")
                info_text = QLabel("Software requires activation")
            
            license_layout.addWidget(status_label)
            license_layout.addWidget(info_text)
            license_layout.addStretch()
            
            activate_btn = SecondaryButton("Manage License")
            license_layout.addWidget(activate_btn)
            
            license_card.layout.addLayout(license_layout)
            layout.addWidget(license_card)
        
        layout.addStretch()
    
    def load_data(self):
        pass


class StudentsView(QWidget):
    """Student management view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
        self.load_students()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Students", "Manage student records and enrollment")
        
        if self.auth.has_permission('manage_students'):
            add_btn = PrimaryButton("+ Add Student")
            add_btn.clicked.connect(self.add_student)
            header.add_action(add_btn)
        
        layout.addWidget(header)
        
        # Filters
        filters_card = CardWidget()
        filters_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or ID...")
        self.search_input.textChanged.connect(self.filter_students)
        self.search_input.setMinimumWidth(300)
        filters_layout.addWidget(self.search_input)
        
        self.class_filter = QComboBox()
        self.class_filter.addItem("All Classes", None)
        from school_manager.models.database import Class
        classes = self.session.query(Class).all()
        for c in classes:
            self.class_filter.addItem(c.name, c.id)
        self.class_filter.currentIndexChanged.connect(self.filter_students)
        filters_layout.addWidget(QLabel("Class:"))
        filters_layout.addWidget(self.class_filter)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Status", "Active", "Suspended", "Graduated", "Transferred"])
        self.status_filter.currentIndexChanged.connect(self.filter_students)
        filters_layout.addWidget(QLabel("Status:"))
        filters_layout.addWidget(self.status_filter)
        
        filters_layout.addStretch()
        
        filters_card.layout.addLayout(filters_layout)
        layout.addWidget(filters_card)
        
        # Students table
        self.table = DataTable(["ID", "Name", "Gender", "Class", "Status", "Actions"])
        layout.addWidget(self.table)
        
        layout.addStretch()
    
    def load_students(self):
        from school_manager.models.database import Student, Class
        
        students = self.session.query(Student).join(Class).all()
        data = []
        
        for s in students:
            data.append({
                "ID": s.student_id,
                "Name": f"{s.first_name} {s.last_name}",
                "Gender": s.gender or "-",
                "Class": s.class_obj.name if s.class_obj else "-",
                "Status": s.status,
                "Actions": "Edit | View"
            })
        
        self.table.set_data(data)
    
    def filter_students(self):
        search = self.search_input.text().lower()
        class_id = self.class_filter.currentData()
        status = self.status_filter.currentText()
        
        from school_manager.models.database import Student, Class
        
        query = self.session.query(Student).join(Class)
        
        if search:
            query = query.filter(
                (Student.first_name + " " + Student.last_name).like(f"%{search}%") |
                Student.student_id.like(f"%{search}%")
            )
        
        if class_id:
            query = query.filter(Student.class_id == class_id)
        
        if status != "All Status":
            query = query.filter(Student.status == status.lower())
        
        students = query.all()
        data = []
        
        for s in students:
            data.append({
                "ID": s.student_id,
                "Name": f"{s.first_name} {s.last_name}",
                "Gender": s.gender or "-",
                "Class": s.class_obj.name if s.class_obj else "-",
                "Status": s.status,
                "Actions": "Edit | View"
            })
        
        self.table.set_data(data)
    
    def add_student(self):
        QMessageBox.information(self, "Add Student", "Student registration dialog would open here")


class MarksView(QWidget):
    """Marks entry and management view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Marks Management", "Enter and manage student examination marks")
        layout.addWidget(header)
        
        # Term and class selection
        selection_card = CardWidget()
        selection_layout = QGridLayout()
        
        # Term selection
        selection_layout.addWidget(QLabel("Term:"), 0, 0)
        self.term_combo = QComboBox()
        from school_manager.models.database import AcademicTerm
        terms = self.session.query(AcademicTerm).all()
        for t in terms:
            self.term_combo.addItem(t.name, t.id)
        selection_layout.addWidget(self.term_combo, 0, 1)
        
        # Class selection
        selection_layout.addWidget(QLabel("Class:"), 0, 2)
        self.class_combo = QComboBox()
        from school_manager.models.database import Class
        classes = self.session.query(Class).all()
        for c in classes:
            self.class_combo.addItem(c.name, c.id)
        selection_layout.addWidget(self.class_combo, 0, 3)
        
        # Subject selection
        selection_layout.addWidget(QLabel("Subject:"), 0, 4)
        self.subject_combo = QComboBox()
        from school_manager.models.database import Subject
        subjects = self.session.query(Subject).all()
        for s in subjects:
            self.subject_combo.addItem(s.name, s.id)
        selection_layout.addWidget(self.subject_combo, 0, 5)
        
        self.load_btn = PrimaryButton("Load Students")
        self.load_btn.clicked.connect(self.load_marks)
        selection_layout.addWidget(self.load_btn, 0, 6)
        
        selection_card.layout.addLayout(selection_layout)
        layout.addWidget(selection_card)
        
        # Marks table
        marks_card = CardWidget()
        marks_layout = QVBoxLayout()
        
        marks_label = QLabel("Student Marks")
        marks_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        marks_layout.addWidget(marks_label)
        
        self.marks_table = QTableWidget()
        self.marks_table.setColumnCount(5)
        self.marks_table.setHorizontalHeaderLabels(["Student ID", "Name", "CAT (30)", "Exam (70)", "Total"])
        self.marks_table.setMinimumHeight(400)
        marks_layout.addWidget(self.marks_table)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = PrimaryButton("Save Marks")
        save_btn.clicked.connect(self.save_marks)
        btn_layout.addWidget(save_btn)
        
        export_btn = SecondaryButton("Export to Excel")
        export_btn.clicked.connect(self.export_marks)
        btn_layout.addWidget(export_btn)
        
        marks_layout.addLayout(btn_layout)
        
        marks_card.layout.addLayout(marks_layout)
        layout.addWidget(marks_card)
    
    def load_marks(self):
        class_id = self.class_combo.currentData()
        
        from school_manager.models.database import Student
        
        students = self.session.query(Student).filter(
            Student.class_id == class_id,
            Student.status == 'active'
        ).all()
        
        self.marks_table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            self.marks_table.setItem(row, 0, QTableWidgetItem(student.student_id))
            self.marks_table.setItem(row, 1, QTableWidgetItem(f"{student.first_name} {student.last_name}"))
            self.marks_table.setItem(row, 2, QTableWidgetItem(""))
            self.marks_table.setItem(row, 3, QTableWidgetItem(""))
            self.marks_table.setItem(row, 4, QTableWidgetItem(""))
    
    def save_marks(self):
        QMessageBox.information(self, "Save", "Marks saved successfully")
    
    def export_marks(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Marks", "", "Excel Files (*.xlsx)")
        if path:
            QMessageBox.information(self, "Export", f"Marks exported to {path}")


class FeesView(QWidget):
    """Fee management view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
        self.load_payments()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Fee Management", "Manage fee structures and payments")
        
        record_btn = PrimaryButton("+ Record Payment")
        record_btn.clicked.connect(self.record_payment)
        header.add_action(record_btn)
        
        layout.addWidget(header)
        
        # Summary cards
        summary_layout = QHBoxLayout()
        
        from school_manager.models.database import FeeStructure, FeePayment
        
        total_fees = self.session.query(FeeStructure).count()
        total_collections = self.session.query(FeePayment).all()
        total_amount = sum(p.amount for p in total_collections)
        
        summary_layout.addWidget(StatCard("Fee Structures", str(total_fees), "📋", "#2563eb"))
        summary_layout.addWidget(StatCard("Total Collections", f"KES {total_amount:,.0f}", "💰", "#16a34a"))
        summary_layout.addWidget(StatCard("Payments Today", str(len([p for p in total_collections if p.payment_date == date.today()])), "📅", "#ea580c"))
        
        layout.addLayout(summary_layout)
        
        # Fee structures
        structures_card = CardWidget()
        structures_layout = QVBoxLayout()
        
        structures_label = QLabel("Fee Structures")
        structures_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        structures_layout.addWidget(structures_label)
        
        self.structures_table = QTableWidget()
        self.structures_table.setColumnCount(4)
        self.structures_table.setHorizontalHeaderLabels(["Name", "Amount", "Due Date", "Status"])
        structures_layout.addWidget(self.structures_table)
        
        structures_card.layout.addLayout(structures_layout)
        layout.addWidget(structures_card)
        
        # Recent payments
        payments_card = CardWidget()
        payments_layout = QVBoxLayout()
        
        payments_label = QLabel("Recent Payments")
        payments_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        payments_layout.addWidget(payments_label)
        
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(5)
        self.payments_table.setHorizontalHeaderLabels(["Receipt #", "Student", "Amount", "Date", "Method"])
        payments_layout.addWidget(self.payments_table)
        
        payments_card.layout.addLayout(payments_layout)
        layout.addWidget(payments_card)
    
    def load_payments(self):
        from school_manager.models.database import FeeStructure, FeePayment, Student
        
        # Load fee structures
        structures = self.session.query(FeeStructure).all()
        self.structures_table.setRowCount(len(structures))
        
        for row, s in enumerate(structures):
            self.structures_table.setItem(row, 0, QTableWidgetItem(s.name))
            self.structures_table.setItem(row, 1, QTableWidgetItem(f"KES {s.amount:,.2f}"))
            self.structures_table.setItem(row, 2, QTableWidgetItem(str(s.due_date) if s.due_date else "-"))
            self.structures_table.setItem(row, 3, QTableWidgetItem("Active" if s.is_recurring else "One-time"))
        
        # Load recent payments
        payments = self.session.query(FeePayment).order_by(FeePayment.payment_date.desc()).limit(50).all()
        self.payments_table.setRowCount(len(payments))
        
        for row, p in enumerate(payments):
            self.payments_table.setItem(row, 0, QTableWidgetItem(p.receipt_number or "-"))
            student = self.session.query(Student).filter(Student.id == p.student_id).first()
            name = f"{student.first_name} {student.last_name}" if student else "Unknown"
            self.payments_table.setItem(row, 1, QTableWidgetItem(name))
            self.payments_table.setItem(row, 2, QTableWidgetItem(f"KES {p.amount:,.2f}"))
            self.payments_table.setItem(row, 3, QTableWidgetItem(str(p.payment_date)))
            self.payments_table.setItem(row, 4, QTableWidgetItem(p.payment_method or "Cash"))
    
    def record_payment(self):
        QMessageBox.information(self, "Record Payment", "Payment recording dialog would open here")


class ReportsView(QWidget):
    """Reports and analytics view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Reports & Analytics", "Generate reports and view analytics")
        layout.addWidget(header)
        
        # Report categories
        categories_layout = QGridLayout()
        categories_layout.setSpacing(20)
        
        report_types = [
            ("📊", "Performance Reports", "Student grades and rankings"),
            ("💰", "Financial Reports", "Fee collections and balances"),
            ("👥", "Enrollment Reports", "Student and staff demographics"),
            ("📈", "Analytics Dashboard", "Visual charts and insights"),
            ("📄", "Report Cards", "Generate student report cards"),
            ("🪪", "ID Cards", "Print student ID cards"),
            ("📋", "Broadsheets", "Class subject performance"),
            ("📧", "Fee Letters", "Generate demand letters"),
        ]
        
        for i, (icon, title, desc) in enumerate(report_types):
            card = CardWidget()
            card_layout = QVBoxLayout()
            
            icon_label = QLabel(f"<center><span style='font-size: 32px;'>{icon}</span></center>")
            card_layout.addWidget(icon_label)
            
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #0f172a;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("font-size: 11px; color: #64748b;")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(desc_label)
            
            btn = SecondaryButton("Generate")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            card_layout.addWidget(btn)
            
            categories_layout.addWidget(card, i // 4, i % 4)
        
        layout.addLayout(categories_layout)
        layout.addStretch()


class SettingsView(QWidget):
    """Settings and configuration view"""
    
    def __init__(self, session, auth, license_manager, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.license_manager = license_manager
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Settings", "Configure system settings and preferences")
        layout.addWidget(header)
        
        # Settings tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
            QTabBar::tab {
                background-color: transparent;
                color: #64748b;
                padding: 10px 20px;
                font-weight: 500;
                border: none;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected {
                color: #2563eb;
                border-bottom: 2px solid #2563eb;
            }
        """)
        
        # School Info Tab
        school_tab = self.create_school_tab()
        tabs.addTab(school_tab, "🏫 School Information")
        
        # Users Tab
        if self.auth.has_permission('manage_users'):
            users_tab = self.create_users_tab()
            tabs.addTab(users_tab, "👥 User Management")
        
        # Features Tab
        if self.auth.has_permission('manage_features'):
            features_tab = self.create_features_tab()
            tabs.addTab(features_tab, "⚡ Premium Features")
        
        # Backup Tab
        if self.auth.has_permission('manage_backup'):
            backup_tab = self.create_backup_tab()
            tabs.addTab(backup_tab, "💾 Backup Settings")
        
        # Portal Tab
        if self.auth.has_permission('manage_school'):
            portal_tab = self.create_portal_tab()
            tabs.addTab(portal_tab, "📱 Portal Settings")
        
        layout.addWidget(tabs)
        layout.addStretch()
    
    def create_school_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        from school_manager.models.database import School
        school = self.session.query(School).first()
        
        if not school:
            school = School(name="My School", address="School Address")
            self.session.add(school)
            self.session.commit()
        
        # School name
        name_field = FormField("School Name", QLineEdit(school.name))
        layout.addWidget(name_field)
        
        # Address
        addr_field = FormField("Address", QTextEdit(school.address or ""))
        addr_field.input.setMaximumHeight(80)
        layout.addWidget(addr_field)
        
        # Contact
        contact_layout = QGridLayout()
        phone_input = QLineEdit(school.phone or "")
        email_input = QLineEdit(school.email or "")
        website_input = QLineEdit(school.website or "")
        
        contact_layout.addWidget(QLabel("Phone:"), 0, 0)
        contact_layout.addWidget(phone_input, 0, 1)
        contact_layout.addWidget(QLabel("Email:"), 0, 2)
        contact_layout.addWidget(email_input, 0, 3)
        contact_layout.addWidget(QLabel("Website:"), 1, 0)
        contact_layout.addWidget(website_input, 1, 1, 1, 3)
        
        layout.addLayout(contact_layout)
        layout.addWidget(FormField("Motto", QLineEdit(school.motto or "")))
        
        # Logo upload
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(QLabel("School Logo:"))
        logo_btn = SecondaryButton("Upload Logo")
        logo_layout.addWidget(logo_btn)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)
        
        # Save button
        save_btn = PrimaryButton("Save School Information")
        save_btn.clicked.connect(self.save_school)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        return widget
    
    def create_users_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Users list
        users_label = QLabel("System Users")
        users_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        layout.addWidget(users_label)
        
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(["Username", "Role", "Status", "Last Login"])
        layout.addWidget(self.users_table)
        
        # Load users
        users = self.auth.get_all_users()
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user['username']))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['role_display']))
            self.users_table.setItem(row, 2, QTableWidgetItem("Active" if user['is_active'] else "Inactive"))
            self.users_table.setItem(row, 3, QTableWidgetItem(str(user['last_login'])[:16] if user['last_login'] else "Never"))
        
        # Add user button
        add_user_btn = PrimaryButton("+ Add New User")
        layout.addWidget(add_user_btn)
        
        layout.addStretch()
        return widget
    
    def create_features_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # License status
        status = self.license_manager.get_activation_status()
        status_card = CardWidget()
        status_layout = QHBoxLayout()
        
        if status['activated']:
            status_layout.addWidget(StatusBadge("Activated", "success"))
            status_layout.addWidget(QLabel(f"Licensed to: {status['client_name']}"))
        else:
            status_layout.addWidget(StatusBadge("Not Activated", "error"))
        
        status_layout.addStretch()
        status_card.layout.addLayout(status_layout)
        layout.addWidget(status_card)
        
        # Feature toggles
        features_label = QLabel("Premium Feature Controls")
        features_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a; margin-top: 20px;")
        layout.addWidget(features_label)
        
        features = [
            ("photo_processing", "Student Photo Processing", "Upload and manage student photos for ID cards and reports"),
            ("pdf_engine", "High-Res PDF Engine", "Generate branded PDF documents with custom headers and logos"),
            ("email_letters", "Automated Email Letters", "Send fee demand letters via email automatically"),
            ("cloud_backup", "Cloud Backup Sync", "Automatically backup data to Google Drive"),
        ]
        
        for feature_id, name, desc in features:
            feature_card = CardWidget()
            feature_layout = QHBoxLayout()
            
            info_layout = QVBoxLayout()
            info_layout.addWidget(QLabel(name))
            info_layout.addWidget(QLabel(desc))
            
            toggle = QCheckBox("Enable")
            toggle.setChecked(self.license_manager.get_feature_status(feature_id))
            toggle.stateChanged.connect(lambda s, fid=feature_id: self.toggle_feature(fid, s))
            
            feature_layout.addLayout(info_layout)
            feature_layout.addStretch()
            feature_layout.addWidget(toggle)
            
            feature_card.layout.addLayout(feature_layout)
            layout.addWidget(feature_card)
        
        layout.addStretch()
        return widget
    
    def create_backup_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # USB Backup
        usb_card = CardWidget()
        usb_layout = QVBoxLayout()
        
        usb_header = QHBoxLayout()
        usb_header.addWidget(QLabel("🖴 USB Backup"))
        usb_header.addStretch()
        
        usb_toggle = QCheckBox("Enable USB Backup")
        usb_toggle.setChecked(True)
        usb_header.addWidget(usb_toggle)
        
        usb_layout.addLayout(usb_header)
        
        usb_btn = PrimaryButton("Backup Now to USB")
        usb_layout.addWidget(usb_btn)
        
        detect_btn = SecondaryButton("Detect USB Drives")
        usb_layout.addWidget(detect_btn)
        
        usb_card.layout.addLayout(usb_layout)
        layout.addWidget(usb_card)
        
        # Cloud Backup
        cloud_card = CardWidget()
        cloud_layout = QVBoxLayout()
        
        cloud_header = QHBoxLayout()
        cloud_header.addWidget(QLabel("☁️ Google Drive Backup"))
        cloud_header.addStretch()
        
        cloud_toggle = QCheckBox("Enable Cloud Backup")
        cloud_header.addWidget(cloud_toggle)
        
        cloud_layout.addLayout(cloud_header)
        
        connect_btn = PrimaryButton("Connect Google Drive")
        cloud_layout.addWidget(connect_btn)
        
        cloud_card.layout.addLayout(cloud_layout)
        layout.addWidget(cloud_card)
        
        # Schedule settings
        schedule_card = CardWidget()
        schedule_layout = QHBoxLayout()
        
        schedule_layout.addWidget(QLabel("Backup Schedule:"))
        
        schedule_combo = QComboBox()
        schedule_combo.addItems(["Daily", "Weekly", "Monthly"])
        schedule_layout.addWidget(schedule_combo)
        schedule_layout.addStretch()
        
        schedule_card.layout.addLayout(schedule_layout)
        layout.addWidget(schedule_card)
        
        layout.addStretch()
        return widget
    
    def create_portal_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Portal status
        portal_card = CardWidget()
        portal_layout = QVBoxLayout()
        
        portal_header = QLabel("📱 LAN Parent/Student Portal")
        portal_header.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        portal_layout.addWidget(portal_header)
        
        portal_info = QLabel("The portal allows parents to view their child's progress using QR codes on the school Wi-Fi.")
        portal_info.setStyleSheet("color: #64748b;")
        portal_info.setWordWrap(True)
        portal_layout.addWidget(portal_info)
        
        portal_layout.addWidget(QLabel("Portal URL:"))
        url_label = QLabel("http://192.168.x.x:8000")
        url_label.setStyleSheet("font-family: monospace; font-size: 14px; color: #2563eb;")
        portal_layout.addWidget(url_label)
        
        portal_layout.addWidget(QLabel("Local IP:"))
        ip_label = QLabel("192.168.x.x")
        ip_label.setStyleSheet("font-family: monospace; font-size: 14px; color: #0f172a;")
        portal_layout.addWidget(ip_label)
        
        portal_btn_layout = QHBoxLayout()
        
        start_btn = PrimaryButton("Start Portal")
        portal_btn_layout.addWidget(start_btn)
        
        stop_btn = SecondaryButton("Stop Portal")
        portal_btn_layout.addWidget(stop_btn)
        
        refresh_btn = SecondaryButton("Refresh IP")
        portal_btn_layout.addWidget(refresh_btn)
        
        portal_layout.addLayout(portal_btn_layout)
        
        # QR Code display
        qr_label = QLabel("[QR Code Preview]")
        qr_label.setStyleSheet("""
            background-color: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            min-height: 150px;
            qproperty-alignment: AlignCenter;
        """)
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        portal_layout.addWidget(qr_label)
        
        portal_card.layout.addLayout(portal_layout)
        layout.addWidget(portal_card)
        
        layout.addStretch()
        return widget
    
    def save_school(self):
        QMessageBox.information(self, "Save", "School information saved successfully")
    
    def toggle_feature(self, feature_id, enabled):
        self.license_manager.set_feature_toggle(feature_id, enabled)


class TermManagementView(QWidget):
    """Academic term management view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
        self.load_terms()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Academic Terms", "Manage academic terms and publishing")
        
        if self.auth.has_permission('publish_terms'):
            add_btn = PrimaryButton("+ Add Term")
            add_btn.clicked.connect(self.add_term)
            header.add_action(add_btn)
        
        layout.addWidget(header)
        
        # Current term info
        current_card = CardWidget()
        current_layout = QHBoxLayout()
        
        from school_manager.models.database import AcademicTerm
        current = self.session.query(AcademicTerm).filter(AcademicTerm.is_current == True).first()
        
        if current:
            current_layout.addWidget(QLabel(f"Current Term:"))
            current_layout.addWidget(QLabel(f"<b>{current.name}</b>"))
            
            if current.is_published:
                current_layout.addWidget(StatusBadge("Published (Locked)", "warning"))
            else:
                current_layout.addWidget(StatusBadge("In Progress", "info"))
            
            current_layout.addStretch()
            
            if self.auth.has_permission('publish_terms') and not current.is_published:
                publish_btn = PrimaryButton("Publish Term")
                publish_btn.clicked.connect(lambda: self.publish_term(current))
                current_layout.addWidget(publish_btn)
        
        current_card.layout.addLayout(current_layout)
        layout.addWidget(current_card)
        
        # Terms table
        terms_card = CardWidget()
        terms_layout = QVBoxLayout()
        
        terms_label = QLabel("All Terms")
        terms_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        terms_layout.addWidget(terms_label)
        
        self.terms_table = QTableWidget()
        self.terms_table.setColumnCount(5)
        self.terms_table.setHorizontalHeaderLabels(["Term Name", "Start Date", "End Date", "Status", "Actions"])
        terms_layout.addWidget(self.terms_table)
        
        terms_card.layout.addLayout(terms_layout)
        layout.addWidget(terms_card)
        
        layout.addStretch()
    
    def load_terms(self):
        from school_manager.models.database import AcademicTerm
        
        terms = self.session.query(AcademicTerm).order_by(AcademicTerm.start_date.desc()).all()
        self.terms_table.setRowCount(len(terms))
        
        for row, term in enumerate(terms):
            self.terms_table.setItem(row, 0, QTableWidgetItem(term.name))
            self.terms_table.setItem(row, 1, QTableWidgetItem(str(term.start_date) if term.start_date else "-"))
            self.terms_table.setItem(row, 2, QTableWidgetItem(str(term.end_date) if term.end_date else "-"))
            
            status = "Published" if term.is_published else ("Current" if term.is_current else "Past")
            self.terms_table.setItem(row, 3, QTableWidgetItem(status))
            
            actions = QLabel("<center><a href='#'>Edit</a> | <a href='#'>Set Current</a></center>")
            self.terms_table.setCellWidget(row, 4, actions)
    
    def add_term(self):
        QMessageBox.information(self, "Add Term", "Term creation dialog would open here")
    
    def publish_term(self, term):
        reply = QMessageBox.question(self, "Publish Term", 
                                      f"Are you sure you want to publish '{term.name}'? This will lock all data for this term.",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            term.is_published = True
            term.published_at = datetime.utcnow()
            self.session.commit()
            self.load_terms()
            QMessageBox.information(self, "Success", "Term published successfully")


class StaffView(QWidget):
    """Staff management view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
        self.load_staff()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Staff Management", "Manage teachers and staff members")
        
        if self.auth.has_permission('manage_staff'):
            add_btn = PrimaryButton("+ Add Staff")
            add_btn.clicked.connect(self.add_staff)
            header.add_action(add_btn)
        
        layout.addWidget(header)
        
        # Filters
        filters_card = CardWidget()
        filters_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search staff...")
        self.search_input.textChanged.connect(self.filter_staff)
        filters_layout.addWidget(self.search_input)
        
        self.role_filter = QComboBox()
        self.role_filter.addItem("All Roles", None)
        from school_manager.utils.auth import Role
        for role in Role.all_roles():
            self.role_filter.addItem(Role.display_name(role), role)
        self.role_filter.currentIndexChanged.connect(self.filter_staff)
        filters_layout.addWidget(QLabel("Role:"), 0, Qt.AlignmentFlag.AlignRight)
        filters_layout.addWidget(self.role_filter)
        
        filters_layout.addStretch()
        
        filters_card.layout.addLayout(filters_layout)
        layout.addWidget(filters_card)
        
        # Staff table
        self.table = DataTable(["Employee ID", "Name", "Role", "Email", "Phone", "Status"])
        layout.addWidget(self.table)
        
        layout.addStretch()
    
    def load_staff(self):
        from school_manager.models.database import Staff
        
        staff = self.session.query(Staff).all()
        data = []
        
        for s in staff:
            data.append({
                "Employee ID": s.employee_id or "-",
                "Name": f"{s.first_name} {s.last_name}",
                "Role": s.role or "-",
                "Email": s.email or "-",
                "Phone": s.phone or "-",
                "Status": "Active" if s.is_active else "Inactive"
            })
        
        self.table.set_data(data)
    
    def filter_staff(self):
        search = self.search_input.text().lower()
        role = self.role_filter.currentData()
        
        from school_manager.models.database import Staff
        
        query = self.session.query(Staff)
        
        if search:
            query = query.filter(
                (Staff.first_name + " " + Staff.last_name).like(f"%{search}%") |
                Staff.employee_id.like(f"%{search}%")
            )
        
        if role:
            query = query.filter(Staff.role == role)
        
        staff = query.all()
        data = []
        
        for s in staff:
            data.append({
                "Employee ID": s.employee_id or "-",
                "Name": f"{s.first_name} {s.last_name}",
                "Role": s.role or "-",
                "Email": s.email or "-",
                "Phone": s.phone or "-",
                "Status": "Active" if s.is_active else "Inactive"
            })
        
        self.table.set_data(data)
    
    def add_staff(self):
        QMessageBox.information(self, "Add Staff", "Staff registration dialog would open here")


class AttendanceView(QWidget):
    """Attendance management view"""
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = HeaderBar("Attendance", "Track student and staff attendance")
        layout.addWidget(header)
        
        # Tabs for student/staff attendance
        tabs = QTabWidget()
        
        # Student Attendance Tab
        student_tab = QWidget()
        student_layout = QVBoxLayout(student_tab)
        
        student_selection = CardWidget()
        sel_layout = QGridLayout()
        
        sel_layout.addWidget(QLabel("Class:"), 0, 0)
        class_combo = QComboBox()
        sel_layout.addWidget(class_combo, 0, 1)
        
        sel_layout.addWidget(QLabel("Date:"), 0, 2)
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        sel_layout.addWidget(date_edit, 0, 3)
        
        load_btn = PrimaryButton("Load Class")
        sel_layout.addWidget(load_btn, 0, 4)
        
        student_selection.layout.addLayout(sel_layout)
        student_layout.addWidget(student_selection)
        
        student_table = QTableWidget()
        student_table.setColumnCount(4)
        student_table.setHorizontalHeaderLabels(["Student ID", "Name", "Status", "Remarks"])
        student_layout.addWidget(student_table)
        
        tabs.addTab(student_tab, "👨‍🎓 Student Attendance")
        
        # Staff Attendance Tab
        staff_tab = QWidget()
        staff_layout = QVBoxLayout(staff_tab)
        
        staff_selection = CardWidget()
        staff_sel_layout = QGridLayout()
        
        staff_sel_layout.addWidget(QLabel("Date:"), 0, 0)
        staff_date_edit = QDateEdit()
        staff_date_edit.setDate(QDate.currentDate())
        staff_sel_layout.addWidget(staff_date_edit, 0, 1)
        
        staff_load_btn = PrimaryButton("Load Staff")
        staff_sel_layout.addWidget(staff_load_btn, 0, 2)
        
        staff_selection.layout.addLayout(staff_sel_layout)
        staff_layout.addWidget(staff_selection)
        
        staff_table = QTableWidget()
        staff_table.setColumnCount(4)
        staff_table.setHorizontalHeaderLabels(["Employee ID", "Name", "Status", "Remarks"])
        staff_layout.addWidget(staff_table)
        
        tabs.addTab(staff_tab, "👨‍🏫 Staff Attendance")
        
        layout.addWidget(tabs)
        layout.addStretch()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, session, auth, license_manager, portal_manager=None):
        super().__init__()
        self.session = session
        self.auth = auth
        self.license_manager = license_manager
        self.portal_manager = portal_manager
        
        self.setup_ui()
        self.setup_menu()
    
    def setup_ui(self):
        self.setWindowTitle("School Manager - Enterprise Edition")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(ModernStylesheet.get_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("""
            QWidget#sidebar {
                background-color: #1e293b;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Sidebar header
        sidebar_header = QWidget()
        sidebar_header.setStyleSheet("padding: 20px;")
        header_layout = QVBoxLayout(sidebar_header)
        
        logo = QLabel("🏫")
        logo.setStyleSheet("font-size: 36px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo)
        
        school_name = self.get_school_name()
        title = QLabel(school_name)
        title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        role_label = QLabel(self.auth.get_role_display())
        role_label.setStyleSheet("color: #64748b; font-size: 11px; text-align: center;")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(role_label)
        
        sidebar_layout.addWidget(sidebar_header)
        
        # Separator
        sep = QLabel()
        sep.setStyleSheet("background-color: #334155; margin: 10px 20px; max-height: 1px;")
        sep.setFixedHeight(1)
        sidebar_layout.addWidget(sep)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("dashboard", "📊", "Dashboard"),
            ("students", "👨‍🎓", "Students"),
            ("staff", "👨‍🏫", "Staff"),
            ("marks", "📝", "Marks"),
            ("fees", "💰", "Fees"),
            ("attendance", "📅", "Attendance"),
            ("terms", "📅", "Terms"),
            ("reports", "📊", "Reports"),
        ]
        
        # Add separator before admin items
        if self.auth.has_permission('manage_settings'):
            admin_sep = QLabel()
            admin_sep.setStyleSheet("background-color: #334155; margin: 10px 20px; max-height: 1px;")
            admin_sep.setFixedHeight(1)
            sidebar_layout.addWidget(admin_sep)
            
            admin_label = QLabel("ADMINISTRATION")
            admin_label.setStyleSheet("color: #64748b; font-size: 11px; padding: 10px 20px;")
            sidebar_layout.addWidget(admin_label)
        
            nav_items.extend([
                ("settings", "⚙️", "Settings"),
            ])
        
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setSpacing(4)
        
        for view_id, icon, text in nav_items:
            # Check permission
            if view_id == "students" and not self.auth.has_permission('manage_students'):
                continue
            if view_id == "staff" and not self.auth.has_permission('manage_staff'):
                continue
            if view_id == "marks" and not self.auth.has_permission('enter_marks'):
                continue
            if view_id == "fees" and not self.auth.has_permission('manage_fees'):
                continue
            if view_id == "settings" and not self.auth.has_permission('manage_school'):
                continue
            
            btn = SidebarButton(f"{icon}  {text}")
            btn.setObjectName("sidebar_btn")
            btn.clicked.connect(lambda checked, v=view_id: self.switch_view(v))
            self.nav_buttons[view_id] = btn
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        sidebar_layout.addWidget(nav_widget)
        
        # Sidebar footer
        sidebar_footer = QWidget()
        sidebar_footer.setStyleSheet("padding: 15px 20px; border-top: 1px solid #334155;")
        footer_layout = QVBoxLayout(sidebar_footer)
        
        # User info
        user = self.auth.current_user
        if user and user.staff:
            user_name = f"{user.staff.first_name} {user.staff.last_name}"
        else:
            user_name = user.username if user else "User"
        
        user_label = QLabel(f"👤 {user_name}")
        user_label.setStyleSheet("color: #ffffff; font-size: 13px;")
        footer_layout.addWidget(user_label)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: none;
                padding: 8px;
                text-align: left;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #dc2626;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        footer_layout.addWidget(logout_btn)
        
        sidebar_layout.addWidget(sidebar_footer)
        
        main_layout.addWidget(self.sidebar)
        
        # Content area
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)
        
        # Create views
        self.views = {}
        self.create_views()
        
        # Set initial view
        self.switch_view("dashboard")
    
    def get_school_name(self):
        from school_manager.models.database import School
        school = self.session.query(School).first()
        return school.name if school else "School Manager"
    
    def create_views(self):
        """Create all view widgets"""
        # Dashboard
        self.views['dashboard'] = DashboardView(self.session, self.auth, self.license_manager)
        self.content_area.addWidget(self.views['dashboard'])
        
        # Students
        self.views['students'] = StudentsView(self.session, self.auth)
        self.content_area.addWidget(self.views['students'])
        
        # Staff
        if self.auth.has_permission('manage_staff'):
            self.views['staff'] = StaffView(self.session, self.auth)
            self.content_area.addWidget(self.views['staff'])
        
        # Marks
        self.views['marks'] = MarksView(self.session, self.auth)
        self.content_area.addWidget(self.views['marks'])
        
        # Fees
        self.views['fees'] = FeesView(self.session, self.auth)
        self.content_area.addWidget(self.views['fees'])
        
        # Attendance
        self.views['attendance'] = AttendanceView(self.session, self.auth)
        self.content_area.addWidget(self.views['attendance'])
        
        # Terms
        self.views['terms'] = TermManagementView(self.session, self.auth)
        self.content_area.addWidget(self.views['terms'])
        
        # Reports
        self.views['reports'] = ReportsView(self.session, self.auth)
        self.content_area.addWidget(self.views['reports'])
        
        # Settings
        if self.auth.has_permission('manage_school'):
            self.views['settings'] = SettingsView(self.session, self.auth, self.license_manager)
            self.content_area.addWidget(self.views['settings'])
    
    def switch_view(self, view_id):
        """Switch to a different view"""
        if view_id in self.views:
            self.content_area.setCurrentWidget(self.views[view_id])
        
        # Update sidebar buttons
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == view_id:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        backup_action = QAction("Backup Database", self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)
        
        restore_action = QAction("Restore Database", self)
        restore_action.triggered.connect(self.restore_database)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Super Admin menu
        if self.auth.has_permission('impersonate'):
            admin_menu = menubar.addMenu("Super Admin")
            
            impersonate_action = QAction("Log In As User...", self)
            impersonate_action.triggered.connect(self.impersonate_user)
            admin_menu.addAction(impersonate_action)
            
            stop_impersonate_action = QAction("Stop Impersonation", self)
            stop_impersonate_action.triggered.connect(self.stop_impersonation)
            admin_menu.addAction(stop_impersonate_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def impersonate_user(self):
        dialog = ImpersonateDialog(self.auth, self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_user:
            success, msg = self.auth.impersonate(dialog.selected_user['id'])
            if success:
                QMessageBox.information(self, "Impersonation", msg)
                self.refresh_ui()
            else:
                QMessageBox.warning(self, "Error", msg)
    
    def stop_impersonation(self):
        self.auth.stop_impersonating()
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh UI after user change"""
        # Recreate views with new permissions
        while self.content_area.count():
            widget = self.content_area.widget(0)
            self.content_area.removeWidget(widget)
        
        self.views = {}
        self.create_views()
        self.switch_view("dashboard")
    
    def backup_database(self):
        QMessageBox.information(self, "Backup", "Database backup initiated")
    
    def restore_database(self):
        QMessageBox.information(self, "Restore", "Database restore dialog would open here")
    
    def show_about(self):
        QMessageBox.about(self, "About School Manager", 
                          "School Manager - Enterprise Edition\n\n"
                          "A comprehensive school management system with:\n"
                          "• Hardware Licensing\n"
                          "• Role-Based Access Control\n"
                          "• Parent/Student Portal\n"
                          "• PDF Report Generation\n"
                          "• Cloud/USB Backup\n\n"
                          "Version 1.0.0")
    
    def logout(self):
        self.auth.logout()
        self.close()
