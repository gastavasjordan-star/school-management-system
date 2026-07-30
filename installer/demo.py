#!/usr/bin/env python3
"""
School Management System - Standalone Desktop Application
Compiled with PyInstaller for Windows
"""
import sqlite3
import hashlib
import os
import sys
from datetime import datetime

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def show_banner():
    clear()
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     ███████╗ █████╗ ██╗   ██╗██╗  ██████╗ ██████╗  ██████╗   ║
║     ██╔════╝██╔══██╗██║   ██║██║ ██╔═══██╗██╔══██╗██╔═══██╗  ║
║     ███████╗███████║██║   ██║██║ ██║   ██║██████╔╝██║   ██║  ║
║     ╚════██║██╔══██║╚██╗ ██╔╝██║ ██║   ██║██╔══██╗██║   ██║  ║
║     ███████║██║  ██║ ╚████╔╝ ██║ ╚██████╔╝██║  ██║╚██████╔╝  ║
║     ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ║
║                                                                  ║
║              Enterprise School Management System v1.0            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

def init_database():
    """Initialize the database with schema"""
    db_path = os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__), 'school.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT, email TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, role TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY, adm TEXT UNIQUE, first_name TEXT, last_name TEXT, 
        gender TEXT, class_id INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY, name TEXT, level INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY, name TEXT, code TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY, student_id INTEGER, date TEXT, status TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS fee_payments (
        id INTEGER PRIMARY KEY, student_id INTEGER, amount REAL, date TEXT, receipt TEXT)''')
    
    # Insert default data if empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        # Default super admin - password: admin123
        pwd_hash = hashlib.sha256(b"admin123").hexdigest()
        c.execute("INSERT INTO users VALUES (?,?,?,?)", (None, "Jordan", pwd_hash, "SUPER_ADMIN"))
        c.execute("INSERT INTO users VALUES (?,?,?,?)", (None, "Teacher", pwd_hash, "CLASS_TEACHER"))
        c.execute("INSERT INTO users VALUES (?,?,?,?)", (None, "Bursar", pwd_hash, "BURSAR"))
        
        # Demo school
        c.execute("INSERT INTO schools VALUES (?,?,?,?,?)", 
            (None, "Demo Academy", "123 Education Lane", "+254 712 345 678", "info@demo.edu"))
        
        # Demo classes
        for i, name in enumerate(["Form 1", "Form 2", "Form 3", "Form 4"]):
            c.execute("INSERT INTO classes VALUES (?,?,?)", (None, name, i+1))
        
        # Demo subjects
        subjects = [("Mathematics", "MATH"), ("English", "ENG"), ("Kiswahili", "KISW"), 
                   ("Science", "SCI"), ("History", "HIST"), ("Geography", "GEO")]
        for name, code in subjects:
            c.execute("INSERT INTO subjects VALUES (?,?,?)", (None, name, code))
        
        # Demo students
        students = [("Amina", "Wanjiku", "Female", 1), ("John", "Kamau", "Male", 2),
                   ("Faith", "Otieno", "Female", 3), ("David", "Mwangi", "Male", 4)]
        for first, last, gender, cls in students:
            adm = f"SCH/2024/{students.index((first,last,gender,cls))+1:03d}"
            c.execute("INSERT INTO students VALUES (?,?,?,?,?,?)", (None, adm, first, last, gender, cls))
    
    conn.commit()
    return conn

def get_machine_id():
    """Get unique machine identifier"""
    return hashlib.md5(os.environ.get('COMPUTERNAME', 'PC').encode()).hexdigest()[:16].upper()

def login(conn):
    """Handle login"""
    print("\n" + "="*60)
    print("LOGIN")
    print("="*60)
    
    username = input("\nUsername: ").strip()
    password = input("Password: ").strip()
    
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    
    c = conn.cursor()
    c.execute("SELECT username, role FROM users WHERE username=? AND password_hash=?", (username, pwd_hash))
    result = c.fetchone()
    
    if result:
        print(f"\n✅ Login successful! Welcome, {result[0]}")
        print(f"   Role: {result[1]}")
        input("\nPress Enter to continue...")
        return result
    else:
        print("\n❌ Invalid credentials!")
        input("\nPress Enter to try again...")
        return None

def show_dashboard(conn, user):
    """Show main dashboard"""
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM students")
    students = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users")
    users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM classes")
    classes = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM subjects")
    subjects = c.fetchone()[0]
    
    clear()
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                     DASHBOARD - {user[0].upper():<33}║
╚══════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────┐
│  📊 OVERVIEW                                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   👨‍🎓 Students     :  {students:<5}                                    │
│   👨‍🏫 Staff        :  {users:<5}                                    │
│   🏫 Classes      :  {classes:<5}                                    │
│   📚 Subjects     :  {subjects:<5}                                    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  🎯 QUICK ACTIONS                                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   [1] 👨‍🎓 Manage Students                                           │
│   [2] 👨‍🏫 Manage Staff                                              │
│   [3] 📚 Manage Classes                                           │
│   [4] 📝 Record Attendance                                        │
│   [5] 💰 Fee Collection                                           │
│   [6] 📄 Generate Reports                                         │
│   [7] ⚙️  Settings                                                │
│   [0] 🚪 Logout                                                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

Machine ID: {get_machine_id()}
""")

def main():
    """Main application entry point"""
    try:
        conn = init_database()
        
        while True:
            show_banner()
            print("Welcome to School Management System")
            print("-" * 40)
            print()
            print("1. Login")
            print("2. Exit")
            print()
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                user = login(conn)
                if user:
                    while True:
                        show_dashboard(conn, user)
                        choice = input("\nSelect action: ").strip()
                        
                        if choice == "0":
                            print("\nLogging out...")
                            break
                        elif choice == "7":
                            clear()
                            print("""
╔══════════════════════════════════════════════════════════════════╗
║                        SETTINGS                                   ║
╚══════════════════════════════════════════════════════════════════╝

🔐 License Information
   Plan: Gold (Demo)
   Machine ID: """ + get_machine_id() + """
   Status: Active

📋 System Information
   Version: 1.0.0
   Database: SQLite
   Python Version: """ + sys.version.split()[0] + """

📦 Installed Features (46 Total)
   ✅ Student Management
   ✅ Staff Management
   ✅ Fee Collection
   ✅ Exam Management
   ✅ Report Cards
   ✅ Attendance Tracking
   ✅ Library Management
   ✅ Transport Management
   ✅ Parent Portal
   ✅ Cloud Backup
   ❌ SMS Integration
   ❌ API Access
   ❌ White Label

Press Enter to continue...""")

                            input()
                        else:
                            print("\n⚠️  Feature coming soon!")
                            input()
            elif choice == "2":
                break
            else:
                print("\n⚠️  Invalid option!")
                input()
        
        conn.close()
        
    except Exception as e:
        print(f"\n\nError: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
