"""
UI Components - Reusable widgets
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                              QPushButton, QFrame, QScrollArea, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QLinearGradient, QColor


class CardWidget(QWidget):
    """Modern card container widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet("""
            QWidget#card {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)


class StatCard(QWidget):
    """Statistics display card"""
    
    def __init__(self, title="", value="0", icon=None, color="#2563eb", parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card")
        self.setStyleSheet("""
            QWidget#stat_card {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 20px;
            }
        """)
        self.setMinimumHeight(100)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #64748b; font-size: 12px; font-weight: 500;")
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        
        # Icon (placeholder)
        if icon:
            self.icon_label = QLabel(f"<center>{icon}</center>")
            self.icon_label.setStyleSheet(f"color: {color}; font-size: 24px;")
        else:
            self.icon_label = QLabel()
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.icon_label)
        layout.addStretch()
    
    def set_value(self, value):
        self.value_label.setText(str(value))
    
    def set_title(self, title):
        self.title_label.setText(title)
    
    def set_color(self, color):
        self.value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")


class SidebarButton(QPushButton):
    """Sidebar navigation button"""
    
    def __init__(self, text, icon=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("sidebar_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(44)
        
        if icon:
            self.setText(f"  {icon}  {text}")
        
        self.setStyleSheet("""
            QPushButton#sidebar_btn {
                background-color: transparent;
                border: none;
                color: #94a3b8;
                text-align: left;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 8px;
                margin: 2px 8px;
            }
            QPushButton#sidebar_btn:hover {
                background-color: #334155;
                color: #ffffff;
            }
            QPushButton#sidebar_btn.active {
                background-color: #2563eb;
                color: #ffffff;
            }
        """)


class PrimaryButton(QPushButton):
    """Primary action button"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("primary_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton#primary_btn {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton#primary_btn:hover {
                background-color: #1e40af;
            }
            QPushButton#primary_btn:pressed {
                background-color: #1e3a8a;
            }
            QPushButton#primary_btn:disabled {
                background-color: #94a3b8;
            }
        """)


class SecondaryButton(QPushButton):
    """Secondary action button"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("secondary_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton#secondary_btn {
                background-color: #f1f5f9;
                color: #0f172a;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#secondary_btn:hover {
                background-color: #e2e8f0;
            }
        """)


class DangerButton(QPushButton):
    """Danger/Delete action button"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("danger_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton#danger_btn {
                background-color: #dc2626;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton#danger_btn:hover {
                background-color: #b91c1c;
            }
        """)


class StatusBadge(QLabel):
    """Status badge label"""
    
    def __init__(self, text, status="success", parent=None):
        super().__init__(text, parent)
        colors = {
            "success": ("#dcfce7", "#16a34a"),
            "warning": ("#ffedd5", "#ea580c"),
            "error": ("#fee2e2", "#dc2626"),
            "info": ("#dbeafe", "#2563eb"),
        }
        bg, fg = colors.get(status, colors["info"])
        self.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
        """)


class TitleLabel(QLabel):
    """Page title label"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            color: #0f172a;
            font-size: 24px;
            font-weight: bold;
        """)


class SubtitleLabel(QLabel):
    """Subtitle label"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            color: #64748b;
            font-size: 14px;
        """)


class FormLabel(QLabel):
    """Form field label"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            color: #374151;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 6px;
        """)


class HeaderBar(QWidget):
    """Header bar with title and actions"""
    
    def __init__(self, title="", subtitle="", parent=None):
        super().__init__(parent)
        self.setMinimumHeight(60)
        self.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #e2e8f0;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 15, 24, 15)
        
        # Title section
        title_section = QVBoxLayout()
        title_section.setSpacing(4)
        
        self.title_label = TitleLabel(title)
        self.subtitle_label = SubtitleLabel(subtitle)
        
        title_section.addWidget(self.title_label)
        title_section.addWidget(self.subtitle_label)
        
        layout.addLayout(title_section)
        layout.addStretch()
        
        # Actions container
        self.actions_layout = QHBoxLayout()
        self.actions_layout.setSpacing(10)
        layout.addLayout(self.actions_layout)
    
    def add_action(self, button):
        self.actions_layout.addWidget(button)
    
    def set_title(self, title):
        self.title_label.setText(title)
    
    def set_subtitle(self, subtitle):
        self.subtitle_label.setText(subtitle)


class ScrollArea(QScrollArea):
    """Styled scroll area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)


class ContentArea(QWidget):
    """Main content area container"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f8fafc;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        self.scroll = ScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.addStretch()
        
        self.scroll.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll)
    
    def add_widget(self, widget):
        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, widget)
    
    def clear(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


class DataTable(QWidget):
    """Data table widget with pagination"""
    
    def __init__(self, columns=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
        
        self.table = QTableWidget()
        self.table.setObjectName("data_table")
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                gridline-color: #f1f5f9;
                font-size: 13px;
                selection-background-color: #dbeafe;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f5f9;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                color: #0f172a;
                font-weight: 600;
                font-size: 12px;
                text-transform: uppercase;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
            }
        """)
        
        if columns:
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
        
        # Set column stretching
        header = self.table.horizontalHeader()
        for i in range(len(columns) if columns else 0):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        
        # Pagination
        pagination = QHBoxLayout()
        pagination.addStretch()
        
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                color: #0f172a;
            }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        self.page_label = QLabel("Page 1 of 1")
        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                color: white;
            }
            QPushButton:hover { background-color: #1e40af; }
        """)
        
        pagination.addWidget(self.prev_btn)
        pagination.addWidget(self.page_label)
        pagination.addWidget(self.next_btn)
        
        layout.addLayout(pagination)
    
    def set_data(self, data):
        """Set table data (list of dicts)"""
        self.table.setRowCount(len(data))
        
        if not data:
            return
        
        # Use first row's keys to determine columns
        keys = list(data[0].keys()) if isinstance(data[0], dict) else list(range(len(data[0])))
        
        for row_idx, row_data in enumerate(data):
            if isinstance(row_data, dict):
                for col_idx, key in enumerate(keys):
                    item = QTableWidgetItem(str(row_data.get(key, '')))
                    self.table.setItem(row_idx, col_idx, item)
            else:
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_idx, col_idx, item)
    
    def get_selected_row(self):
        """Get selected row index"""
        return self.table.currentRow()
    
    def get_row_data(self, row=None):
        """Get row data as dict"""
        if row is None:
            row = self.table.currentRow()
        
        if row < 0:
            return None
        
        data = {}
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text()
            item = self.table.item(row, col)
            data[header] = item.text() if item else ''
        
        return data


class FormField(QWidget):
    """Form field with label and input"""
    
    def __init__(self, label, widget, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        self.label = FormLabel(label)
        self.input = widget
        
        layout.addWidget(self.label)
        layout.addWidget(self.input)


class IconButton(QPushButton):
    """Icon-only button"""
    
    def __init__(self, icon_text, tooltip="", parent=None):
        super().__init__(icon_text, parent)
        self.setFixedSize(36, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #64748b;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                color: #2563eb;
            }
        """)
        if tooltip:
            self.setToolTip(tooltip)


class AvatarWidget(QLabel):
    """User avatar widget"""
    
    def __init__(self, name="", size=40, parent=None):
        super().__init__(parent)
        self.name = name
        self.size = size
        self.setFixedSize(size, size)
        
        # Generate initials
        initials = ""
        if name:
            parts = name.split()
            for part in parts[:2]:
                if part:
                    initials += part[0].upper()
        
        self.setText(initials)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            background-color: #2563eb;
            color: white;
            border-radius: {size//2}px;
            font-size: {size//3}px;
            font-weight: bold;
        """)


class LoadingOverlay(QWidget):
    """Loading overlay widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("background-color: rgba(248, 250, 252, 0.8);")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel("Loading...")
        self.label.setStyleSheet("""
            color: #0f172a;
            font-size: 16px;
            font-weight: 500;
        """)
        
        layout.addWidget(self.label)
    
    def show(self):
        parent = self.parent()
        if parent:
            self.setGeometry(parent.rect())
        super().show()
    
    def hide(self):
        super().hide()
