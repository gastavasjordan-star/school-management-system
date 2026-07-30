"""
Hardware Fingerprinting & Licensing Module
Anti-piracy protection with machine lock
"""
import hashlib
import uuid
import platform
import os
from datetime import datetime
from cryptography.fernet import Fernet
import base64

class HardwareFingerprint:
    """Generate unique machine ID from hardware components"""
    
    @staticmethod
    def get_machine_id():
        """Generate a unique machine ID from hardware components"""
        components = []
        
        # Try to get CPU info
        try:
            if platform.system() == 'Windows':
                import wmi
                c = wmi.WMI()
                for processor in c.Win32_Processor():
                    components.append(processor.ProcessorId.strip())
                for board in c.Win32_BaseBoard():
                    components.append(board.SerialNumber.strip())
                for bios in c.Win32_BIOS():
                    components.append(bios.SerialNumber.strip())
            else:
                # Linux/Unix fallback
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.startswith('model name'):
                            components.append(line.split(':')[1].strip())
                with open('/sys/class/dmi/id/product_uuid', 'r') as f:
                    components.append(f.read().strip())
        except Exception as e:
            # Ultimate fallback using uuid
            components.append(str(uuid.getnode()))
        
        if not components:
            components.append(str(uuid.getnode()))
        
        # Create a deterministic hash
        combined = '|'.join(components)
        machine_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        return machine_hash.upper()[:32]
    
    @staticmethod
    def get_fingerprint_display():
        """Get formatted machine ID for display"""
        machine_id = HardwareFingerprint.get_machine_id()
        return '-'.join([machine_id[i:i+4] for i in range(0, len(machine_id), 4)])


class LicenseManager:
    """Manage software licensing and activation"""
    
    def __init__(self, db_session):
        self.session = db_session
        self.cipher = self._get_cipher()
    
    def _get_cipher(self):
        """Get encryption cipher with stored key"""
        key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.license.key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)
    
    def is_activated(self):
        """Check if software is activated for this machine"""
        from school_manager.models.database import License
        machine_id = HardwareFingerprint.get_machine_id()
        
        license = self.session.query(License).filter(
            License.machine_id == machine_id,
            License.is_active == True
        ).first()
        
        if not license:
            return False
        
        # Check expiry
        if license.expiry_date:
            if license.expiry_date < datetime.now().date():
                return False
        
        return True
    
    def get_activation_status(self):
        """Get detailed activation status"""
        from school_manager.models.database import License
        machine_id = HardwareFingerprint.get_machine_id()
        
        license = self.session.query(License).filter(
            License.machine_id == machine_id
        ).first()
        
        if not license:
            return {
                'activated': False,
                'message': 'No license found',
                'expiry_date': None,
                'client_name': None,
                'features': {}
            }
        
        # Parse features
        features = {}
        if license.features:
            for feature in license.features.split(','):
                if ':' in feature:
                    key, value = feature.split(':')
                    features[key] = bool(int(value))
        
        return {
            'activated': license.is_active and (not license.expiry_date or license.expiry_date >= datetime.now().date()),
            'message': 'Active' if license.is_active else 'License inactive',
            'expiry_date': license.expiry_date,
            'client_name': license.client_name,
            'features': features
        }
    
    def activate_license(self, license_key):
        """Activate software with a license key"""
        from school_manager.models.database import License
        
        # Decrypt the license key
        try:
            decrypted = self.cipher.decrypt(base64.b64decode(license_key)).decode()
            parts = decrypted.split('|')
            
            if len(parts) < 4:
                return False, "Invalid license key format"
            
            client_name = parts[0]
            expiry_str = parts[1]
            features = parts[2]
            verification = parts[3]
            
            # Verify checksum
            expected_verification = hashlib.sha256(f"{client_name}|{expiry_str}|{features}".encode()).hexdigest()[:8]
            if verification != expected_verification:
                return False, "License key verification failed"
            
            # Parse expiry date
            expiry_date = None
            if expiry_str and expiry_str != 'never':
                expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d').date()
            
            machine_id = HardwareFingerprint.get_machine_id()
            
            # Check if license already exists
            existing = self.session.query(License).filter(
                License.machine_id == machine_id
            ).first()
            
            if existing:
                existing.license_key = license_key
                existing.client_name = client_name
                existing.expiry_date = expiry_date
                existing.is_active = True
                existing.features = features
                existing.activated_at = datetime.utcnow()
            else:
                license = License(
                    license_key=license_key,
                    machine_id=machine_id,
                    client_name=client_name,
                    expiry_date=expiry_date,
                    is_active=True,
                    features=features,
                    activated_at=datetime.utcnow()
                )
                self.session.add(license)
            
            self.session.commit()
            return True, f"Successfully activated for {client_name}"
            
        except Exception as e:
            return False, f"Activation failed: {str(e)}"
    
    def generate_license_key(self, client_name, expiry_date=None, features=None):
        """Generate a new license key (Super Admin only)"""
        from school_manager.models.database import License
        
        expiry_str = expiry_date.strftime('%Y-%m-%d') if expiry_date else 'never'
        features_str = features or 'photo_processing:1,pdf_engine:1,email_letters:1,cloud_backup:1'
        
        verification = hashlib.sha256(f"{client_name}|{expiry_str}|{features_str}".encode()).hexdigest()[:8]
        data = f"{client_name}|{expiry_str}|{features_str}|{verification}"
        
        encrypted = base64.b64encode(self.cipher.encrypt(data.encode())).decode()
        return encrypted
    
    def get_feature_status(self, feature_name):
        """Check if a specific premium feature is enabled"""
        from school_manager.models.database import FeatureToggle
        
        status = self.get_activation_status()
        
        if not status['activated']:
            return False
        
        # Check if feature is enabled globally
        toggle = self.session.query(FeatureToggle).filter(
            FeatureToggle.feature_name == feature_name
        ).first()
        
        if toggle and not toggle.is_enabled:
            return False
        
        # Check license features
        if feature_name in status['features']:
            return status['features'][feature_name]
        
        # Default to enabled if not specified
        return True
    
    def set_feature_toggle(self, feature_name, enabled, display_name=None, description=None):
        """Enable or disable a premium feature (Super Admin only)"""
        from school_manager.models.database import FeatureToggle
        
        toggle = self.session.query(FeatureToggle).filter(
            FeatureToggle.feature_name == feature_name
        ).first()
        
        if toggle:
            toggle.is_enabled = enabled
            if display_name:
                toggle.display_name = display_name
            if description:
                toggle.description = description
        else:
            toggle = FeatureToggle(
                feature_name=feature_name,
                display_name=display_name or feature_name,
                description=description,
                is_enabled=enabled
            )
            self.session.add(toggle)
        
        self.session.commit()
        return True
    
    def get_all_features(self):
        """Get status of all premium features"""
        from school_manager.models.database import FeatureToggle
        
        status = self.get_activation_status()
        
        features = self.session.query(FeatureToggle).all()
        result = []
        
        for f in features:
            result.append({
                'name': f.feature_name,
                'display_name': f.display_name,
                'description': f.description,
                'is_enabled': f.is_enabled and status['activated'],
                'is_premium': f.is_premium
            })
        
        return result
