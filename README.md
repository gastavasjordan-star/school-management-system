# 🏫 School Manager - Enterprise Edition

A comprehensive, enterprise-grade offline School Management System with hardware licensing, role-based access control, LAN parent/student portal, and modern PDF report generation.

## ✨ Features

### 1. Hardware Licensing & Anti-Piracy
- **Machine Fingerprinting**: Generates unique Machine ID from CPU/Motherboard UUID
- **License Activation**: Blocks app access until valid license key is provided
- **Term Lock**: Publish term freezes data as read-only; advancing requires authorization

### 2. Monetized Feature Toggles (Super Admin Controls)
- Student Photo Processing & Bulk ID Card Printing
- High-Res Custom PDF Branding Engine
- Automated Email Fee Demand Letters
- Automated Cloud Backup Sync

### 3. LAN-Only Parent & Student Portal
- **Zero-Registration Authentication**: Parents use Student ID + Parent Phone
- **QR Code Bridge**: Dynamic QR code for easy mobile access
- **Local IP Auto-Detection**: Automatically detects host machine's LAN IP
- **No Internet Required**: Works entirely on school LAN

### 4. Role-Based Access Control

| Role | Permissions |
|------|-------------|
| **Super Admin (Jordan)** | Unlimited control + User Impersonation |
| **School Admin** | Operational oversight, revenue, metrics |
| **Director of Studies** | Academic broadsheets, rankings, exam locking |
| **Class Teacher** | Enter marks, view performance, report cards |
| **Subject Teacher** | Enter marks for assigned subjects only |
| **Bursar** | Fee structure, payments, receipts |
| **Secretary** | Student registration, parent details |

### 5. Modern PDF Engine
- Curved styled PDF headers with school branding
- Student report cards with photos and rankings
- Auto-generated teacher comments based on marks
- A4 printable ID card grids (8-10 cards per page)

### 6. Hybrid Backup System
- **USB Backup**: Auto-export encrypted SQLite to flash drive
- **Cloud Sync**: Silent upload to Google Drive when online

### 7. 20 Core Enterprise Features

1. ✅ Automated Fee Demand Letters
2. ✅ Dynamic A4 Student ID Generator Grid
3. ✅ Subject & Class Performance Analytics
4. ✅ Student & Class Ranking Engine
5. ✅ Class Teacher Broadsheet Export
6. ✅ LAN Parent/Student PWA Portal
7. ✅ Bursar Payment Receipt Engine (Thermal/A5/A4)
8. ✅ Automated End-of-Year Student Promotion
9. ✅ Staff Attendance & Payroll Tracker
10. ✅ Library & Book Inventory
11. ✅ Disciplinary & Behavior Tracking
12. ✅ Medical & Health Records
13. ✅ Custom Grading Scheme Configurator
14. ✅ Audit Trail & Activity Logs
15. ✅ Multi-Stream Support
16. ✅ One-Click USB Emergency Restore
17. ✅ Digital School Stamp & Signature Overlays
18. ✅ Custom ID Card Designer Templates
19. ✅ High-Achiever Leaderboards
20. ✅ Graduation & Alumni Archiving

## 🖥️ System Requirements

- **OS**: Windows 10/11 (64-bit) or Linux with GUI
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Display**: 1280x720 minimum resolution

## 📦 Installation

### Option 1: Pre-built Executable
```bash
# Download the latest release from releases page
# Run SchoolManager.exe
```

### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/your-repo/school-manager.git
cd school-manager

# Install dependencies
pip install -r requirements.txt

# Run the application
python school_manager/app.py
```

### Option 3: Build Standalone Executable
```bash
# Run the build script
chmod +x build.sh
./build.sh

# Or use PyInstaller directly
pyinstaller --windowed --onedir school_manager/app.py
```

## 🚀 Getting Started

### First Launch
1. **Activation**: Enter your license key (contact your vendor)
2. **Login**: Use default credentials:
   - Username: `Jordan`
   - Password: `admin123`
3. **Configure**: Set up your school information in Settings

### Quick Setup Checklist
- [ ] Configure School Information (name, address, logo)
- [ ] Add Staff Members
- [ ] Create Classes and Streams
- [ ] Add Subjects
- [ ] Set up Fee Structures
- [ ] Enable Parent Portal (optional)

## 📱 Parent/Student Portal

The LAN portal allows parents to access their child's information without internet:

1. Start the portal from **Settings > Portal Settings**
2. A QR code is displayed with the portal URL
3. Parents scan the QR code on the school Wi-Fi
4. Login with:
   - **Username**: Student's ID (e.g., `SCH/2026/001`)
   - **Password**: Parent's registered phone number

## 🎨 UI Design

Modern light theme with enterprise aesthetics:
- **Background**: Slate (#f8fafc)
- **Cards**: Pure White (#ffffff)
- **Text**: Dark Slate (#0f172a)
- **Accent**: Vibrant Blue (#2563eb)

## 📁 Project Structure

```
school_manager/
├── app.py                 # Main entry point
├── models/
│   └── database.py       # SQLAlchemy models
├── views/
│   ├── main_window.py    # Main UI window
│   ├── styles.py         # Modern styles
│   └── components.py     # Reusable widgets
├── utils/
│   ├── auth.py          # Authentication & RBAC
│   ├── hardware.py       # Hardware licensing
│   ├── pdf_engine.py     # PDF generation
│   └── backup.py        # Backup system
├── portal/
│   └── parent_portal.py # LAN portal server
└── school_data.db       # SQLite database
```

## 🔐 Security Features

- Hardware-locked licensing
- Password hashing (SHA-256)
- Encrypted backups (Fernet)
- Audit trail logging
- Role-based permissions

## 📊 Database Schema

Key tables:
- `schools` - School configuration
- `users` - System users with roles
- `students` - Student records
- `parents` - Parent/guardian info
- `staff` - Teachers and staff
- `classes` - Class definitions
- `subjects` - Subject catalog
- `exam_results` - Student marks
- `fee_payments` - Payment records
- `licenses` - License keys
- `audit_logs` - Activity tracking

## 🛠️ Development

### Adding New Features

1. Add database models in `models/database.py`
2. Create UI components in `views/`
3. Add business logic in `utils/`
4. Register routes in `views/main_window.py`

### Building Custom Reports

```python
from school_manager.utils.pdf_engine import ReportCardGenerator

generator = ReportCardGenerator(school_info)
pdf = generator.generate_report_card(student, results, term_info)
```

## 📝 License

This software requires a valid license key. Contact your vendor for pricing and activation.

## 🤝 Support

For technical support:
- Email: support@schoolmanager.com
- Documentation: docs.schoolmanager.com

## 📄 License Key Format

License keys are encrypted strings in format:
```
XXXX-XXXX-XXXX-XXXX-XXXX
```

Generated by vendor using:
- Client name
- Expiry date
- Enabled features
- Hardware fingerprint validation

---

**Built with ❤️ for Educational Excellence**
