"""
License Management Panel - Super Admin Control Center
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                              QPushButton, QLineEdit, QComboBox, QTableWidget, 
                              QTableWidgetItem, QGroupBox, QCheckBox, QSpinBox,
                              QDateEdit, QTextEdit, QMessageBox, QDialog, QTabWidget,
                              QFormLayout)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime, timedelta


class LicenseGeneratorDialog(QDialog):
    """Dialog for generating new license keys"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate License Key")
        self.setMinimumSize(500, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Client Information
        info_group = QGroupBox("Client Information")
        info_layout = QFormLayout()
        
        self.client_name = QLineEdit()
        self.client_name.setPlaceholderText("School Name")
        info_layout.addRow("School Name:", self.client_name)
        
        self.billing_email = QLineEdit()
        self.billing_email.setPlaceholderText("billing@school.com")
        info_layout.addRow("Billing Email:", self.billing_email)
        
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(60)
        info_layout.addRow("Notes:", self.notes)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Subscription Tier
        tier_group = QGroupBox("Subscription Tier")
        tier_layout = QVBoxLayout()
        
        self.tier_combo = QComboBox()
        self.tier_combo.addItems([
            "🥉 Bronze - $49/mo (100 students, 5 classes)",
            "🥈 Silver - $149/mo (500 students, 15 classes)",
            "🥇 Gold - $299/mo (2000 students, 50 classes)",
            "💎 Platinum - $499/mo (Unlimited)"
        ])
        tier_layout.addWidget(self.tier_combo)
        
        self.tier_info = QLabel()
        self.tier_info.setStyleSheet("color: #64748b; font-size: 12px;")
        tier_layout.addWidget(self.tier_info)
        
        tier_group.setLayout(tier_layout)
        layout.addWidget(tier_group)
        
        # Custom Limits
        limits_group = QGroupBox("Custom Limits (Optional)")
        limits_layout = QFormLayout()
        
        self.max_students = QSpinBox()
        self.max_students.setRange(-1, 999999)
        self.max_students.setValue(-1)
        self.max_students.setSpecialValueText("Unlimited")
        limits_layout.addRow("Max Students:", self.max_students)
        
        self.max_staff = QSpinBox()
        self.max_staff.setRange(-1, 9999)
        self.max_staff.setValue(-1)
        self.max_staff.setSpecialValueText("Unlimited")
        limits_layout.addRow("Max Staff:", self.max_staff)
        
        self.max_classes = QSpinBox()
        self.max_classes.setRange(-1, 999)
        self.max_classes.setValue(-1)
        self.max_classes.setSpecialValueText("Unlimited")
        limits_layout.addRow("Max Classes:", self.max_classes)
        
        self.terms_included = QSpinBox()
        self.terms_included.setRange(1, 12)
        self.terms_included.setValue(3)
        limits_layout.addRow("Terms Included:", self.terms_included)
        
        limits_group.setLayout(limits_layout)
        layout.addWidget(limits_group)
        
        # Expiry Date
        expiry_group = QGroupBox("License Validity")
        expiry_layout = QHBoxLayout()
        
        expiry_layout.addWidget(QLabel("Expiry Date:"))
        
        self.expiry_date = QDateEdit()
        self.expiry_date.setDate(QDate.currentDate().addMonths(12))
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setMinimumDate(QDate.currentDate())
        expiry_layout.addWidget(self.expiry_date)
        
        self.auto_renew = QCheckBox("Auto-Renew")
        expiry_layout.addWidget(self.auto_renew)
        expiry_layout.addStretch()
        
        expiry_group.setLayout(expiry_layout)
        layout.addWidget(expiry_group)
        
        # Features
        features_group = QGroupBox("Features")
        features_layout = QVBoxLayout()
        
        self.feature_checkboxes = {}
        features = [
            ("student_photos", "Student Photo Processing"),
            ("id_card_generator", "ID Card Generator"),
            ("pdf_branding", "Custom PDF Branding"),
            ("email_letters", "Email Fee Letters"),
            ("cloud_backup", "Cloud Backup"),
            ("parent_portal", "Parent Portal"),
            ("analytics_dashboard", "Analytics Dashboard"),
            ("advanced_reports", "Advanced Reports"),
            ("library_module", "Library Module"),
            ("medical_records", "Medical Records"),
            ("disciplinary_tracking", "Disciplinary Tracking"),
            ("payroll_module", "Payroll Module"),
            ("custom_branding", "White Label Branding"),
        ]
        
        for feat_id, feat_name in features:
            cb = QCheckBox(feat_name)
            cb.setChecked(True)
            self.feature_checkboxes[feat_id] = cb
            features_layout.addWidget(cb)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("🔑 Generate License")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a34a;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #15803d; }
        """)
        self.generate_btn.clicked.connect(self.generate)
        btn_layout.addWidget(self.generate_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def generate(self):
        if not self.client_name.text().strip():
            QMessageBox.warning(self, "Error", "Please enter school name")
            return
        
        tier_map = {
            0: 'bronze',
            1: 'silver',
            2: 'gold',
            3: 'platinum'
        }
        
        tier = tier_map[self.tier_combo.currentIndex()]
        
        custom_features = {}
        for feat_id, cb in self.feature_checkboxes.items():
            custom_features[feat_id] = cb.isChecked()
        
        from school_manager.utils.licensing import LicenseKeyGenerator
        generator = LicenseKeyGenerator()
        
        expiry = self.expiry_date.date().toPyDate()
        
        key, data = generator.generate(
            client_name=self.client_name.text().strip(),
            tier=tier,
            expiry_date=expiry,
            terms=self.terms_included.value(),
            max_students=self.max_students.value() if self.max_students.value() > 0 else None,
            max_staff=self.max_staff.value() if self.max_staff.value() > 0 else None,
            max_classes=self.max_classes.value() if self.max_classes.value() > 0 else None,
            custom_features=custom_features
        )
        
        self.generated_key = key
        self.generated_data = data
        
        # Show result
        QMessageBox.information(
            self, 
            "License Generated",
            f"<b>License Key for {self.client_name.text()}:</b><br><br>"
            f"<code style='font-size: 11px;'>{key}</code><br><br>"
            f"<b>Tier:</b> {tier.title()}<br>"
            f"<b>Students:</b> {data['max_students']}<br>"
            f"<b>Staff:</b> {data['max_staff']}<br>"
            f"<b>Expiry:</b> {data['expiry']}<br><br>"
            f"<small>Copy this key and send to the client.</small>"
        )
        
        self.accept()


class LicenseManagementPanel(QWidget):
    """License management panel for Super Admin"""
    
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setup_ui()
        self.load_licenses()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("🔐 License Management")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        layout.addWidget(header)
        
        subtitle = QLabel("Manage subscription licenses and track usage")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")
        layout.addWidget(subtitle)
        
        # Tabs
        tabs = QTabWidget()
        
        # Licenses Tab
        licenses_tab = QWidget()
        licenses_layout = QVBoxLayout(licenses_tab)
        
        # Actions
        actions_layout = QHBoxLayout()
        
        generate_btn = QPushButton("➕ Generate New License")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1e40af; }
        """)
        generate_btn.clicked.connect(self.generate_license)
        actions_layout.addWidget(generate_btn)
        
        validate_btn = QPushButton("✓ Validate Key")
        validate_btn.clicked.connect(self.validate_key)
        actions_layout.addWidget(validate_btn)
        
        actions_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_licenses)
        actions_layout.addWidget(refresh_btn)
        
        licenses_layout.addLayout(actions_layout)
        
        # Licenses table
        self.licenses_table = QTableWidget()
        self.licenses_table.setColumnCount(7)
        self.licenses_table.setHorizontalHeaderLabels([
            "Client", "Tier", "Students", "Staff", "Expiry", "Status", "Actions"
        ])
        licenses_layout.addWidget(self.licenses_table)
        
        tabs.addTab(licenses_tab, "📋 All Licenses")
        
        # Usage Tab
        usage_tab = QWidget()
        usage_layout = QVBoxLayout(usage_tab)
        
        usage_info = QLabel("Current Installation Usage:")
        usage_info.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        usage_layout.addWidget(usage_info)
        
        self.usage_table = QTableWidget()
        self.usage_table.setColumnCount(3)
        self.usage_table.setHorizontalHeaderLabels(["Entity", "Current Count", "License Limit"])
        usage_layout.addWidget(self.usage_table)
        
        tabs.addTab(usage_tab, "📊 Usage")
        
        # Plans Tab
        plans_tab = QWidget()
        plans_layout = QVBoxLayout(plans_tab)
        
        plans_header = QLabel("Subscription Plans")
        plans_header.setStyleSheet("font-size: 16px; font-weight: bold;")
        plans_layout.addWidget(plans_header)
        
        self.plans_table = QTableWidget()
        self.plans_table.setColumnCount(6)
        self.plans_table.setHorizontalHeaderLabels([
            "Plan", "Students", "Classes", "Staff", "Monthly", "Annual"
        ])
        self.load_plans()
        plans_layout.addWidget(self.plans_table)
        
        tabs.addTab(plans_tab, "💰 Plans")
        
        layout.addWidget(tabs)
    
    def load_licenses(self):
        from school_manager.models.database import License
        
        licenses = self.session.query(License).order_by(License.created_at.desc()).all()
        
        self.licenses_table.setRowCount(len(licenses))
        
        for row, lic in enumerate(licenses):
            self.licenses_table.setItem(row, 0, QTableWidgetItem(lic.client_name or "N/A"))
            self.licenses_table.setItem(row, 1, QTableWidgetItem(lic.tier or "N/A"))
            self.licenses_table.setItem(row, 2, QTableWidgetItem(str(lic.max_students)))
            self.licenses_table.setItem(row, 3, QTableWidgetItem(str(lic.max_staff)))
            self.licenses_table.setItem(row, 4, QTableWidgetItem(
                str(lic.expiry_date) if lic.expiry_date else "Never"
            ))
            
            # Status
            status = "Active"
            if lic.expiry_date and lic.expiry_date < datetime.now().date():
                status = "Expired"
            elif not lic.is_active:
                status = "Inactive"
            
            status_item = QTableWidgetItem(status)
            if status == "Active":
                status_item.setBackground(Qt.GlobalColor.green)
            elif status == "Expired":
                status_item.setBackground(Qt.GlobalColor.red)
            self.licenses_table.setItem(row, 5, status_item)
            
            # Actions
            actions = QLabel("<a href='#'>View</a> | <a href='#'>Edit</a>")
            self.licenses_table.setCellWidget(row, 6, actions)
    
    def load_plans(self):
        from school_manager.utils.licensing import SubscriptionPlan
        
        tiers = SubscriptionPlan.get_all_tiers()
        self.plans_table.setRowCount(len(tiers))
        
        tier_display = {
            'bronze': '🥉 Bronze',
            'silver': '🥈 Silver',
            'gold': '🥇 Gold',
            'platinum': '💎 Platinum'
        }
        
        for row, tier in enumerate(tiers):
            plan = SubscriptionPlan.get_plan_features(tier)
            
            self.plans_table.setItem(row, 0, QTableWidgetItem(tier_display.get(tier, tier)))
            self.plans_table.setItem(row, 1, QTableWidgetItem(
                str(plan['max_students']) if plan['max_students'] > 0 else "Unlimited"
            ))
            self.plans_table.setItem(row, 2, QTableWidgetItem(
                str(plan['max_classes']) if plan['max_classes'] > 0 else "Unlimited"
            ))
            self.plans_table.setItem(row, 3, QTableWidgetItem(
                str(plan['max_staff']) if plan['max_staff'] > 0 else "Unlimited"
            ))
            self.plans_table.setItem(row, 4, QTableWidgetItem(f"${plan['price_monthly']}"))
            self.plans_table.setItem(row, 5, QTableWidgetItem(f"${plan['price_annual']}"))
    
    def generate_license(self):
        dialog = LicenseGeneratorDialog(self)
        dialog.exec()
        self.load_licenses()
    
    def validate_key(self):
        from PyQt6.QtWidgets import QInputDialog
        from school_manager.utils.licensing import LicenseKeyGenerator
        
        key, ok = QInputDialog.getMultiLineText(
            self, "Validate License", "Paste license key:"
        )
        
        if ok and key.strip():
            generator = LicenseKeyGenerator()
            valid, data, msg = generator.validate(key.strip())
            
            if valid:
                QMessageBox.information(
                    self, "Valid License",
                    f"✓ License is valid!\n\n"
                    f"Client: {data.get('client_name')}\n"
                    f"Tier: {data.get('tier', 'N/A')}\n"
                    f"Students: {data.get('max_students')}\n"
                    f"Staff: {data.get('max_staff')}\n"
                    f"Expiry: {data.get('expiry')}"
                )
            else:
                QMessageBox.warning(self, "Invalid License", f"✗ {msg}")
