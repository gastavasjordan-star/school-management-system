"""
Feature Access Middleware
Decorator-based access control for all features
"""
from functools import wraps


class FeatureRequired(Exception):
    """Exception raised when feature is not available"""
    def __init__(self, feature_id, feature_name):
        self.feature_id = feature_id
        self.feature_name = feature_name
        super().__init__(f"Feature '{feature_name}' is not available")


def require_feature(feature_id, show_message=True):
    """Decorator to require a specific feature"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'check_feature_access'):
                enabled, msg = self.check_feature_access(feature_id)
                if not enabled:
                    if show_message and hasattr(self, 'show_warning'):
                        self.show_warning("Feature Not Available", msg)
                    return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class FeatureAccessChecker:
    """Mixin class for checking feature access"""
    
    def __init__(self):
        self._feature_manager = None
        self._school_id = None
    
    def init_feature_checker(self, session, school_id):
        from school_manager.models.features import FeatureManager
        self._feature_manager = FeatureManager(session, school_id)
        self._school_id = school_id
    
    def check_feature_access(self, feature_id):
        if not self._feature_manager:
            return True, "OK"
        
        enabled = self._feature_manager.is_feature_enabled(self._school_id, feature_id)
        if enabled:
            return True, "Available"
        
        from school_manager.models.features import FeatureRegistry
        features = FeatureRegistry.get_all_features()
        feat_data = features.get(feature_id, {})
        feat_name = feat_data.get('name', feature_id)
        tier = feat_data.get('default_tier', 'bronze')
        
        tier_names = {None: 'Core', 'bronze': 'Bronze', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'}
        msg = f"'{feat_name}' requires {tier_names.get(tier, tier)} subscription."
        return False, msg
    
    def show_warning(self, title, message):
        print(f"WARNING: {title} - {message}")
    
    def check_limit(self, entity_type, current_count):
        if not self._feature_manager:
            return True, "OK"
        return self._feature_manager.check_limit(self._school_id, entity_type, current_count)


# Feature module mapping
FEATURE_MODULES = {
    'add_student': 'core_students',
    'view_student': 'core_students',
    'student_photos': 'integration_photos',
    'enter_marks': 'core_marks',
    'generate_report_cards': 'academic_report_cards',
    'class_broadsheet': 'academic_broadsheets',
    'fee_management': 'finance_fees',
    'record_payment': 'finance_fees',
    'print_receipt': 'finance_receipts',
    'fee_reminder': 'finance_reminders',
    'fee_letter': 'finance_demand_letters',
    'analytics_dashboard': 'analytics_dashboard',
    'enrollment_analytics': 'analytics_enrollment',
    'performance_analytics': 'analytics_performance',
    'custom_reports': 'analytics_custom_reports',
    'data_export': 'analytics_exports',
    'parent_portal': 'portal_parent',
    'qr_code': 'portal_qr',
    'push_notifications': 'portal_notifications',
    'whatsapp': 'portal_whatsapp',
    'library': 'premium_library',
    'medical': 'premium_medical',
    'disciplinary': 'premium_disciplinary',
    'alumni': 'premium_alumni',
    'hostel': 'premium_hostel',
    'transport': 'premium_transport',
    'id_cards': 'integration_id_cards',
    'pdf_branding': 'integration_pdf',
    'email': 'integration_email',
    'sms': 'integration_sms',
    'cloud_backup': 'integration_cloud',
    'online_payments': 'integration_payments',
    'expenses': 'finance_expenses',
    'budgets': 'finance_budgets',
    'payroll': 'finance_payroll',
    'financial_reports': 'finance_reports',
    'timetable': 'academic_timetable',
    'exams': 'academic_exams',
    'assignments': 'academic_assignments',
    'lesson_plans': 'academic_lessons',
    'custom_grading': 'academic_grading',
    'auto_comments': 'academic_comments',
    'promotions': 'academic_promotions',
    'rankings': 'academic_rankings',
}


def can_access_feature(session, school_id, feature_id):
    from school_manager.models.features import FeatureManager
    manager = FeatureManager(session, school_id)
    return manager.is_feature_enabled(school_id, feature_id)


def get_available_features(session, school_id):
    from school_manager.models.features import FeatureManager
    manager = FeatureManager(session, school_id)
    return manager.get_school_features(school_id)


def check_module_access(session, school_id, module_name):
    feature_id = FEATURE_MODULES.get(module_name)
    if not feature_id:
        return True
    return can_access_feature(session, school_id, feature_id)


def get_required_feature(module_name):
    """Get the feature ID required for a module"""
    return FEATURE_MODULES.get(module_name)

