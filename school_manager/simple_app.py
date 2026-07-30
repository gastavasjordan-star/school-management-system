#!/usr/bin/env python3
"""
School Manager - Simple Standalone Demo
This is a simplified version that shows the UI works
Run this WITHOUT PyQt to verify core logic works
"""
import os
import sys
import json
from datetime import datetime

print("""
╔══════════════════════════════════════════════════════════════╗
║                    🏫 SCHOOL MANAGER                        ║
║              Enterprise School Management System              ║
╚══════════════════════════════════════════════════════════════╝
""")

# Test core modules
print("[1] Loading modules...")
try:
    from school_manager.models.database import Base, init_database, get_session, School, User, Student, Subject, Class, Stream
    from school_manager.utils.hardware import HardwareFingerprint
    from school_manager.models.features import FeatureRegistry
    print("    ✅ All modules loaded")
except ImportError as e:
    print(f"    ❌ Import error: {e}")
    sys.exit(1)

# Test database
print("\n[2] Testing database...")
db_path = "school_demo.db"
if os.path.exists(db_path):
    os.remove(db_path)
engine = init_database(db_path)
session = get_session(engine)
print("    ✅ Database working")

# Show machine ID
print("\n[3] Hardware ID:")
machine_id = HardwareFingerprint.get_machine_id()
print(f"    Machine ID: {machine_id[:40]}...")

# Show features
print("\n[4] Feature Registry:")
features = FeatureRegistry.get_all_features()
print(f"    ✅ {len(features)} features available")

categories = FeatureRegistry.get_features_by_category()
for cat_id, feats in list(categories.items())[:3]:
    cat_name = FeatureRegistry.get_category_display_name(cat_id)
    print(f"    📁 {cat_name}: {len(feats)} features")

# Demo data
print("\n[5] Creating demo data...")
school = School(name="Demo Academy", address="123 Main St", phone="0712345678", email="demo@school.edu")
session.add(school)

# Create subjects
subjects = ["Mathematics", "English", "Science", "History", "Geography"]
for sub_name in subjects:
    subject = Subject(name=sub_name, code=sub_name[:3].upper())
    session.add(subject)

# Create classes
classes = ["Form 1", "Form 2", "Form 3", "Form 4"]
for cls_name in classes:
    cls = Class(name=cls_name, level=1)
    session.add(cls)

session.commit()
print("    ✅ Demo data created")

# Show data
print("\n[6] Database contents:")
student_count = session.query(Student).count()
subject_count = session.query(Subject).count()
class_count = session.query(Class).count()
print(f"    📚 Students: {student_count}")
print(f"    📖 Subjects: {subject_count}")
print(f"    🏫 Classes: {class_count}")

session.close()

# Cleanup
if os.path.exists(db_path):
    os.remove(db_path)

print("""
╔══════════════════════════════════════════════════════════════╗
║                    ✅ CORE SYSTEMS WORKING                   ║
╚══════════════════════════════════════════════════════════════╝

To run the FULL GUI application:

1. Install Python 3.11+ from python.org

2. Install dependencies:
   pip install PyQt6 PyQt6-WebEngine reportlab Pillow qrcode cryptography

3. Run the app:
   set PYTHONPATH=C:\\path\\to\\school-management-system
   python school_manager/app.py

4. Login credentials:
   Username: Jordan
   Password: admin123

""")
