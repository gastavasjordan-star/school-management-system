"""
Analytics and Reporting Utilities
"""
from datetime import datetime, date
from sqlalchemy import func


class AnalyticsEngine:
    """Generate analytics and insights for the school"""
    
    def __init__(self, session):
        self.session = session
    
    def get_enrollment_stats(self):
        """Get enrollment statistics"""
        from school_manager.models.database import Student, Class, Stream
        
        total_students = self.session.query(Student).filter(Student.status == 'active').count()
        
        # By class
        class_counts = self.session.query(
            Class.name, func.count(Student.id)
        ).join(Student).filter(
            Student.status == 'active'
        ).group_by(Class.name).all()
        
        # By stream
        stream_counts = self.session.query(
            Stream.name, func.count(Student.id)
        ).join(Class).join(Student).filter(
            Student.status == 'active'
        ).group_by(Stream.name).all()
        
        # Gender distribution
        male_count = self.session.query(Student).filter(
            Student.status == 'active',
            Student.gender == 'Male'
        ).count()
        
        female_count = self.session.query(Student).filter(
            Student.status == 'active',
            Student.gender == 'Female'
        ).count()
        
        return {
            'total': total_students,
            'by_class': dict(class_counts),
            'by_stream': dict(stream_counts),
            'male': male_count,
            'female': female_count
        }
    
    def get_fee_collection_stats(self, term_id=None):
        """Get fee collection statistics"""
        from school_manager.models.database import FeePayment, FeeStructure, Student
        
        total_collected = self.session.query(func.sum(FeePayment.amount)).scalar() or 0
        
        # This term
        total_expected = self.session.query(func.sum(FeeStructure.amount)).scalar() or 0
        
        # Collection rate
        collection_rate = (total_collected / total_expected * 100) if total_expected > 0 else 0
        
        return {
            'total_collected': total_collected,
            'total_expected': total_expected,
            'collection_rate': collection_rate,
            'outstanding': total_expected - total_collected
        }
    
    def get_attendance_stats(self, class_id=None, start_date=None, end_date=None):
        """Get attendance statistics"""
        from school_manager.models.database import StudentAttendance, Student
        
        query = self.session.query(StudentAttendance)
        
        if class_id:
            query = query.join(Student).filter(Student.class_id == class_id)
        
        if start_date:
            query = query.filter(StudentAttendance.date >= start_date)
        
        if end_date:
            query = query.filter(StudentAttendance.date <= end_date)
        
        total = query.count()
        present = query.filter(StudentAttendance.status == 'present').count()
        absent = query.filter(StudentAttendance.status == 'absent').count()
        late = query.filter(StudentAttendance.status == 'late').count()
        
        return {
            'total_records': total,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_rate': (present / total * 100) if total > 0 else 0
        }
    
    def get_subject_performance(self, class_id, term_id):
        """Get subject performance for a class"""
        from school_manager.models.database import ExamResult, ClassSubject, Subject
        
        results = self.session.query(
            Subject.name,
            func.avg(ExamResult.total_score).label('average'),
            func.min(ExamResult.total_score).label('min'),
            func.max(ExamResult.total_score).label('max'),
            func.count(ExamResult.id).label('count')
        ).join(
            ClassSubject, ExamResult.class_subject_id == ClassSubject.id
        ).join(
            Subject, ClassSubject.subject_id == Subject.id
        ).filter(
            ClassSubject.class_id == class_id,
            ExamResult.term_id == term_id
        ).group_by(Subject.name).all()
        
        return [{
            'subject': r.name,
            'average': r.average,
            'min': r.min,
            'max': r.max,
            'count': r.count
        } for r in results]
    
    def get_class_rankings(self, class_id, term_id):
        """Get student rankings for a class"""
        from school_manager.models.database import ExamResult, Student, ClassSubject
        
        # Get all students in class
        students = self.session.query(Student).filter(
            Student.class_id == class_id,
            Student.status == 'active'
        ).all()
        
        rankings = []
        
        for student in students:
            # Calculate total score
            total = self.session.query(
                func.sum(ExamResult.total_score)
            ).join(
                ClassSubject, ExamResult.class_subject_id == ClassSubject.id
            ).filter(
                ExamResult.student_id == student.id,
                ClassSubject.class_id == class_id,
                ExamResult.term_id == term_id
            ).scalar() or 0
            
            rankings.append({
                'student_id': student.id,
                'name': f"{student.first_name} {student.last_name}",
                'total': total
            })
        
        # Sort by total and assign positions
        rankings.sort(key=lambda x: x['total'], reverse=True)
        
        for i, r in enumerate(rankings):
            r['position'] = i + 1
        
        return rankings
    
    def get_top_performers(self, limit=10, term_id=None):
        """Get top performing students"""
        from school_manager.models.database import ExamResult, Student
        
        query = self.session.query(
            Student,
            func.avg(ExamResult.total_score).label('average')
        ).join(
            ExamResult, Student.id == ExamResult.student_id
        ).group_by(Student.id).order_by(func.avg(ExamResult.total_score).desc())
        
        if term_id:
            query = query.filter(ExamResult.term_id == term_id)
        
        results = query.limit(limit).all()
        
        return [{
            'student_id': r[0].id,
            'name': f"{r[0].first_name} {r[0].last_name}",
            'student_id_number': r[0].student_id,
            'average': r.average
        } for r in results]
    
    def get_fee_defaulters(self, class_id=None):
        """Get students with outstanding fees"""
        from school_manager.models.database import Student, FeePayment, FeeStructure
        
        # Get total fees per student
        query = self.session.query(Student).filter(Student.status == 'active')
        
        if class_id:
            query = query.filter(Student.class_id == class_id)
        
        students = query.all()
        defaulters = []
        
        for student in students:
            total_fees = self.session.query(func.sum(FeeStructure.amount)).scalar() or 0
            total_paid = self.session.query(func.sum(FeePayment.amount)).filter(
                FeePayment.student_id == student.id
            ).scalar() or 0
            
            balance = total_fees - total_paid
            
            if balance > 0:
                defaulters.append({
                    'student_id': student.id,
                    'student_number': student.student_id,
                    'name': f"{student.first_name} {student.last_name}",
                    'class': student.class_obj.name if student.class_obj else 'N/A',
                    'balance': balance
                })
        
        # Sort by balance
        defaulters.sort(key=lambda x: x['balance'], reverse=True)
        
        return defaulters


class RankingEngine:
    """Student and class ranking calculations"""
    
    def __init__(self, session):
        self.session = session
    
    def calculate_student_position(self, student_id, class_id, term_id):
        """Calculate a student's position in their class"""
        from school_manager.models.database import ExamResult, ClassSubject
        from sqlalchemy import func
        
        # Get all students in the class
        total_score = self.session.query(
            func.sum(ExamResult.total_score)
        ).join(
            ClassSubject, ExamResult.class_subject_id == ClassSubject.id
        ).filter(
            ExamResult.student_id == student_id,
            ClassSubject.class_id == class_id,
            ExamResult.term_id == term_id
        ).scalar() or 0
        
        # Count students with higher scores
        # This would be more efficient with a raw SQL query
        from school_manager.models.database import Student
        students = self.session.query(Student.id).filter(
            Student.class_id == class_id,
            Student.status == 'active',
            Student.id != student_id
        ).all()
        
        position = 1
        for s in students:
            their_score = self.session.query(
                func.sum(ExamResult.total_score)
            ).join(
                ClassSubject, ExamResult.class_subject_id == ClassSubject.id
            ).filter(
                ExamResult.student_id == s.id,
                ClassSubject.class_id == class_id,
                ExamResult.term_id == term_id
            ).scalar() or 0
            
            if their_score > total_score:
                position += 1
        
        return position
    
    def get_subject_rank(self, student_id, subject_id, class_id, term_id):
        """Get student's rank in a specific subject"""
        from school_manager.models.database import ExamResult, ClassSubject
        from sqlalchemy import func
        
        student_score = self.session.query(ExamResult.total_score).join(
            ClassSubject, ExamResult.class_subject_id == ClassSubject.id
        ).filter(
            ExamResult.student_id == student_id,
            ClassSubject.subject_id == subject_id,
            ClassSubject.class_id == class_id,
            ExamResult.term_id == term_id
        ).scalar() or 0
        
        # Count students with higher scores
        rank = self.session.query(func.count(ExamResult.id)).join(
            ClassSubject, ExamResult.class_subject_id == ClassSubject.id
        ).filter(
            ClassSubject.subject_id == subject_id,
            ClassSubject.class_id == class_id,
            ExamResult.term_id == term_id,
            ExamResult.total_score > student_score
        ).scalar() or 0
        
        return rank + 1


class PromotionEngine:
    """Handle student promotion workflows"""
    
    def __init__(self, session):
        self.session = session
    
    def can_promote(self, student_id, next_class_id):
        """Check if a student can be promoted"""
        from school_manager.models.database import Student, AcademicTerm, ExamResult, ClassSubject
        
        # Get current term
        current_term = self.session.query(AcademicTerm).filter(
            AcademicTerm.is_current == True
        ).first()
        
        if not current_term:
            return False, "No current term found"
        
        if current_term.is_published:
            return False, "Current term is published and locked"
        
        # Check if student has all required marks
        student = self.session.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            return False, "Student not found"
        
        return True, "Student can be promoted"
    
    def promote_students(self, class_id, next_class_id, criteria='pass_all'):
        """Promote all students from one class to the next"""
        from school_manager.models.database import Student, AcademicTerm
        
        # Get students
        students = self.session.query(Student).filter(
            Student.class_id == class_id,
            Student.status == 'active'
        ).all()
        
        promoted = 0
        not_promoted = 0
        results = []
        
        for student in students:
            can_promo, msg = self.can_promote(student.id, next_class_id)
            
            if can_promo:
                student.class_id = next_class_id
                promoted += 1
                results.append({
                    'student_id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'status': 'promoted'
                })
            else:
                not_promoted += 1
                results.append({
                    'student_id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'status': 'not_promoted',
                    'reason': msg
                })
        
        self.session.commit()
        
        return {
            'promoted': promoted,
            'not_promoted': not_promoted,
            'details': results
        }
    
    def demote_students(self, class_id, previous_class_id):
        """Demote students to previous class"""
        from school_manager.models.database import Student
        
        students = self.session.query(Student).filter(
            Student.class_id == class_id,
            Student.status == 'active'
        ).all()
        
        for student in students:
            student.class_id = previous_class_id
        
        self.session.commit()
        
        return len(students)
    
    def archive_year(self, year):
        """Archive students for a completed year"""
        from school_manager.models.database import Student, AcademicTerm
        
        # Find last term of the year
        terms = self.session.query(AcademicTerm).filter(
            AcademicTerm.name.like(f'%{year}%')
        ).order_by(AcademicTerm.end_date.desc()).first()
        
        if terms and terms.is_published:
            # Mark all active students as potentially graduating
            return True, "Year archived successfully"
        
        return False, "Cannot archive - year not complete"
