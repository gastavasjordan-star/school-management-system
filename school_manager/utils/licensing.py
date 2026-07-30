"""
Enhanced Subscription Licensing System
Pay-per-term licensing with tiered plans
"""
import hashlib
import uuid
import base64
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet


class SubscriptionPlan:
    """Subscription tier definitions"""
    
    # Tier levels
    TIER_BRONZE = 'bronze'
    TIER_SILVER = 'silver'
    TIER_GOLD = 'gold'
    TIER_PLATINUM = 'platinum'
    
    @classmethod
    def get_plan_features(cls, tier):
        """Get features for each subscription tier"""
        features = {
            cls.TIER_BRONZE: {
                'max_students': 100,
                'max_staff': 20,
                'max_classes': 5,
                'features': {
                    'student_photos': False,
                    'id_card_generator': False,
                    'pdf_branding': False,
                    'email_letters': False,
                    'cloud_backup': False,
                    'parent_portal': False,
                    'analytics_dashboard': False,
                    'advanced_reports': False,
                    'multi_term': False,
                    'library_module': False,
                    'medical_records': False,
                    'disciplinary_tracking': False,
                    'payroll_module': False,
                    'custom_branding': False,
                },
                'support_level': 'email',
                'price_monthly': 49,
                'price_annual': 470,
            },
            cls.TIER_SILVER: {
                'max_students': 500,
                'max_staff': 50,
                'max_classes': 15,
                'features': {
                    'student_photos': True,
                    'id_card_generator': True,
                    'pdf_branding': True,
                    'email_letters': False,
                    'cloud_backup': False,
                    'parent_portal': True,
                    'analytics_dashboard': True,
                    'advanced_reports': False,
                    'multi_term': True,
                    'library_module': True,
                    'medical_records': True,
                    'disciplinary_tracking': True,
                    'payroll_module': False,
                    'custom_branding': False,
                },
                'support_level': 'email',
                'price_monthly': 149,
                'price_annual': 1430,
            },
            cls.TIER_GOLD: {
                'max_students': 2000,
                'max_staff': 150,
                'max_classes': 50,
                'features': {
                    'student_photos': True,
                    'id_card_generator': True,
                    'pdf_branding': True,
                    'email_letters': True,
                    'cloud_backup': True,
                    'parent_portal': True,
                    'analytics_dashboard': True,
                    'advanced_reports': True,
                    'multi_term': True,
                    'library_module': True,
                    'medical_records': True,
                    'disciplinary_tracking': True,
                    'payroll_module': True,
                    'custom_branding': True,
                },
                'support_level': 'priority',
                'price_monthly': 299,
                'price_annual': 2870,
            },
            cls.TIER_PLATINUM: {
                'max_students': -1,  # Unlimited
                'max_staff': -1,
                'max_classes': -1,
                'features': {
                    'student_photos': True,
                    'id_card_generator': True,
                    'pdf_branding': True,
                    'email_letters': True,
                    'cloud_backup': True,
                    'parent_portal': True,
                    'analytics_dashboard': True,
                    'advanced_reports': True,
                    'multi_term': True,
                    'library_module': True,
                    'medical_records': True,
                    'disciplinary_tracking': True,
                    'payroll_module': True,
                    'custom_branding': True,
                },
                'support_level': 'dedicated',
                'price_monthly': 499,
                'price_annual': 4790,
            }
        }
        return features.get(tier, features[cls.TIER_BRONZE])
    
    @classmethod
    def get_all_tiers(cls):
        """Get all available tiers"""
        return [cls.TIER_BRONZE, cls.TIER_SILVER, cls.TIER_GOLD, cls.TIER_PLATINUM]
    
    @classmethod
    def get_tier_display_name(cls, tier):
        """Get display name for tier"""
        names = {
            cls.TIER_BRONZE: '🥉 Bronze',
            cls.TIER_SILVER: '🥈 Silver',
            cls.TIER_GOLD: '🥇 Gold',
            cls.TIER_PLATINUM: '💎 Platinum',
        }
        return names.get(tier, tier.title())


class SubscriptionLicenseManager:
    """
    Advanced subscription-based licensing system
    Generates and validates tiered subscription licenses
    """
    
    def __init__(self, db_session):
        self.session = db_session
        self.cipher = self._get_cipher()
    
    def _get_cipher(self):
        """Get encryption cipher with stored key"""
        import os
        key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.license.key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)
    
    def generate_license_key(self, client_info):
        """
        Generate a subscription license key
        
        client_info = {
            'client_name': 'School Name',
            'tier': 'gold',
            'expiry_date': datetime(2025, 12, 31),
            'max_students': 500,  # Override tier default
            'max_staff': 50,
            'custom_features': {...},  # Override tier features
            'terms_included': 3,  # Number of terms per year
        }
        """
        tier = client_info.get('tier', SubscriptionPlan.TIER_BRONZE)
        plan = SubscriptionPlan.get_plan_features(tier)
        
        # Merge custom values with tier defaults
        max_students = client_info.get('max_students', plan['max_students'])
        max_staff = client_info.get('max_staff', plan['max_staff'])
        max_classes = client_info.get('max_classes', plan['max_classes'])
        features = {**plan['features'], **client_info.get('custom_features', {})}
        terms_included = client_info.get('terms_included', 3)
        
        expiry_date = client_info.get('expiry_date')
        expiry_str = expiry_date.strftime('%Y-%m-%d') if expiry_date else 'never'
        
        # Build license data
        data = {
            'client_name': client_info['client_name'],
            'tier': tier,
            'expiry': expiry_str,
            'max_students': max_students,
            'max_staff': max_staff,
            'max_classes': max_classes,
            'terms_included': terms_included,
            'features': features,
            'created': datetime.now().isoformat(),
        }
        
        # Create checksum
        data_str = json.dumps(data, sort_keys=True)
        checksum = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        data['checksum'] = checksum
        
        # Encrypt the license
        json_data = json.dumps(data)
        encrypted = base64.b64encode(self.cipher.encrypt(json_data.encode())).decode()
        
        # Format as readable key (XXXX-XXXX-XXXX-XXXX)
        chunks = [encrypted[i:i+4] for i in range(0, len(encrypted), 4)]
        formatted_key = '-'.join(chunks[:16])
        
        return formatted_key, data
    
    def validate_license_key(self, license_key):
        """
        Validate and parse a license key
        Returns: (is_valid, data_dict, error_message)
        """
        try:
            # Remove formatting
            clean_key = license_key.replace('-', '')
            
            # Try to decode
            decrypted = self.cipher.decrypt(base64.b64decode(clean_key)).decode()
            data = json.loads(decrypted)
            
            # Verify checksum
            data_copy = {k: v for k, v in data.items() if k != 'checksum'}
            expected_checksum = hashlib.sha256(
                json.dumps(data_copy, sort_keys=True).encode()
            ).hexdigest()[:16]
            
            if data.get('checksum') != expected_checksum:
                return False, None, "License checksum verification failed"
            
            # Check expiry
            expiry_str = data.get('expiry', 'never')
            if expiry_str != 'never':
                expiry = datetime.strptime(expiry_str, '%Y-%m-%d').date()
                if expiry < datetime.now().date():
                    return False, data, f"License expired on {expiry_str}"
            
            return True, data, "Valid"
        
        except Exception as e:
            return False, None, f"Invalid license key: {str(e)}"
    
    def activate_license(self, license_key):
        """Activate a license and store in database"""
        from school_manager.models.database import License, FeatureToggle
        
        is_valid, data, msg = self.validate_license_key(license_key)
        
        if not is_valid:
            return False, msg
        
        # Store license
        from school_manager.utils.hardware import HardwareFingerprint
        machine_id = HardwareFingerprint.get_machine_id()
        
        # Check if already activated
        existing = self.session.query(License).filter(
            License.machine_id == machine_id
        ).first()
        
        features_json = json.dumps(data['features'])
        expiry_date = None
        if data['expiry'] != 'never':
            expiry_date = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
        
        if existing:
            existing.license_key = license_key
            existing.client_name = data['client_name']
            existing.tier = data['tier']
            existing.expiry_date = expiry_date
            existing.is_active = True
            existing.features = features_json
            existing.max_students = data['max_students']
            existing.max_staff = data['max_staff']
            existing.max_classes = data['max_classes']
            existing.terms_included = data.get('terms_included', 3)
            existing.activated_at = datetime.utcnow()
        else:
            license = License(
                license_key=license_key,
                machine_id=machine_id,
                client_name=data['client_name'],
                tier=data['tier'],
                expiry_date=expiry_date,
                is_active=True,
                features=features_json,
                max_students=data['max_students'],
                max_staff=data['max_staff'],
                max_classes=data['max_classes'],
                terms_included=data.get('terms_included', 3),
                activated_at=datetime.utcnow()
            )
            self.session.add(license)
        
        # Update feature toggles
        for feature_name, enabled in data['features'].items():
            toggle = self.session.query(FeatureToggle).filter(
                FeatureToggle.feature_name == feature_name
            ).first()
            
            if toggle:
                toggle.is_enabled = enabled
            else:
                toggle = FeatureToggle(
                    feature_name=feature_name,
                    display_name=feature_name.replace('_', ' ').title(),
                    is_enabled=enabled,
                    is_premium=True
                )
                self.session.add(toggle)
        
        self.session.commit()
        return True, f"Activated {SubscriptionPlan.get_tier_display_name(data['tier'])} subscription"
    
    def get_subscription_status(self):
        """Get current subscription status"""
        from school_manager.models.database import License
        from school_manager.utils.hardware import HardwareFingerprint
        
        machine_id = HardwareFingerprint.get_machine_id()
        license = self.session.query(License).filter(
            License.machine_id == machine_id,
            License.is_active == True
        ).first()
        
        if not license:
            return {
                'activated': False,
                'tier': None,
                'tier_display': 'None',
                'message': 'No active subscription',
                'features': {},
                'limits': {},
                'expiry_date': None,
            }
        
        # Check expiry
        expired = False
        if license.expiry_date and license.expiry_date < datetime.now().date():
            expired = True
        
        features = json.loads(license.features) if license.features else {}
        plan = SubscriptionPlan.get_plan_features(license.tier)
        
        return {
            'activated': not expired,
            'tier': license.tier,
            'tier_display': SubscriptionPlan.get_tier_display_name(license.tier),
            'message': 'Active' if not expired else 'Expired',
            'client_name': license.client_name,
            'features': features,
            'limits': {
                'max_students': license.max_students,
                'max_staff': license.max_staff,
                'max_classes': license.max_classes,
                'terms_included': license.terms_included,
            },
            'expiry_date': license.expiry_date,
            'days_remaining': (license.expiry_date - datetime.now().date()).days if license.expiry_date else None,
        }
    
    def check_feature_access(self, feature_name):
        """Check if a feature is accessible under current subscription"""
        status = self.get_subscription_status()
        
        if not status['activated']:
            return False
        
        return status['features'].get(feature_name, False)
    
    def check_limits(self, entity_type, current_count):
        """Check if current usage exceeds subscription limits"""
        status = self.get_subscription_status()
        
        if not status['activated']:
            return False, "No active subscription"
        
        limits = status['limits']
        limit = limits.get(f'max_{entity_type}', -1)
        
        if limit == -1:  # Unlimited
            return True, "OK"
        
        if current_count >= limit:
            return False, f"Limit reached ({current_count}/{limit})"
        
        return True, f"{current_count}/{limit}"
    
    def is_within_term_limit(self, terms_published):
        """Check if school is within their allowed terms per year"""
        status = self.get_subscription_status()
        
        if not status['activated']:
            return False, "No active subscription"
        
        limit = status['limits'].get('terms_included', 0)
        
        if terms_published >= limit:
            return False, f"Term limit reached ({terms_published}/{limit})"
        
        return True, f"{terms_published}/{limit} terms used"


class LicenseKeyGenerator:
    """Admin tool for generating license keys (CLI/API)"""
    
    def __init__(self):
        self.cipher = self._get_cipher()
    
    def _get_cipher(self):
        import os
        key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.license.key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)
    
    def generate(self, client_name, tier, expiry_date=None, terms=3, 
                 max_students=None, max_staff=None, max_classes=None,
                 custom_features=None):
        """Generate a license key for a client"""
        manager = SubscriptionLicenseManager(None)
        
        client_info = {
            'client_name': client_name,
            'tier': tier,
            'expiry_date': expiry_date,
            'terms_included': terms,
            'custom_features': custom_features or {},
        }
        
        if max_students:
            client_info['max_students'] = max_students
        if max_staff:
            client_info['max_staff'] = max_staff
        if max_classes:
            client_info['max_classes'] = max_classes
        
        return manager.generate_license_key(client_info)
    
    def validate(self, license_key):
        """Validate a license key without activation"""
        manager = SubscriptionLicenseManager(None)
        return manager.validate_license_key(license_key)
    
    def generate_demo_key(self):
        """Generate a demo key for testing"""
        return self.generate(
            client_name='Demo School',
            tier=SubscriptionPlan.TIER_BRONZE,
            expiry_date=datetime.now() + timedelta(days=30),
            terms=1,
            max_students=20,
            max_staff=5,
            max_classes=2
        )


# Quick CLI for generating licenses
if __name__ == '__main__':
    import sys
    
    generator = LicenseKeyGenerator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'generate':
            client = sys.argv[2] if len(sys.argv) > 2 else 'Test School'
            tier = sys.argv[3] if len(sys.argv) > 3 else 'gold'
            days = int(sys.argv[4]) if len(sys.argv) > 4 else 365
            
            key, data = generator.generate(
                client_name=client,
                tier=tier,
                expiry_date=datetime.now() + timedelta(days=days),
                terms=3
            )
            
            print(f"\n{'='*60}")
            print(f"License Key Generated")
            print(f"{'='*60}")
            print(f"Client: {data['client_name']}")
            print(f"Tier: {SubscriptionPlan.get_tier_display_name(data['tier'])}")
            print(f"Expiry: {data['expiry']}")
            print(f"Students: {data['max_students']}")
            print(f"Staff: {data['max_staff']}")
            print(f"Classes: {data['max_classes']}")
            print(f"\nLicense Key:\n{key}")
            print(f"{'='*60}\n")
        
        elif command == 'validate':
            key = sys.argv[2] if len(sys.argv) > 2 else ''
            if key:
                valid, data, msg = generator.validate(key)
                print(f"Valid: {valid}")
                print(f"Message: {msg}")
                if data:
                    print(f"Client: {data.get('client_name')}")
                    print(f"Tier: {data.get('tier')}")
        
        elif command == 'demo':
            key, data = generator.generate_demo_key()
            print(f"\nDemo License Key:\n{key}\n")
        
        else:
            print("Usage: python licensing.py [generate|validate|demo]")
    else:
        print("""
School Manager License Generator
-------------------------------
Usage:
  python licensing.py generate [client_name] [tier] [days]
  python licensing.py validate [license_key]
  python licensing.py demo

Examples:
  python licensing.py generate "My School" gold 365
  python licensing.py generate "Trial" bronze 30
  python licensing.py demo
""")
