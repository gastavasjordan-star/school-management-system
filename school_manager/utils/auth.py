"""
Authentication & Role-Based Access Control
"""
import hashlib
from datetime import datetime
from functools import wraps

class Role:
    """User roles with associated permissions"""
    SUPER_ADMIN = 'SUPER_ADMIN'
    ADMIN = 'ADMIN'
    HEAD_TEACHER = 'HEAD_TEACHER'
    DEPUTY_HEAD = 'DEPUTY_HEAD'
    DOS = 'DOS'
    CLASS_TEACHER = 'CLASS_TEACHER'
    SUBJECT_TEACHER = 'SUBJECT_TEACHER'
    BURSAR = 'BURSAR'
    SECRETARY = 'SECRETARY'
    LIBRARIAN = 'LIBRARIAN'
    EXAMINATION_OFFICER = 'EXAMINATION_OFFICER'
    
    @classmethod
    def all_roles(cls):
        return [
            cls.SUPER_ADMIN, cls.ADMIN, cls.HEAD_TEACHER, cls.DEPUTY_HEAD,
            cls.DOS, cls.CLASS_TEACHER, cls.SUBJECT_TEACHER, 
            cls.BURSAR, cls.SECRETARY, cls.LIBRARIAN, cls.EXAMINATION_OFFICER
        ]
    
    @classmethod
    def display_name(cls, role):
        names = {
            cls.SUPER_ADMIN: 'Super Admin',
            cls.ADMIN: 'School Admin / Director',
            cls.HEAD_TEACHER: 'Head Teacher',
            cls.DEPUTY_HEAD: 'Deputy Head Teacher',
            cls.DOS: 'Director of Studies',
            cls.CLASS_TEACHER: 'Class Teacher',
            cls.SUBJECT_TEACHER: 'Subject Teacher',
            cls.BURSAR: 'Bursar',
            cls.SECRETARY: 'Secretary / Registrar',
            cls.LIBRARIAN: 'Librarian',
            cls.EXAMINATION_OFFICER: 'Examination Officer',
        }
        return names.get(role, role)
    
    @classmethod
    def category(cls, role):
        """Get role category"""
        categories = {
            cls.SUPER_ADMIN: 'administration',
            cls.ADMIN: 'administration',
            cls.HEAD_TEACHER: 'administration',
            cls.DEPUTY_HEAD: 'administration',
            cls.DOS: 'academic',
            cls.CLASS_TEACHER: 'academic',
            cls.SUBJECT_TEACHER: 'academic',
            cls.EXAMINATION_OFFICER: 'academic',
            cls.BURSAR: 'finance',
            cls.SECRETARY: 'administration',
            cls.LIBRARIAN: 'support',
        }
        return categories.get(role, 'other')
    
    @classmethod
    def permissions(cls, role):
        """Define permissions for each role"""
        perms = {
            # === SUPER ADMIN ===
            cls.SUPER_ADMIN: {
                'all': True,
                'manage_users': True,
                'manage_licenses': True,
                'manage_features': True,
                'manage_school': True,
                'manage_students': True,
                'manage_staff': True,
                'manage_staff_view': True,
                'manage_staff_edit': True,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': True,
                'process_payments': True,
                'view_financials': True,
                'manage_backup': True,
                'impersonate': True,
                'publish_terms': True,
                'manage_library': True,
                'manage_medical': True,
                'manage_disciplinary': True,
                'manage_payroll': True,
                'approve_leaves': True,
                'view_audit_logs': True,
                'export_data': True,
            },
            
            # === SCHOOL ADMIN ===
            cls.ADMIN: {
                'all': False,
                'manage_users': True,
                'manage_school': True,
                'manage_students': True,
                'manage_staff': True,
                'manage_staff_view': True,
                'manage_staff_edit': True,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': True,
                'process_payments': True,
                'view_financials': True,
                'manage_backup': True,
                'impersonate': False,
                'publish_terms': True,
                'manage_library': True,
                'manage_medical': True,
                'manage_disciplinary': True,
                'manage_payroll': True,
                'approve_leaves': True,
                'view_audit_logs': True,
                'export_data': True,
            },
            
            # === HEAD TEACHER ===
            cls.HEAD_TEACHER: {
                'all': False,
                'manage_users': False,
                'manage_school': True,
                'manage_students': True,
                'manage_staff': True,
                'manage_staff_view': True,  # Can VIEW staff details
                'manage_staff_edit': False,  # Cannot EDIT staff
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': True,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': True,
                'manage_library': True,
                'manage_medical': True,
                'manage_disciplinary': True,
                'manage_payroll': True,
                'approve_leaves': True,
                'view_audit_logs': True,
                'export_data': True,
            },
            
            # === DEPUTY HEAD ===
            cls.DEPUTY_HEAD: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': True,
                'manage_staff_view': True,
                'manage_staff_edit': False,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': False,
                'manage_library': False,
                'manage_medical': True,
                'manage_disciplinary': True,
                'manage_payroll': False,
                'approve_leaves': True,
                'view_audit_logs': False,
                'export_data': True,
            },
            
            # === DIRECTOR OF STUDIES ===
            cls.DOS: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': False,
                'manage_staff_view': True,
                'manage_staff_edit': False,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': True,
                'manage_library': False,
                'manage_medical': False,
                'manage_disciplinary': False,
                'manage_payroll': False,
                'approve_leaves': False,
                'view_audit_logs': False,
                'export_data': True,
            },
            
            # === CLASS TEACHER ===
            cls.CLASS_TEACHER: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': False,
                'manage_staff_view': False,
                'manage_staff_edit': False,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': False,
                'manage_library': False,
                'manage_medical': False,
                'manage_disciplinary': True,
                'manage_payroll': False,
                'approve_leaves': False,
                'view_audit_logs': False,
                'export_data': False,
            },
            
            # === SUBJECT TEACHER ===
            cls.SUBJECT_TEACHER: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': False,
                'manage_staff': False,
                'manage_staff_view': False,
                'manage_staff_edit': False,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': False,
                'manage_library': False,
                'manage_medical': False,
                'manage_disciplinary': False,
                'manage_payroll': False,
                'approve_leaves': False,
                'view_audit_logs': False,
                'export_data': False,
            },
            
            # === BURSAR ===
            cls.BURSAR: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': False,
                'manage_staff_view': True,
                'manage_staff_edit': False,
                'manage_subjects': False,
                'manage_classes': False,
                'enter_marks': False,
                'view_reports': True,
                'manage_fees': True,
                'process_payments': True,
                'view_financials': True,
                'manage_backup': True,
                'impersonate': False,
                'publish_terms': False,
                'manage_library': False,
                'manage_medical': False,
                'manage_disciplinary': False,
                'manage_payroll': True,
                'approve_leaves': False,
                'view_audit_logs': True,
                'export_data': True,
            },
            
            # === SECRETARY ===
            cls.SECRETARY: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': True,
                'manage_staff_view': True,
                'manage_staff_edit': True,
                'manage_subjects': False,
                'manage_classes': False,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': True,
                'process_payments': True,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': False,
                'manage_library': False,
                'manage_medical': True,
                'manage_disciplinary': False,
                'manage_payroll': False,
                'approve_leaves': False,
                'view_audit_logs': False,
                'export_data': True,
            },
            
            # === LIBRARIAN ===
            cls.LIBRARIAN: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': False,
                'manage_staff_view': True,
                'manage_staff_edit': False,
                'manage_subjects': False,
                'manage_classes': False,
                'enter_marks': False,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': False,
                'manage_library': True,
                'manage_medical': False,
                'manage_disciplinary': False,
                'manage_payroll': False,
                'approve_leaves': False,
                'view_audit_logs': False,
                'export_data': True,
            },
            
            # === EXAMINATION OFFICER ===
            cls.EXAMINATION_OFFICER: {
                'all': False,
                'manage_users': False,
                'manage_school': False,
                'manage_students': True,
                'manage_staff': False,
                'manage_staff_view': True,
                'manage_staff_edit': False,
                'manage_subjects': True,
                'manage_classes': True,
                'enter_marks': True,
                'view_reports': True,
                'manage_fees': False,
                'process_payments': False,
                'view_financials': False,
                'manage_backup': False,
                'impersonate': False,
                'publish_terms': True,
                'manage_library': False,
                'manage_medical': False,
                'manage_disciplinary': False,
                'manage_payroll': False,
                'approve_leaves': False,
                'view_audit_logs': False,
                'export_data': True,
            },
        }
        return perms.get(role, {})


class AuthManager:
    """Authentication and session management"""
    
    def __init__(self, db_session):
        self.session = db_session
        self.current_user = None
        self.impersonating = False
        self.original_user = None
    
    @staticmethod
    def hash_password(password, salt=None):
        """Hash a password with optional salt"""
        if salt is None:
            salt = 'school_manager_salt'
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        from school_manager.models.database import User
        
        password_hash = self.hash_password(password)
        user = self.session.query(User).filter(
            User.username == username,
            User.is_active == True
        ).first()
        
        if user and user.password_hash == password_hash:
            user.last_login = datetime.utcnow()
            self.session.commit()
            self.current_user = user
            return user
        
        return None
    
    def logout(self):
        """Log out current user"""
        if self.impersonating and self.original_user:
            self.current_user = self.original_user
            self.impersonating = False
        else:
            self.current_user = None
    
    def impersonate(self, user_id):
        """Impersonate another user (Super Admin only)"""
        from school_manager.models.database import User
        
        if not self.has_permission('impersonate'):
            return False, "Permission denied"
        
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            if not self.impersonating:
                self.original_user = self.current_user
            self.current_user = user
            self.impersonating = True
            return True, f"Now impersonating {user.username}"
        
        return False, "User not found"
    
    def stop_impersonating(self):
        """Stop impersonation and return to original user"""
        if self.impersonating and self.original_user:
            self.current_user = self.original_user
            self.impersonating = False
            self.original_user = None
            return True
        return False
    
    def has_permission(self, permission):
        """Check if current user has a specific permission"""
        if not self.current_user:
            return False
        
        perms = Role.permissions(self.current_user.role)
        
        if perms.get('all', False):
            return True
        
        return perms.get(permission, False)
    
    def get_role_display(self):
        """Get display name for current user's role"""
        if not self.current_user:
            return "Guest"
        return Role.display_name(self.current_user.role)
    
    def create_user(self, username, password, role, staff_id=None):
        """Create a new user"""
        from school_manager.models.database import User
        
        # Check if username exists
        existing = self.session.query(User).filter(User.username == username).first()
        if existing:
            return None, "Username already exists"
        
        user = User(
            username=username,
            password_hash=self.hash_password(password),
            role=role,
            staff_id=staff_id,
            is_active=True
        )
        self.session.add(user)
        self.session.commit()
        
        return user, "User created successfully"
    
    def change_password(self, user_id, new_password):
        """Change a user's password"""
        from school_manager.models.database import User
        
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            user.password_hash = self.hash_password(new_password)
            self.session.commit()
            return True
        return False
    
    def get_all_users(self):
        """Get all users with their details"""
        from school_manager.models.database import User, Staff
        
        users = self.session.query(User).all()
        result = []
        for u in users:
            staff_name = None
            if u.staff_id:
                staff = self.session.query(Staff).filter(Staff.id == u.staff_id).first()
                if staff:
                    staff_name = f"{staff.first_name} {staff.last_name}"
            
            result.append({
                'id': u.id,
                'username': u.username,
                'role': u.role,
                'role_display': Role.display_name(u.role),
                'staff_id': u.staff_id,
                'staff_name': staff_name,
                'is_active': u.is_active,
                'last_login': u.last_login
            })
        return result
    
    def deactivate_user(self, user_id):
        """Deactivate a user"""
        from school_manager.models.database import User
        
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = False
            self.session.commit()
            return True
        return False
    
    def log_action(self, action, entity_type=None, entity_id=None, details=None):
        """Log an audit trail entry"""
        from school_manager.models.database import AuditLog
        
        if not self.current_user:
            return
        
        log = AuditLog(
            user_id=self.current_user.id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            timestamp=datetime.utcnow()
        )
        self.session.add(log)
        self.session.commit()


def require_permission(permission):
    """Decorator to require a specific permission"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'auth'):
                return False, "Authentication not configured"
            
            if not self.auth.has_permission(permission):
                return False, f"Permission denied: {permission} required"
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def require_role(*roles):
    """Decorator to require specific roles"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'auth'):
                return False, "Authentication not configured"
            
            if self.auth.current_user.role not in roles:
                return False, f"Role not allowed: required {roles}"
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
