"""
Super Admin Feature Control Panel
Manage which features each school can access
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                              QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
                              QGroupBox, QCheckBox, QScrollArea, QFrame, QDialog,
                              QListWidget, QListWidgetItem, QProgressBar, QMessageBox,
                              QTabWidget, QLineEdit, QSpinBox, QTextEdit, QSplitter)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont


class FeatureControlPanel(QWidget):
    """
    Super Admin Feature Management Panel
    Control which features each school can access
    """
    
    def __init__(self, session, auth, parent=None):
        super().__init__(parent)
        self.session = session
        self.auth = auth
        self.setup_ui()
        self.load_schools()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("🎛️ Feature Control Center")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #0f172a;")
        layout.addWidget(header)
        
        subtitle = QLabel("Super Admin: Control which features each school can access")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")
        layout.addWidget(subtitle)
        
        # School selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select School:"))
        
        self.school_combo = QComboBox()
        self.school_combo.setMinimumWidth(300)
        self.school_combo.currentIndexChanged.connect(self.on_school_changed)
        selector_layout.addWidget(self.school_combo)
        
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Main content - splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: School info and stats
        left_panel = self.create_school_info_panel()
        splitter.addWidget(left_panel)
        
        # Right: Feature categories
        right_panel = self.create_features_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
    
    def create_school_info_panel(self):
        """Create school info panel"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        # School name
        self.school_name_label = QLabel("Select a School")
        self.school_name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0f172a;")
        layout.addWidget(self.school_name_label)
        
        # Subscription info
        sub_group = QGroupBox("Subscription")
        sub_layout = QVBoxLayout()
        
        self.tier_label = QLabel("Tier: -")
        sub_layout.addWidget(self.tier_label)
        
        self.expiry_label = QLabel("Expiry: -")
        sub_layout.addWidget(self.expiry_label)
        
        self.students_label = QLabel("Students: -")
        sub_layout.addWidget(self.students_label)
        
        self.staff_label = QLabel("Staff: -")
        sub_layout.addWidget(self.staff_label)
        
        sub_group.setLayout(sub_layout)
        layout.addWidget(sub_group)
        
        # Usage stats
        usage_group = QGroupBox("Current Usage")
        usage_layout = QVBoxLayout()
        
        self.usage_students = QProgressBar()
        self.usage_students.setMaximumHeight(20)
        usage_layout.addWidget(QLabel("Students:"))
        usage_layout.addWidget(self.usage_students)
        
        self.usage_staff = QProgressBar()
        self.usage_staff.setMaximumHeight(20)
        usage_layout.addWidget(QLabel("Staff:"))
        usage_layout.addWidget(self.usage_staff)
        
        self.usage_classes = QProgressBar()
        self.usage_classes.setMaximumHeight(20)
        usage_layout.addWidget(QLabel("Classes:"))
        usage_layout.addWidget(self.usage_classes)
        
        usage_group.setLayout(usage_layout)
        layout.addWidget(usage_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout()
        
        enable_all_btn = QPushButton("✓ Enable All Tier Features")
        enable_all_btn.clicked.connect(self.enable_all_tier_features)
        actions_layout.addWidget(enable_all_btn)
        
        disable_premium_btn = QPushButton("✗ Disable All Premium")
        disable_premium_btn.clicked.connect(self.disable_all_premium)
        actions_layout.addWidget(disable_premium_btn)
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        actions_layout.addWidget(reset_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
        
        return frame
    
    def create_features_panel(self):
        """Create features categories panel"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        # Feature categories tabs
        self.feature_tabs = QTabWidget()
        
        categories = [
            ('core', '🔧 Core'),
            ('academic', '📚 Academic'),
            ('finance', '💰 Finance'),
            ('admin', '⚙️ Admin'),
            ('portal', '📱 Portals'),
            ('analytics', '📊 Analytics'),
            ('integration', '🔗 Integration'),
            ('premium', '💎 Premium'),
        ]
        
        for cat_id, cat_name in categories:
            tab = self.create_category_tab(cat_id)
            self.feature_tabs.addTab(tab, cat_name)
        
        layout.addWidget(self.feature_tabs)
        
        scroll.setWidget(container)
        return scroll
    
    def create_category_tab(self, category):
        """Create a category feature tab"""
        from school_manager.models.features import FeatureRegistry
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # Category header
        features = FeatureRegistry.get_all_features()
        cat_features = {k: v for k, v in features.items() if v['category'] == category}
        
        # Enable/Disable all in category
        header_layout = QHBoxLayout()
        
        cat_name = FeatureRegistry.get_category_display_name(category)
        header = QLabel(cat_name)
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        enable_all = QPushButton("Enable All")
        enable_all.setStyleSheet("padding: 5px 15px; background: #16a34a; color: white; border: none; border-radius: 5px;")
        enable_all.clicked.connect(lambda: self.enable_category(category))
        header_layout.addWidget(enable_all)
        
        disable_all = QPushButton("Disable All")
        disable_all.setStyleSheet("padding: 5px 15px; background: #dc2626; color: white; border: none; border-radius: 5px;")
        disable_all.clicked.connect(lambda: self.disable_category(category))
        header_layout.addWidget(disable_all)
        
        layout.addLayout(header_layout)
        
        # Feature cards
        for feat_id, feat_data in cat_features.items():
            card = self.create_feature_card(feat_id, feat_data)
            layout.addWidget(card)
        
        layout.addStretch()
        return widget
    
    def create_feature_card(self, feature_id, feature_data):
        """Create a feature toggle card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
            }
            QFrame:hover {
                border-color: #2563eb;
            }
        """)
        layout = QHBoxLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Icon
        icon = QLabel(feature_data.get('icon', '📦'))
        icon.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon)
        
        # Info
        info_layout = QVBoxLayout()
        
        name = QLabel(feature_data['name'])
        name.setStyleSheet("font-size: 14px; font-weight: 600; color: #0f172a;")
        info_layout.addWidget(name)
        
        desc = QLabel(feature_data['description'])
        desc.setStyleSheet("font-size: 11px; color: #64748b;")
        info_layout.addWidget(desc)
        
        # Tier badge
        tier = feature_data.get('default_tier', 'core')
        if tier is None:
            tier_text = "Always"
            tier_color = "#16a34a"
        else:
            tier_text = tier.upper()
            tier_color = {
                'bronze': '#cd7f32',
                'silver': '#c0c0c0',
                'gold': '#ffd700',
                'platinum': '#e5e4e2',
            }.get(tier, '#64748b')
        
        tier_label = QLabel(f" {tier_text} ")
        tier_label.setStyleSheet(f"""
            background-color: {tier_color};
            color: {'white' if tier in ['gold', 'platinum'] else 'black'};
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: bold;
        """)
        info_layout.addWidget(tier_label)
        
        layout.addLayout(info_layout)
        
        # Toggle
        checkbox = QCheckBox()
        checkbox.setObjectName(feature_id)
        checkbox.stateChanged.connect(lambda s, fid=feature_id: self.toggle_feature(fid, s))
        layout.addWidget(checkbox)
        
        return card
    
    def load_schools(self):
        """Load schools into selector"""
        from school_manager.models.database import School, License
        from school_manager.utils.hardware import HardwareFingerprint
        
        # Get current machine as "this school"
        current_machine = HardwareFingerprint.get_machine_id()
        
        # For demo, show current school
        school = self.session.query(School).first()
        if not school:
            school = School(name="Demo School")
            self.session.add(school)
            self.session.commit()
        
        self.school_combo.clear()
        self.school_combo.addItem(school.name, school.id)
        
        self.current_school_id = school.id
        self.update_school_info()
        self.update_feature_states()
    
    def on_school_changed(self, index):
        """Handle school selection change"""
        school_id = self.school_combo.currentData()
        if school_id:
            self.current_school_id = school_id
            self.update_school_info()
            self.update_feature_states()
    
    def update_school_info(self):
        """Update school info display"""
        from school_manager.models.database import School, License, Student, Staff, Class
        from school_manager.utils.hardware import HardwareFingerprint
        from school_manager.models.features import SubscriptionPlan
        
        school = self.session.query(School).filter(School.id == self.current_school_id).first()
        if not school:
            return
        
        self.school_name_label.setText(school.name)
        
        # Get license info
        current_machine = HardwareFingerprint.get_machine_id()
        license = self.session.query(License).filter(
            License.machine_id == current_machine
        ).first()
        
        tier = license.tier if license else 'bronze'
        tier_display = SubscriptionPlan.get_tier_display_name(tier)
        self.tier_label.setText(f"Tier: {tier_display}")
        
        if license and license.expiry_date:
            self.expiry_label.setText(f"Expires: {license.expiry_date}")
        else:
            self.expiry_label.setText("Expires: Never")
        
        # Count entities
        student_count = self.session.query(Student).count()
        staff_count = self.session.query(Staff).count()
        class_count = self.session.query(Class).count()
        
        self.students_label.setText(f"Students: {student_count}")
        self.staff_label.setText(f"Staff: {staff_count}")
        
        # Update progress bars
        max_students = license.max_students if license else 100
        if max_students == -1:
            max_students = student_count + 100
        
        max_staff = license.max_staff if license else 20
        if max_staff == -1:
            max_staff = staff_count + 100
        
        max_classes = license.max_classes if license else 5
        if max_classes == -1:
            max_classes = class_count + 100
        
        self.usage_students.setMaximum(max_students)
        self.usage_students.setValue(student_count)
        self.usage_students.setFormat(f"{student_count}/{max_students}")
        
        self.usage_staff.setMaximum(max_staff)
        self.usage_staff.setValue(staff_count)
        self.usage_staff.setFormat(f"{staff_count}/{max_staff}")
        
        self.usage_classes.setMaximum(max_classes)
        self.usage_classes.setValue(class_count)
        self.usage_classes.setFormat(f"{class_count}/{max_classes}")
    
    def update_feature_states(self):
        """Update feature toggle states"""
        from school_manager.models.features import FeatureManager
        
        manager = FeatureManager(self.session, self.current_school_id)
        enabled_features = manager.get_school_features(self.current_school_id)
        
        # Update all checkboxes
        for checkbox in self.findChildren(QCheckBox):
            feat_id = checkbox.objectName()
            if feat_id:
                checkbox.setChecked(feat_id in enabled_features)
    
    def toggle_feature(self, feature_id, state):
        """Handle feature toggle"""
        from school_manager.models.features import FeatureManager
        
        manager = FeatureManager(self.session, self.current_school_id)
        
        if state == Qt.CheckState.Checked.value:
            manager.enable_feature(self.current_school_id, feature_id)
        else:
            manager.disable_feature(self.current_school_id, feature_id)
    
    def enable_category(self, category):
        """Enable all features in a category"""
        from school_manager.models.features import FeatureRegistry, FeatureManager
        
        features = FeatureRegistry.get_all_features()
        manager = FeatureManager(self.session, self.current_school_id)
        
        for feat_id, feat_data in features.items():
            if feat_data['category'] == category:
                manager.enable_feature(self.current_school_id, feat_id)
        
        self.update_feature_states()
        QMessageBox.information(self, "Success", "All features in category enabled")
    
    def disable_category(self, category):
        """Disable all features in a category"""
        from school_manager.models.features import FeatureRegistry, FeatureManager
        
        features = FeatureRegistry.get_all_features()
        manager = FeatureManager(self.session, self.current_school_id)
        
        for feat_id, feat_data in features.items():
            if feat_data['category'] == category:
                # Don't disable core features
                if feat_data.get('default_tier') is not None or feat_data.get('is_critical'):
                    manager.disable_feature(self.current_school_id, feat_id)
        
        self.update_feature_states()
        QMessageBox.information(self, "Success", "Premium features in category disabled")
    
    def enable_all_tier_features(self):
        """Enable all features for current tier"""
        from school_manager.models.database import License
        from school_manager.models.features import FeatureManager
        
        current_machine = HardwareFingerprint.get_machine_id()
        license = self.session.query(License).filter(
            License.machine_id == current_machine
        ).first()
        
        tier = license.tier if license else 'bronze'
        
        manager = FeatureManager(self.session, self.current_school_id)
        tier_features = manager.get_tier_defaults(tier)
        
        for feat_id in tier_features:
            manager.enable_feature(self.current_school_id, feat_id)
        
        self.update_feature_states()
        QMessageBox.information(self, "Success", f"All {tier.upper()} tier features enabled")
    
    def disable_all_premium(self):
        """Disable all premium features"""
        from school_manager.models.features import FeatureRegistry, FeatureManager
        
        features = FeatureRegistry.get_all_features()
        manager = FeatureManager(self.session, self.current_school_id)
        
        disabled = 0
        for feat_id, feat_data in features.items():
            # Only disable non-core features
            if feat_data.get('default_tier') is not None:
                manager.disable_feature(self.current_school_id, feat_id)
                disabled += 1
        
        self.update_feature_states()
        QMessageBox.information(self, "Success", f"Disabled {disabled} premium features")
    
    def reset_to_defaults(self):
        """Reset to tier defaults"""
        from school_manager.models.features import FeatureManager
        
        manager = FeatureManager(self.session, self.current_school_id)
        manager.reset_to_tier_defaults(self.current_school_id)
        
        self.update_feature_states()
        QMessageBox.information(self, "Success", "Reset to tier defaults")


class FeatureAccessDialog(QDialog):
    """Dialog for viewing/editing school feature access"""
    
    def __init__(self, session, school_id, parent=None):
        super().__init__(parent)
        self.session = session
        self.school_id = school_id
        self.setWindowTitle("Feature Access")
        self.setMinimumSize(600, 500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("🏫 School Feature Access")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)
        
        # Feature list
        from school_manager.models.features import FeatureRegistry, FeatureManager
        
        manager = FeatureManager(self.session, self.school_id)
        enabled = manager.get_school_features(self.school_id)
        features = FeatureRegistry.get_all_features()
        
        self.feature_list = QListWidget()
        for feat_id, feat_data in features.items():
            item = QListWidgetItem(f"{feat_data['icon']} {feat_data['name']}")
            item.setData(Qt.ItemDataRole.UserRole, feat_id)
            item.setCheckState(Qt.CheckState.Checked if feat_id in enabled else Qt.CheckState.Unchecked)
            self.feature_list.addItem(item)
        
        layout.addWidget(self.feature_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)
        btn_layout.addWidget(save_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def save_changes(self):
        from school_manager.models.features import FeatureManager
        
        manager = FeatureManager(self.session, self.school_id)
        
        for i in range(self.feature_list.count()):
            item = self.feature_list.item(i)
            feat_id = item.data(Qt.ItemDataRole.UserRole)
            enabled = item.checkState() == Qt.CheckState.Checked
            
            if enabled:
                manager.enable_feature(self.school_id, feat_id)
            else:
                manager.disable_feature(self.school_id, feat_id)
        
        QMessageBox.information(self, "Success", "Feature access updated")
        self.accept()
