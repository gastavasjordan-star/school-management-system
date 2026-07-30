"""
Modern UI Styles and Theme Configuration
"""
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QColor, QPalette, QFont, QIcon, QPixmap, QPainter, QLinearGradient
from PyQt6.QtWidgets import QStyleFactory, QProxyStyle


# Color Palette
class Colors:
    """Application color palette"""
    BG_LIGHT = QColor('#f8fafc')      # Main background
    CARD_WHITE = QColor('#ffffff')     # Card backgrounds
    TEXT_DARK = QColor('#0f172a')      # Primary text
    TEXT_MUTED = QColor('#64748b')     # Secondary text
    ACCENT_BLUE = QColor('#2563eb')    # Primary accent
    ACCENT_LIGHT = QColor('#dbeafe')   # Light blue
    ACCENT_DARK = QColor('#1e40af')    # Dark blue
    SUCCESS = QColor('#16a34a')        # Green
    SUCCESS_LIGHT = QColor('#dcfce7')  # Light green
    WARNING = QColor('#ea580c')        # Orange
    WARNING_LIGHT = QColor('#ffedd5')  # Light orange
    ERROR = QColor('#dc2626')          # Red
    ERROR_LIGHT = QColor('#fee2e2')     # Light red
    BORDER = QColor('#e2e8f0')          # Border color
    SIDEBAR_BG = QColor('#1e293b')      # Dark sidebar
    SIDEBAR_TEXT = QColor('#94a3b8')    # Sidebar text
    SIDEBAR_ACTIVE = QColor('#2563eb') # Sidebar active item


class ModernStylesheet:
    """Modern CSS-like stylesheet for the application"""
    
    @staticmethod
    def get_stylesheet():
        return """
        /* Main Window */
        QMainWindow {
            background-color: #f8fafc;
        }
        
        /* Sidebar */
        QWidget#sidebar {
            background-color: #1e293b;
        }
        
        QPushButton#sidebar_btn {
            background-color: transparent;
            border: none;
            color: #94a3b8;
            text-align: left;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 8px;
        }
        
        QPushButton#sidebar_btn:hover {
            background-color: #334155;
            color: #ffffff;
        }
        
        QPushButton#sidebar_btn.active {
            background-color: #2563eb;
            color: #ffffff;
        }
        
        QPushButton#sidebar_btn:pressed {
            background-color: #1e40af;
        }
        
        /* Sidebar Header */
        QLabel#sidebar_title {
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
            padding: 20px;
        }
        
        QLabel#sidebar_subtitle {
            color: #64748b;
            font-size: 11px;
            padding: 0px 20px 20px 20px;
        }
        
        /* Cards */
        QWidget#card {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }
        
        /* Primary Button */
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
        
        /* Secondary Button */
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
        
        /* Danger Button */
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
        
        /* Input Fields */
        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 14px;
            color: #0f172a;
        }
        
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #2563eb;
        }
        
        QLineEdit:placeholder, QTextEdit:placeholder {
            color: #94a3b8;
        }
        
        /* ComboBox */
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 14px;
            color: #0f172a;
        }
        
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #64748b;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            selection-background-color: #2563eb;
            padding: 5px;
        }
        
        /* Table */
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
        
        QTableWidget::item:selected {
            background-color: #dbeafe;
            color: #0f172a;
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
        
        /* Tab Widget */
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
        
        QTabBar::tab:hover:!selected {
            color: #0f172a;
        }
        
        /* Labels */
        QLabel#title {
            color: #0f172a;
            font-size: 24px;
            font-weight: bold;
        }
        
        QLabel#subtitle {
            color: #64748b;
            font-size: 14px;
        }
        
        QLabel#card_title {
            color: #0f172a;
            font-size: 16px;
            font-weight: 600;
        }
        
        /* Stats Card */
        QWidget#stat_card {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }
        
        QLabel#stat_value {
            color: #0f172a;
            font-size: 28px;
            font-weight: bold;
        }
        
        QLabel#stat_label {
            color: #64748b;
            font-size: 12px;
        }
        
        /* Status Badge */
        QLabel#badge_success {
            background-color: #dcfce7;
            color: #16a34a;
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        QLabel#badge_warning {
            background-color: #ffedd5;
            color: #ea580c;
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        QLabel#badge_error {
            background-color: #fee2e2;
            color: #dc2626;
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        /* Scrollbar */
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
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }
        
        /* Dialog */
        QDialog {
            background-color: #f8fafc;
        }
        
        /* Menu */
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 5px;
        }
        
        QMenu::item {
            padding: 10px 20px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #dbeafe;
        }
        
        /* Toolbar */
        QToolBar {
            background-color: #ffffff;
            border: none;
            border-bottom: 1px solid #e2e8f0;
            spacing: 10px;
            padding: 10px;
        }
        
        /* Progress Bar */
        QProgressBar {
            background-color: #e2e8f0;
            border: none;
            border-radius: 6px;
            height: 8px;
        }
        
        QProgressBar::chunk {
            background-color: #2563eb;
            border-radius: 6px;
        }
        
        /* Message Box */
        QMessageBox {
            background-color: #ffffff;
        }
        
        /* CheckBox */
        QCheckBox {
            spacing: 8px;
            font-size: 14px;
            color: #0f172a;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #e2e8f0;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2563eb;
            border-color: #2563eb;
        }
        
        /* Radio Button */
        QRadioButton {
            spacing: 8px;
            font-size: 14px;
            color: #0f172a;
        }
        
        QRadioButton::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            background-color: #ffffff;
        }
        
        QRadioButton::indicator:checked {
            background-color: #2563eb;
            border-color: #2563eb;
        }
        
        /* Group Box */
        QGroupBox {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: 600;
            color: #0f172a;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
        }
        """
    
    @staticmethod
    def get_sidebar_style():
        return """
        QWidget#sidebar {
            background-color: #1e293b;
        }
        
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
        
        QLabel#sidebar_separator {
            background-color: #334155;
            margin: 10px 20px;
            max-height: 1px;
        }
        
        QLabel#user_label {
            color: #ffffff;
            font-size: 14px;
            font-weight: 500;
        }
        
        QLabel#role_label {
            color: #64748b;
            font-size: 11px;
        }
        """


def get_font(family="Segoe UI", size=10, weight=QFont.Weight.Normal):
    """Get a configured font"""
    font = QFont(family, size)
    font.setWeight(weight)
    return font


def set_app_font(widget, family="Segoe UI", size=10):
    """Set font for a widget and its children"""
    font = QFont(family, size)
    widget.setFont(font)
    for child in widget.children():
        if isinstance(child, (QFont)):
            child.setFont(font)
