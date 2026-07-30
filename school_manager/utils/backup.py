"""
Hybrid Backup System - USB & Cloud Backup
"""
import os
import shutil
import json
import sqlite3
import threading
import schedule
import time
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import zipfile
from pathlib import Path


class BackupConfig:
    """Backup configuration manager"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.backup_config.json')
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load backup configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            'usb_enabled': True,
            'cloud_enabled': False,
            'schedule': 'weekly',  # daily, weekly, monthly
            'retention_days': 30,
            'google_drive_folder_id': None,
            'last_backup': None,
            'backup_history': []
        }
    
    def save_config(self):
        """Save backup configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_cipher(self):
        """Get encryption cipher"""
        key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.backup.key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)


class USBBackup:
    """USB Flash Drive Backup Manager"""
    
    # Common USB mount points
    USB_PATHS = [
        '/media/*/*',
        '/mnt/*',
        '/Volumes/*',
        'E:/',
        'F:/',
        'D:/Backup',
        'E:/SchoolBackups',
    ]
    
    def __init__(self, config, db_path):
        self.config = config
        self.db_path = db_path
        self.cipher = config.get_cipher()
    
    def detect_usb_drives(self):
        """Detect connected USB drives"""
        drives = []
        
        if os.name == 'nt':  # Windows
            import win32api
            try:
                drive_list = win32api.GetLogicalDrives()
                for i, bit in enumerate(drive_list):
                    if bit:
                        drive = chr(65 + i) + ':/'
                        try:
                            if os.path.exists(drive):
                                # Check if it's a removable drive
                                import win32file
                                drive_type = win32file.GetDriveType(drive)
                                if drive_type == 2:  # DRIVE_REMOVABLE
                                    drives.append(drive)
                        except:
                            pass
            except ImportError:
                # Fallback without win32api
                for letter in 'EFGHIJK':
                    drive = f"{letter}:/"
                    if os.path.exists(drive):
                        drives.append(drive)
        else:  # Unix/Linux/Mac
            for path in ['/media', '/mnt', '/Volumes']:
                if os.path.exists(path):
                    for item in os.listdir(path):
                        drives.append(os.path.join(path, item))
        
        return drives
    
    def backup_to_usb(self):
        """Create encrypted backup and save to USB drive"""
        # Detect USB drives
        usb_drives = self.detect_usb_drives()
        
        if not usb_drives:
            return False, "No USB drive detected"
        
        # Create backup
        backup_path, backup_size = self._create_encrypted_backup()
        
        if not backup_path:
            return False, "Failed to create backup"
        
        # Save to each detected USB drive
        saved_to = []
        for drive in usb_drives:
            try:
                backup_dir = os.path.join(drive, 'SchoolManagerBackups')
                os.makedirs(backup_dir, exist_ok=True)
                
                filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
                dest_path = os.path.join(backup_dir, filename)
                
                shutil.copy2(backup_path, dest_path)
                saved_to.append(dest_path)
                
                # Clean old backups on this drive
                self._clean_old_backups(backup_dir)
                
            except Exception as e:
                print(f"Failed to backup to {drive}: {e}")
                continue
        
        # Remove temp file
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        if saved_to:
            return True, f"Backup saved to {len(saved_to)} USB drive(s)"
        else:
            return False, "Failed to save to any USB drive"
    
    def _create_encrypted_backup(self):
        """Create encrypted SQLite backup"""
        try:
            # Create backup directory
            temp_dir = os.path.join(os.path.dirname(self.db_path), 'temp_backups')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create backup filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(temp_dir, f'backup_{timestamp}.db')
            
            # Close any existing connections to the database
            # Create backup using sqlite3
            conn = sqlite3.connect(self.db_path)
            backup_conn = sqlite3.connect(backup_file)
            conn.backup(backup_conn)
            backup_conn.close()
            conn.close()
            
            # Encrypt the backup
            encrypted_file = backup_file + '.enc'
            with open(backup_file, 'rb') as f:
                data = f.read()
            
            encrypted_data = self.cipher.encrypt(data)
            
            with open(encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Remove unencrypted backup
            os.remove(backup_file)
            
            return encrypted_file, len(encrypted_data)
        
        except Exception as e:
            print(f"Backup creation failed: {e}")
            return None, 0
    
    def _clean_old_backups(self, backup_dir, retention_days=None):
        """Remove old backups beyond retention period"""
        if retention_days is None:
            retention_days = self.config.get('retention_days', 30)
        
        cutoff = datetime.now() - timedelta(days=retention_days)
        
        for filename in os.listdir(backup_dir):
            if filename.startswith('backup_') and filename.endswith('.enc'):
                filepath = os.path.join(backup_dir, filename)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime < cutoff:
                    try:
                        os.remove(filepath)
                    except:
                        pass
    
    def restore_from_usb(self, backup_file):
        """Restore database from USB backup"""
        try:
            # Decrypt backup
            with open(backup_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Create temp file
            temp_db = self.db_path + '.tmp'
            with open(temp_db, 'wb') as f:
                f.write(decrypted_data)
            
            # Verify it's a valid SQLite database
            test_conn = sqlite3.connect(temp_db)
            test_conn.execute("SELECT 1")
            test_conn.close()
            
            # Create backup of current database
            if os.path.exists(self.db_path):
                current_backup = self.db_path + f'.pre_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                shutil.copy2(self.db_path, current_backup)
            
            # Replace current database
            shutil.move(temp_db, self.db_path)
            
            return True, "Restore completed successfully"
        
        except Exception as e:
            return False, f"Restore failed: {str(e)}"


class CloudBackup:
    """Google Drive Cloud Backup Manager"""
    
    def __init__(self, config, db_path):
        self.config = config
        self.db_path = db_path
        self.cipher = config.get_cipher()
        self.credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.gdrive_credentials.json')
    
    def is_configured(self):
        """Check if Google Drive is configured"""
        return (self.config.get('cloud_enabled') and 
                self.config.get('google_drive_folder_id') and 
                os.path.exists(self.credentials_path))
    
    def authenticate(self):
        """Authenticate with Google Drive API"""
        if not os.path.exists(self.credentials_path):
            return False, "Credentials file not found. Please configure Google Drive in settings."
        
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            creds = Credentials.from_authorized_user_file(self.credentials_path, SCOPES)
            
            if not creds or not creds.valid:
                return False, "Invalid credentials. Please re-authenticate."
            
            self.service = build('drive', 'v3', credentials=creds)
            return True, "Authenticated successfully"
        
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def backup_to_cloud(self):
        """Upload encrypted backup to Google Drive"""
        if not self.is_configured():
            return False, "Google Drive not configured"
        
        auth_result = self.authenticate()
        if not auth_result[0]:
            return auth_result
        
        try:
            # Create encrypted backup
            backup_path, backup_size = self._create_encrypted_backup()
            
            if not backup_path:
                return False, "Failed to create backup"
            
            # Upload to Google Drive
            from googleapiclient.http import MediaFileUpload
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"SchoolManager_Backup_{timestamp}.enc"
            
            file_metadata = {
                'name': filename,
                'parents': [self.config['google_drive_folder_id']]
            }
            
            media = MediaFileUpload(backup_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            # Remove temp file
            os.remove(backup_path)
            
            # Update last backup time
            self.config.config['last_backup'] = datetime.now().isoformat()
            self.config.save_config()
            
            return True, f"Backup uploaded to Google Drive (File ID: {file.get('id')})"
        
        except Exception as e:
            return False, f"Cloud backup failed: {str(e)}"
    
    def _create_encrypted_backup(self):
        """Create encrypted SQLite backup"""
        try:
            # Create backup using sqlite3
            conn = sqlite3.connect(self.db_path)
            backup_file = self.db_path + '.cloud_backup'
            backup_conn = sqlite3.connect(backup_file)
            conn.backup(backup_conn)
            backup_conn.close()
            conn.close()
            
            # Encrypt the backup
            encrypted_file = backup_file + '.enc'
            with open(backup_file, 'rb') as f:
                data = f.read()
            
            encrypted_data = self.cipher.encrypt(data)
            
            with open(encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Remove unencrypted backup
            os.remove(backup_file)
            
            return encrypted_file, len(encrypted_data)
        
        except Exception as e:
            print(f"Backup creation failed: {e}")
            return None, 0
    
    def list_cloud_backups(self):
        """List available cloud backups"""
        if not self.is_configured():
            return []
        
        auth_result = self.authenticate()
        if not auth_result[0]:
            return []
        
        try:
            results = self.service.files().list(
                q=f"'{self.config['google_drive_folder_id']}' in parents and name contains 'SchoolManager_Backup'",
                fields="files(id, name, createdTime, size)"
            ).execute()
            
            backups = []
            for f in results.get('files', []):
                backups.append({
                    'id': f['id'],
                    'name': f['name'],
                    'created': f.get('createdTime'),
                    'size': int(f.get('size', 0))
                })
            
            return sorted(backups, key=lambda x: x['created'], reverse=True)
        
        except Exception as e:
            print(f"Failed to list backups: {e}")
            return []
    
    def restore_from_cloud(self, file_id):
        """Restore database from Google Drive backup"""
        auth_result = self.authenticate()
        if not auth_result[0]:
            return auth_result
        
        try:
            # Download file
            from googleapiclient.http import MediaIoBaseDownload
            
            request = self.service.files().get_media(fileId=file_id)
            temp_file = os.path.join(os.path.dirname(self.db_path), 'temp_cloud_restore.enc')
            
            with open(temp_file, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
            
            # Decrypt
            with open(temp_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Create temp database
            temp_db = self.db_path + '.tmp'
            with open(temp_db, 'wb') as f:
                f.write(decrypted_data)
            
            # Verify it's valid
            test_conn = sqlite3.connect(temp_db)
            test_conn.execute("SELECT 1")
            test_conn.close()
            
            # Backup current database
            if os.path.exists(self.db_path):
                current_backup = self.db_path + f'.pre_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                shutil.copy2(self.db_path, current_backup)
            
            # Replace current database
            shutil.move(temp_db, self.db_path)
            
            # Clean up
            os.remove(temp_file)
            
            return True, "Restore completed successfully"
        
        except Exception as e:
            return False, f"Restore failed: {str(e)}"


class BackupManager:
    """Main backup manager coordinating USB and Cloud backups"""
    
    def __init__(self, db_path, db_session):
        self.db_path = db_path
        self.session = db_session
        self.config = BackupConfig()
        self.usb_backup = USBBackup(self.config, db_path)
        self.cloud_backup = CloudBackup(self.config, db_path)
        self._scheduler_thread = None
        self._running = False
    
    def backup(self, backup_type='all'):
        """Perform backup(s)"""
        results = {'usb': None, 'cloud': None}
        
        # USB backup
        if backup_type in ['all', 'usb'] and self.config.config.get('usb_enabled'):
            try:
                success, message = self.usb_backup.backup_to_usb()
                results['usb'] = {'success': success, 'message': message}
                self._log_backup('usb', success, message)
            except Exception as e:
                results['usb'] = {'success': False, 'message': str(e)}
        
        # Cloud backup
        if backup_type in ['all', 'cloud'] and self.config.config.get('cloud_enabled'):
            try:
                success, message = self.cloud_backup.backup_to_cloud()
                results['cloud'] = {'success': success, 'message': message}
                self._log_backup('cloud', success, message)
            except Exception as e:
                results['cloud'] = {'success': False, 'message': str(e)}
        
        return results
    
    def _log_backup(self, backup_type, success, message):
        """Log backup to database"""
        from school_manager.models.database import BackupRecord
        
        record = BackupRecord(
            backup_type=backup_type,
            status='completed' if success else 'failed',
            error_message=message if not success else None
        )
        self.session.add(record)
        self.session.commit()
    
    def restore(self, source, file_path=None, file_id=None):
        """Restore from backup"""
        if source == 'usb':
            if not file_path:
                return False, "No backup file specified"
            return self.usb_backup.restore_from_usb(file_path)
        
        elif source == 'cloud':
            if not file_id:
                return False, "No file ID specified"
            return self.cloud_backup.restore_from_cloud(file_id)
        
        return False, "Invalid backup source"
    
    def start_scheduler(self):
        """Start automatic backup scheduler"""
        if self._running:
            return
        
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop automatic backup scheduler"""
        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
    
    def _run_scheduler(self):
        """Run backup scheduler loop"""
        schedule_type = self.config.config.get('schedule', 'weekly')
        
        if schedule_type == 'daily':
            schedule.every().day.at("02:00").do(self.backup)
        elif schedule_type == 'weekly':
            schedule.every().monday.at("02:00").do(self.backup)
        elif schedule_type == 'monthly':
            schedule.every().month.do(self.backup)
        
        while self._running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def get_backup_status(self):
        """Get current backup status"""
        return {
            'usb_enabled': self.config.config.get('usb_enabled', True),
            'cloud_enabled': self.config.config.get('cloud_enabled', False),
            'schedule': self.config.config.get('schedule', 'weekly'),
            'last_backup': self.config.config.get('last_backup'),
            'scheduler_running': self._running
        }
    
    def configure(self, **kwargs):
        """Configure backup settings"""
        for key, value in kwargs.items():
            self.config.config[key] = value
        self.config.save_config()
    
    def detect_usb_for_restore(self):
        """Detect USB drives for restore operation"""
        return self.usb_backup.detect_usb_drives()
    
    def get_usb_backups(self, drive_path):
        """Get available backups on a USB drive"""
        backups = []
        backup_dir = os.path.join(drive_path, 'SchoolManagerBackups')
        
        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                if filename.startswith('backup_') and filename.endswith('.enc'):
                    filepath = os.path.join(backup_dir, filename)
                    backups.append({
                        'name': filename,
                        'path': filepath,
                        'date': datetime.fromtimestamp(os.path.getmtime(filepath)),
                        'size': os.path.getsize(filepath)
                    })
        
        return sorted(backups, key=lambda x: x['date'], reverse=True)
