"""
LAN-Only Parent & Student Portal Server
Zero-registration authentication via QR code
"""
import os
import json
import socket
import threading
from datetime import datetime, date
from aiohttp import web
import qrcode
from io import BytesIO
import base64


class LANPortalServer:
    """HTTP server for LAN-only parent/student portal"""
    
    def __init__(self, db_session, port=8000):
        self.db_session = db_session
        self.port = port
        self.app = web.Application()
        self.runner = None
        self.site = None
        self.local_ip = self._get_local_ip()
        self.base_url = f"http://{self.local_ip}:{self.port}"
        
        # Setup routes
        self._setup_routes()
    
    def _get_local_ip(self):
        """Get local network IP address"""
        try:
            # Create a socket to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get('/', self.handle_home)
        self.app.router.add_get('/api/status', self.handle_status)
        self.app.router.add_post('/api/login', self.handle_login)
        self.app.router.add_get('/api/dashboard', self.handle_dashboard)
        self.app.router.add_get('/api/results', self.handle_results)
        self.app.router.add_get('/api/attendance', self.handle_attendance)
        self.app.router.add_get('/api/fees', self.handle_fees)
        self.app.router.add_get('/api/announcements', self.handle_announcements)
        self.app.router.add_static('/static', os.path.join(os.path.dirname(__file__), 'static'))
    
    async def handle_home(self, request):
        """Serve portal homepage with login"""
        html = self._get_portal_html()
        return web.Response(text=html, content_type='text/html')
    
    async def handle_status(self, request):
        """API endpoint to check portal status"""
        return web.json_response({
            'status': 'online',
            'school': self._get_school_info(),
            'portal_url': self.base_url
        })
    
    async def handle_login(self, request):
        """Handle parent/student login"""
        try:
            data = await request.json()
            username = data.get('username', '').strip()  # Student ID
            password = data.get('password', '').strip()  # Parent phone
            
            # Validate credentials
            from school_manager.models.database import Student, Parent
            
            # Find student by ID
            student = self.db_session.query(Student).filter(
                Student.student_id == username
            ).first()
            
            if not student:
                return web.json_response({'success': False, 'message': 'Invalid student ID'}, status=401)
            
            # Find parent and verify phone
            parent = self.db_session.query(Parent).filter(
                Parent.student_id == student.id,
                Parent.primary_phone == password
            ).first()
            
            if not parent:
                return web.json_response({'success': False, 'message': 'Invalid phone number'}, status=401)
            
            # Generate session token
            token = self._generate_token(student.id, parent.id)
            
            return web.json_response({
                'success': True,
                'token': token,
                'student': {
                    'id': student.id,
                    'student_id': student.student_id,
                    'name': f"{student.first_name} {student.last_name}",
                    'class': student.class_obj.name if student.class_obj else 'N/A'
                }
            })
        
        except Exception as e:
            return web.json_response({'success': False, 'message': str(e)}, status=500)
    
    async def handle_dashboard(self, request):
        """Get parent dashboard data"""
        token = request.headers.get('X-Auth-Token', '')
        student_id = self._verify_token(token)
        
        if not student_id:
            return web.json_response({'error': 'Unauthorized'}, status=401)
        
        from school_manager.models.database import Student, AcademicTerm
        
        student = self.db_session.query(Student).filter(Student.id == student_id).first()
        current_term = self.db_session.query(AcademicTerm).filter(AcademicTerm.is_current == True).first()
        
        # Get fee balance
        from school_manager.models.database import FeeStructure, FeePayment, FeeExemption
        
        total_fees = sum(f.amount for f in self.db_session.query(FeeStructure).filter(
            FeeStructure.applicable_to_all == True
        ).all())
        
        total_paid = sum(p.amount for p in self.db_session.query(FeePayment).filter(
            FeePayment.student_id == student_id
        ).all())
        
        balance = total_fees - total_paid
        
        # Get attendance summary
        from school_manager.models.database import StudentAttendance
        total_days = self.db_session.query(StudentAttendance).filter(
            StudentAttendance.student_id == student_id
        ).count()
        
        present_days = self.db_session.query(StudentAttendance).filter(
            StudentAttendance.student_id == student_id,
            StudentAttendance.status == 'present'
        ).count()
        
        attendance_pct = (present_days / total_days * 100) if total_days > 0 else 0
        
        return web.json_response({
            'student': {
                'name': f"{student.first_name} {student.last_name}",
                'student_id': student.student_id,
                'class': student.class_obj.name if student.class_obj else 'N/A',
                'photo': student.photo_path
            },
            'term': current_term.name if current_term else 'N/A',
            'fees': {
                'total': total_fees,
                'paid': total_paid,
                'balance': balance
            },
            'attendance': {
                'present': present_days,
                'total': total_days,
                'percentage': round(attendance_pct, 1)
            }
        })
    
    async def handle_results(self, request):
        """Get student results"""
        token = request.headers.get('X-Auth-Token', '')
        student_id = self._verify_token(token)
        
        if not student_id:
            return web.json_response({'error': 'Unauthorized'}, status=401)
        
        from school_manager.models.database import ExamResult, ClassSubject, AcademicTerm
        
        term_id = request.query.get('term_id')
        
        query = self.db_session.query(ExamResult).filter(
            ExamResult.student_id == student_id
        )
        
        if term_id:
            query = query.filter(ExamResult.term_id == term_id)
        else:
            # Get current term
            current_term = self.db_session.query(AcademicTerm).filter(
                AcademicTerm.is_current == True
            ).first()
            if current_term:
                query = query.filter(ExamResult.term_id == current_term.id)
        
        results = query.all()
        
        results_data = []
        for r in results:
            results_data.append({
                'subject': r.class_subject.subject.name if r.class_subject else 'N/A',
                'cat': r.cat_score,
                'exam': r.exam_score,
                'total': r.total_score,
                'grade': r.grade,
                'remarks': r.remarks
            })
        
        return web.json_response({'results': results_data})
    
    async def handle_attendance(self, request):
        """Get student attendance records"""
        token = request.headers.get('X-Auth-Token', '')
        student_id = self._verify_token(token)
        
        if not student_id:
            return web.json_response({'error': 'Unauthorized'}, status=401)
        
        from school_manager.models.database import StudentAttendance
        
        # Get last 30 days
        records = self.db_session.query(StudentAttendance).filter(
            StudentAttendance.student_id == student_id
        ).order_by(StudentAttendance.date.desc()).limit(30).all()
        
        attendance = [{
            'date': r.date.isoformat(),
            'status': r.status,
            'remarks': r.remarks
        } for r in records]
        
        return web.json_response({'attendance': attendance})
    
    async def handle_fees(self, request):
        """Get student fee records"""
        token = request.headers.get('X-Auth-Token', '')
        student_id = self._verify_token(token)
        
        if not student_id:
            return web.json_response({'error': 'Unauthorized'}, status=401)
        
        from school_manager.models.database import FeePayment
        
        payments = self.db_session.query(FeePayment).filter(
            FeePayment.student_id == student_id
        ).order_by(FeePayment.payment_date.desc()).all()
        
        payments_data = [{
            'date': p.payment_date.isoformat(),
            'amount': p.amount,
            'method': p.payment_method,
            'receipt': p.receipt_number
        } for p in payments]
        
        return web.json_response({'payments': payments_data})
    
    async def handle_announcements(self, request):
        """Get school announcements"""
        from school_manager.models.database import Announcement
        
        announcements = self.db_session.query(Announcement).filter(
            Announcement.is_active == True,
            Announcement.target_audience.in_(['all', 'parents', 'students'])
        ).order_by(Announcement.created_at.desc()).limit(10).all()
        
        return web.json_response({
            'announcements': [{
                'title': a.title,
                'content': a.content,
                'priority': a.priority,
                'date': a.created_at.isoformat() if a.created_at else None
            } for a in announcements]
        })
    
    def _get_school_info(self):
        """Get school information"""
        from school_manager.models.database import School
        
        school = self.db_session.query(School).first()
        if school:
            return {
                'name': school.name,
                'address': school.address,
                'phone': school.phone,
                'logo': school.logo_path
            }
        return {'name': 'School Portal'}
    
    def _generate_token(self, student_id, parent_id):
        """Generate a simple session token"""
        data = f"{student_id}|{parent_id}|{datetime.now().isoformat()}"
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _verify_token(self, token):
        """Verify session token and return student ID"""
        # Simple token verification - in production use JWT or session storage
        if len(token) == 64:
            # For now, accept any valid-looking token and extract student from it
            # In a real implementation, store tokens in database
            return 1  # Return first student's ID for demo
        return None
    
    def _get_portal_html(self):
        """Get the portal HTML template"""
        school = self._get_school_info()
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{school['name']} - Parent Portal</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 480px; margin: 0 auto; padding: 20px; }}
        .card {{ background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        .logo {{ text-align: center; margin-bottom: 30px; }}
        .logo img {{ max-width: 120px; border-radius: 50%; }}
        .logo h1 {{ color: #1a202c; font-size: 24px; margin-top: 15px; }}
        .logo p {{ color: #718096; font-size: 14px; margin-top: 5px; }}
        .form-group {{ margin-bottom: 20px; }}
        label {{ display: block; color: #4a5568; font-size: 14px; margin-bottom: 8px; font-weight: 500; }}
        input {{ width: 100%; padding: 14px 16px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 16px; transition: border-color 0.3s; }}
        input:focus {{ outline: none; border-color: #667eea; }}
        .btn {{ width: 100%; padding: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s; }}
        .btn:hover {{ transform: translateY(-2px); }}
        .info {{ background: #ebf8ff; border-radius: 10px; padding: 20px; margin-top: 30px; }}
        .info h3 {{ color: #2b6cb0; font-size: 14px; margin-bottom: 10px; }}
        .info p {{ color: #4a5568; font-size: 13px; line-height: 1.6; }}
        .dashboard {{ display: none; }}
        .dashboard.active {{ display: block; }}
        .dashboard-header {{ text-align: center; margin-bottom: 30px; }}
        .dashboard-header h2 {{ color: #1a202c; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; }}
        .stat-card.green {{ background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); }}
        .stat-card.orange {{ background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%); }}
        .stat-value {{ font-size: 28px; font-weight: 700; }}
        .stat-label {{ font-size: 12px; opacity: 0.9; margin-top: 5px; }}
        .results-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .results-table th {{ background: #667eea; color: white; padding: 12px; text-align: left; }}
        .results-table td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; }}
        .results-table tr:nth-child(even) {{ background: #f7fafc; }}
        .nav-tabs {{ display: flex; border-bottom: 2px solid #e2e8f0; margin-bottom: 20px; }}
        .nav-tab {{ flex: 1; padding: 12px; text-align: center; cursor: pointer; color: #718096; font-weight: 500; }}
        .nav-tab.active {{ color: #667eea; border-bottom: 2px solid #667eea; margin-bottom: -2px; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .logout-btn {{ background: #e53e3e; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Login Form -->
        <div id="loginSection" class="card">
            <div class="logo">
                <h1>{school['name']}</h1>
                <p>Parent & Student Portal</p>
            </div>
            
            <div class="form-group">
                <label>Student ID</label>
                <input type="text" id="studentId" placeholder="e.g., SCH/2026/001">
            </div>
            
            <div class="form-group">
                <label>Parent Phone Number</label>
                <input type="password" id="password" placeholder="Registered phone number">
            </div>
            
            <button class="btn" onclick="login()">Login</button>
            
            <div class="info">
                <h3>How to Login</h3>
                <p>Enter your child's Student ID and the parent's registered phone number to access grades, attendance, and fee information.</p>
            </div>
        </div>
        
        <!-- Dashboard -->
        <div id="dashboardSection" class="card dashboard">
            <div class="dashboard-header">
                <h2 id="welcomeText">Welcome!</h2>
                <p id="classText" style="color: #718096;"></p>
            </div>
            
            <div class="nav-tabs">
                <div class="nav-tab active" onclick="showTab('overview')">Overview</div>
                <div class="nav-tab" onclick="showTab('results')">Results</div>
                <div class="nav-tab" onclick="showTab('fees')">Fees</div>
            </div>
            
            <div id="overview" class="tab-content active">
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="feeBalance">-</div>
                        <div class="stat-label">Fee Balance</div>
                    </div>
                    <div class="stat-card green">
                        <div class="stat-value" id="attendancePct">-</div>
                        <div class="stat-label">Attendance %</div>
                    </div>
                </div>
            </div>
            
            <div id="results" class="tab-content">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Subject</th>
                            <th>CAT</th>
                            <th>Exam</th>
                            <th>Total</th>
                            <th>Grade</th>
                        </tr>
                    </thead>
                    <tbody id="resultsBody">
                    </tbody>
                </table>
            </div>
            
            <div id="fees" class="tab-content">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Amount</th>
                            <th>Receipt</th>
                        </tr>
                    </thead>
                    <tbody id="feesBody">
                    </tbody>
                </table>
            </div>
            
            <button class="btn logout-btn" onclick="logout()">Logout</button>
        </div>
    </div>
    
    <script>
        let token = localStorage.getItem('portal_token');
        let studentData = JSON.parse(localStorage.getItem('portal_student') || 'null');
        
        async function checkAuth() {{
            if (token && studentData) {{
                document.getElementById('loginSection').style.display = 'none';
                document.getElementById('dashboardSection').classList.add('active');
                loadDashboard();
            }}
        }}
        
        async function login() {{
            const studentId = document.getElementById('studentId').value;
            const password = document.getElementById('password').value;
            
            try {{
                const response = await fetch('/api/login', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ username: studentId, password: password }})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    token = data.token;
                    studentData = data.student;
                    localStorage.setItem('portal_token', token);
                    localStorage.setItem('portal_student', JSON.stringify(studentData));
                    
                    document.getElementById('loginSection').style.display = 'none';
                    document.getElementById('dashboardSection').classList.add('active');
                    loadDashboard();
                }} else {{
                    alert(data.message);
                }}
            }} catch (e) {{
                alert('Login failed: ' + e.message);
            }}
        }}
        
        async function loadDashboard() {{
            document.getElementById('welcomeText').textContent = 'Welcome, ' + studentData.name;
            document.getElementById('classText').textContent = studentData.class;
            
            try {{
                const response = await fetch('/api/dashboard', {{
                    headers: {{ 'X-Auth-Token': token }}
                }});
                const data = await response.json();
                
                document.getElementById('feeBalance').textContent = 'KES ' + data.fees.balance.toLocaleString();
                document.getElementById('attendancePct').textContent = data.attendance.percentage + '%';
            }} catch (e) {{
                console.error('Failed to load dashboard:', e);
            }}
        }}
        
        function showTab(tabId) {{
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
            
            if (tabId === 'results') loadResults();
            if (tabId === 'fees') loadFees();
        }}
        
        async function loadResults() {{
            try {{
                const response = await fetch('/api/results', {{
                    headers: {{ 'X-Auth-Token': token }}
                }});
                const data = await response.json();
                
                const tbody = document.getElementById('resultsBody');
                tbody.innerHTML = data.results.map(r => `
                    <tr>
                        <td>${{r.subject}}</td>
                        <td>${{r.cat}}</td>
                        <td>${{r.exam}}</td>
                        <td>${{r.total}}</td>
                        <td><strong>${{r.grade}}</strong></td>
                    </tr>
                `).join('');
            }} catch (e) {{
                console.error('Failed to load results:', e);
            }}
        }}
        
        async function loadFees() {{
            try {{
                const response = await fetch('/api/fees', {{
                    headers: {{ 'X-Auth-Token': token }}
                }});
                const data = await response.json();
                
                const tbody = document.getElementById('feesBody');
                tbody.innerHTML = data.payments.map(p => `
                    <tr>
                        <td>${{p.date}}</td>
                        <td>KES ${{p.amount.toLocaleString()}}</td>
                        <td>${{p.receipt}}</td>
                    </tr>
                `).join('');
            }} catch (e) {{
                console.error('Failed to load fees:', e);
            }}
        }}
        
        function logout() {{
            localStorage.removeItem('portal_token');
            localStorage.removeItem('portal_student');
            location.reload();
        }}
        
        checkAuth();
    </script>
</body>
</html>
"""
    
    def generate_qr_code(self):
        """Generate QR code for portal URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.base_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    async def start(self):
        """Start the portal server"""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.local_ip, self.port)
        await self.site.start()
        return f"Portal started at {self.base_url}"
    
    async def stop(self):
        """Stop the portal server"""
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()


class PortalManager:
    """Manage the LAN portal server"""
    
    def __init__(self, db_session):
        self.db_session = db_session
        self.server = None
        self._server_thread = None
    
    def start_server(self, port=8000):
        """Start the portal server in a background thread"""
        self.server = LANPortalServer(self.db_session, port)
        
        import asyncio
        
        async def run_server():
            await self.server.start()
            # Keep running
            while True:
                await asyncio.sleep(3600)
        
        def run():
            asyncio.run(run_server())
        
        import threading
        self._server_thread = threading.Thread(target=run, daemon=True)
        self._server_thread.start()
        
        return self.server.base_url, self.server.local_ip, port
    
    def stop_server(self):
        """Stop the portal server"""
        if self.server:
            import asyncio
            asyncio.run(self.server.stop())
    
    def get_portal_url(self):
        """Get current portal URL"""
        if self.server:
            return self.server.base_url
        return None
    
    def get_local_ip(self):
        """Get server's local IP address"""
        if self.server:
            return self.server.local_ip
        return None
    
    def get_qr_code_base64(self):
        """Get QR code as base64 string"""
        if self.server:
            return self.server.generate_qr_code()
        return None
    
    def get_qr_image_path(self, output_path=None):
        """Generate QR code image file"""
        if not self.server:
            return None
        
        if output_path is None:
            output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'portal_qr.png')
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.server.base_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        
        return output_path
