"""
Enterprise Feature Registry - Super Admin Controlled
All features are defined here with default tiers. Super Admin can override per-school.
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import json

# Import Base from database models
from school_manager.models.database import Base


class FeatureRegistry:
    """
    Central registry of ALL available features.
    Super Admin controls which features are enabled per school.
    """
    
    # Feature categories
    CATEGORY_CORE = 'core'
    CATEGORY_ACADEMIC = 'academic'
    CATEGORY_FINANCE = 'finance'
    CATEGORY_ADMIN = 'admin'
    CATEGORY_PORTAL = 'portal'
    CATEGORY_ANALYTICS = 'analytics'
    CATEGORY_INTEGRATION = 'integration'
    CATEGORY_PREMIUM = 'premium'
    
    @classmethod
    def get_all_features(cls):
        """Get all available features with their definitions"""
        return {
            # ===== CORE FEATURES (Always Included) =====
            'core_students': {
                'name': 'Student Management',
                'category': cls.CATEGORY_CORE,
                'description': 'Basic student registration and management',
                'default_tier': None,  # Always available
                'is_critical': True,
                'icon': '👨‍🎓',
            },
            'core_staff': {
                'name': 'Staff Management',
                'category': cls.CATEGORY_CORE,
                'description': 'Staff records and basic management',
                'default_tier': None,
                'is_critical': True,
                'icon': '👨‍🏫',
            },
            'core_classes': {
                'name': 'Class Management',
                'category': cls.CATEGORY_CORE,
                'description': 'Create and manage classes/streams',
                'default_tier': None,
                'is_critical': True,
                'icon': '🏫',
            },
            'core_subjects': {
                'name': 'Subject Management',
                'category': cls.CATEGORY_CORE,
                'description': 'Subject catalog and assignments',
                'default_tier': None,
                'is_critical': True,
                'icon': '📚',
            },
            'core_attendance': {
                'name': 'Attendance Tracking',
                'category': cls.CATEGORY_CORE,
                'description': 'Daily student and staff attendance',
                'default_tier': None,
                'is_critical': True,
                'icon': '📅',
            },
            'core_marks': {
                'name': 'Marks Entry',
                'category': cls.CATEGORY_CORE,
                'description': 'Enter and manage exam marks',
                'default_tier': None,
                'is_critical': True,
                'icon': '📝',
            },
            'core_terms': {
                'name': 'Term Management',
                'category': cls.CATEGORY_CORE,
                'description': 'Academic terms and publishing',
                'default_tier': None,
                'is_critical': True,
                'icon': '📆',
            },
            
            # ===== ACADEMIC FEATURES =====
            'academic_report_cards': {
                'name': 'Report Card Generation',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Generate student report cards (PDF)',
                'default_tier': 'bronze',
                'icon': '📄',
            },
            'academic_broadsheets': {
                'name': 'Class Broadsheets',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Subject performance broadsheets',
                'default_tier': 'bronze',
                'icon': '📊',
            },
            'academic_rankings': {
                'name': 'Student Rankings',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Class and subject rankings',
                'default_tier': 'bronze',
                'icon': '🏆',
            },
            'academic_promotions': {
                'name': 'Student Promotions',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'End-of-year promotion workflow',
                'default_tier': 'silver',
                'icon': '⬆️',
            },
            'academic_timetable': {
                'name': 'Timetable Management',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Class timetables and scheduling',
                'default_tier': 'gold',
                'icon': '⏰',
            },
            'academic_exams': {
                'name': 'Exam Management',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Exam schedules and seating',
                'default_tier': 'silver',
                'icon': '📋',
            },
            'academic_assignments': {
                'name': 'Assignment Tracking',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Create and track assignments',
                'default_tier': 'gold',
                'icon': '📌',
            },
            'academic_lessons': {
                'name': 'Lesson Plans',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Lesson plan templates and tracking',
                'default_tier': 'gold',
                'icon': '📖',
            },
            'academic_grading': {
                'name': 'Custom Grading Schemes',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'Configure custom grade definitions',
                'default_tier': 'silver',
                'icon': '🔢',
            },
            'academic_comments': {
                'name': 'Auto-Generated Comments',
                'category': cls.CATEGORY_ACADEMIC,
                'description': 'AI-generated teacher comments',
                'default_tier': 'silver',
                'icon': '💬',
            },
            
            # ===== FINANCE FEATURES =====
            'finance_fees': {
                'name': 'Fee Management',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Fee structures and collections',
                'default_tier': 'bronze',
                'icon': '💰',
            },
            'finance_receipts': {
                'name': 'Payment Receipts',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Generate printable receipts',
                'default_tier': 'bronze',
                'icon': '🧾',
            },
            'finance_statements': {
                'name': 'Student Statements',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Fee balance statements',
                'default_tier': 'bronze',
                'icon': '📃',
            },
            'finance_reminders': {
                'name': 'Fee Reminders',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Automated fee reminder messages',
                'default_tier': 'silver',
                'icon': '🔔',
            },
            'finance_demand_letters': {
                'name': 'Fee Demand Letters',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Generate PDF demand letters',
                'default_tier': 'silver',
                'icon': '📧',
            },
            'finance_expenses': {
                'name': 'Expense Tracking',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Track school expenses',
                'default_tier': 'silver',
                'icon': '💸',
            },
            'finance_budgets': {
                'name': 'Budget Management',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Annual budgeting and tracking',
                'default_tier': 'gold',
                'icon': '📈',
            },
            'finance_payroll': {
                'name': 'Staff Payroll',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Salary processing and payslips',
                'default_tier': 'gold',
                'icon': '💵',
            },
            'finance_reports': {
                'name': 'Financial Reports',
                'category': cls.CATEGORY_FINANCE,
                'description': 'Financial statements and reports',
                'default_tier': 'silver',
                'icon': '📑',
            },
            
            # ===== ADMIN FEATURES =====
            'admin_users': {
                'name': 'User Management',
                'category': cls.CATEGORY_ADMIN,
                'description': 'Create and manage system users',
                'default_tier': 'bronze',
                'icon': '👥',
            },
            'admin_roles': {
                'name': 'Role Management',
                'category': cls.CATEGORY_ADMIN,
                'description': 'Configure roles and permissions',
                'default_tier': 'bronze',
                'icon': '🔐',
            },
            'admin_backup': {
                'name': 'Backup Management',
                'category': cls.CATEGORY_ADMIN,
                'description': 'USB and cloud backups',
                'default_tier': 'bronze',
                'icon': '💾',
            },
            'admin_audit': {
                'name': 'Audit Logs',
                'category': cls.CATEGORY_ADMIN,
                'description': 'System activity logs',
                'default_tier': 'silver',
                'icon': '🔍',
            },
            'admin_settings': {
                'name': 'School Settings',
                'category': cls.CATEGORY_ADMIN,
                'description': 'School profile and branding',
                'default_tier': 'bronze',
                'icon': '⚙️',
            },
            
            # ===== PORTAL FEATURES =====
            'portal_parent': {
                'name': 'Parent Portal',
                'category': cls.CATEGORY_PORTAL,
                'description': 'Parent/student web portal',
                'default_tier': 'silver',
                'icon': '📱',
            },
            'portal_qr': {
                'name': 'QR Code Access',
                'category': cls.CATEGORY_PORTAL,
                'description': 'QR code for portal access',
                'default_tier': 'silver',
                'icon': '📲',
            },
            'portal_notifications': {
                'name': 'Push Notifications',
                'category': cls.CATEGORY_PORTAL,
                'description': 'Mobile push notifications',
                'default_tier': 'gold',
                'icon': '🔔',
            },
            'portal_whatsapp': {
                'name': 'WhatsApp Integration',
                'category': cls.CATEGORY_PORTAL,
                'description': 'WhatsApp messaging',
                'default_tier': 'gold',
                'icon': '💬',
            },
            'portal_student': {
                'name': 'Student Self-Service',
                'category': cls.CATEGORY_PORTAL,
                'description': 'Student portal access',
                'default_tier': 'silver',
                'icon': '🎓',
            },
            
            # ===== ANALYTICS FEATURES =====
            'analytics_dashboard': {
                'name': 'Analytics Dashboard',
                'category': cls.CATEGORY_ANALYTICS,
                'description': 'Visual charts and insights',
                'default_tier': 'silver',
                'icon': '📊',
            },
            'analytics_enrollment': {
                'name': 'Enrollment Analytics',
                'category': cls.CATEGORY_ANALYTICS,
                'description': 'Student enrollment trends',
                'default_tier': 'silver',
                'icon': '📈',
            },
            'analytics_performance': {
                'name': 'Performance Analytics',
                'category': cls.CATEGORY_ANALYTICS,
                'description': 'Academic performance insights',
                'default_tier': 'silver',
                'icon': '🎯',
            },
            'analytics_predictions': {
                'name': 'Predictive Analytics',
                'category': cls.CATEGORY_ANALYTICS,
                'description': 'AI-powered predictions',
                'default_tier': 'platinum',
                'icon': '🤖',
            },
            'analytics_custom_reports': {
                'name': 'Custom Reports',
                'category': cls.CATEGORY_ANALYTICS,
                'description': 'Build custom report templates',
                'default_tier': 'gold',
                'icon': '📝',
            },
            'analytics_exports': {
                'name': 'Data Exports',
                'category': cls.CATEGORY_ANALYTICS,
                'description': 'Export data to Excel/PDF',
                'default_tier': 'bronze',
                'icon': '📤',
            },
            
            # ===== INTEGRATION FEATURES =====
            'integration_photos': {
                'name': 'Student Photos',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Upload and manage photos',
                'default_tier': 'silver',
                'icon': '📷',
            },
            'integration_id_cards': {
                'name': 'ID Card Generator',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Generate printable ID cards',
                'default_tier': 'silver',
                'icon': '🪪',
            },
            'integration_pdf': {
                'name': 'Custom PDF Branding',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Branded PDF documents',
                'default_tier': 'silver',
                'icon': '🎨',
            },
            'integration_email': {
                'name': 'Email Integration',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Send emails from system',
                'default_tier': 'gold',
                'icon': '📧',
            },
            'integration_sms': {
                'name': 'SMS Integration',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Send SMS messages',
                'default_tier': 'gold',
                'icon': '📱',
            },
            'integration_cloud': {
                'name': 'Cloud Backup',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Google Drive backup',
                'default_tier': 'gold',
                'icon': '☁️',
            },
            'integration_payments': {
                'name': 'Online Payments',
                'category': cls.CATEGORY_INTEGRATION,
                'description': 'Payment gateway integration',
                'default_tier': 'gold',
                'icon': '💳',
            },
            
            # ===== PREMIUM ADD-ONS =====
            'premium_library': {
                'name': 'Library Management',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Book inventory and borrowing',
                'default_tier': 'silver',
                'icon': '📚',
            },
            'premium_medical': {
                'name': 'Medical Records',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Health records management',
                'default_tier': 'silver',
                'icon': '🏥',
            },
            'premium_disciplinary': {
                'name': 'Disciplinary Tracking',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Behavior management',
                'default_tier': 'silver',
                'icon': '⚠️',
            },
            'premium_alumni': {
                'name': 'Alumni Management',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Graduates and alumni records',
                'default_tier': 'silver',
                'icon': '🎓',
            },
            'premium_hostel': {
                'name': 'Hostel Management',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Boarding and dormitory',
                'default_tier': 'gold',
                'icon': '🏠',
            },
            'premium_transport': {
                'name': 'Transport Management',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'School transport/bus tracking',
                'default_tier': 'gold',
                'icon': '🚌',
            },
            'premium_canteen': {
                'name': 'Canteen Management',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Meals and cafeteria',
                'default_tier': 'gold',
                'icon': '🍽️',
            },
            'premium_multi_branch': {
                'name': 'Multi-Branch Support',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Multiple school campuses',
                'default_tier': 'platinum',
                'icon': '🏢',
            },
            'premium_api': {
                'name': 'API Access',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'REST API for integrations',
                'default_tier': 'platinum',
                'icon': '🔌',
            },
            'premium_white_label': {
                'name': 'White Label',
                'category': cls.CATEGORY_PREMIUM,
                'description': 'Custom branding domain',
                'default_tier': 'platinum',
                'icon': '✨',
            },
        }
    
    @classmethod
    def get_features_by_category(cls):
        """Group features by category"""
        features = cls.get_all_features()
        categories = {}
        
        for feat_id, feat_data in features.items():
            cat = feat_data['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'id': feat_id,
                **feat_data
            })
        
        return categories
    
    @classmethod
    def get_category_display_name(cls, category):
        """Get display name for category"""
        names = {
            cls.CATEGORY_CORE: '🔧 Core Features',
            cls.CATEGORY_ACADEMIC: '📚 Academic',
            cls.CATEGORY_FINANCE: '💰 Finance',
            cls.CATEGORY_ADMIN: '⚙️ Administration',
            cls.CATEGORY_PORTAL: '📱 Portals',
            cls.CATEGORY_ANALYTICS: '📊 Analytics',
            cls.CATEGORY_INTEGRATION: '🔗 Integration',
            cls.CATEGORY_PREMIUM: '💎 Premium Add-ons',
        }
        return names.get(category, category)


class FeatureManager:
    """
    Manages feature access for schools.
    Combines tier defaults with Super Admin overrides.
    """
    
    def __init__(self, session, school_id=None):
        self.session = session
        self.school_id = school_id
    
    def get_tier_defaults(self, tier):
        """Get default features for a tier"""
        features = FeatureRegistry.get_all_features()
        tier_features = []
        
        for feat_id, feat_data in features.items():
            default_tier = feat_data.get('default_tier')
            # Core features are always available
            if default_tier is None:
                tier_features.append(feat_id)
            elif default_tier == tier:
                tier_features.append(feat_id)
            elif self._tier_rank(default_tier) <= self._tier_rank(tier):
                tier_features.append(feat_id)
        
        return tier_features
    
    def _tier_rank(self, tier):
        """Get numeric rank for tier (lower = more features)"""
        ranks = {
            None: 0,  # Core features
            'bronze': 1,
            'silver': 2,
            'gold': 3,
            'platinum': 4,
        }
        return ranks.get(tier, 0)
    
    def get_school_features(self, school_id):
        """Get all enabled features for a school"""
        from school_manager.models.database import License
        
        # Get tier from license
        machine_id = self._get_machine_id()
        license = self.session.query(License).filter(
            License.machine_id == machine_id
        ).first()
        
        tier = license.tier if license else 'bronze'
        
        # Get tier defaults
        enabled = set(self.get_tier_defaults(tier))
        
        # School-specific overrides stored in license or a separate table
        # For simplicity, we use the features JSON from license
        if license and license.features:
            try:
                import json
                disabled = json.loads(license.features).get('disabled_features', [])
                enabled -= set(disabled)
            except:
                pass
        
        return list(enabled)
    
    def _get_machine_id(self):
        """Get current machine ID"""
        from school_manager.utils.hardware import HardwareFingerprint
        return HardwareFingerprint.get_machine_id()
    
    def is_feature_enabled(self, school_id, feature_id):
        """Check if a specific feature is enabled"""
        features = self.get_school_features(school_id)
        return feature_id in features
    
    def enable_feature(self, school_id, feature_id):
        """Enable a feature for a school"""
        # Feature enable logic - simplified version
        pass
    
    def disable_feature(self, school_id, feature_id):
        """Disable a feature for a school"""
        # Feature disable logic - simplified version
        pass
    
    def reset_to_tier_defaults(self, school_id):
        """Reset school to tier default features"""
        pass
    
    def check_limit(self, school_id, entity_type, current_count):
        """Check if school is within their limit"""
        from school_manager.models.database import License
        
        machine_id = self._get_machine_id()
        license = self.session.query(License).filter(
            License.machine_id == machine_id
        ).first()
        
        if not license:
            return False, "No license found"
        
        limit = getattr(license, f'max_{entity_type}')
        
        if limit == -1 or limit is None:
            return True, "Unlimited"
        
        if current_count >= limit:
            return False, f"Limit reached ({current_count}/{limit})"
        
        return True, f"{current_count}/{limit}"
