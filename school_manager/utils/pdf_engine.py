"""
Modern PDF Engine for Report Cards, ID Cards, and Documents
"""
import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
                                 Image, HRFlowable, PageBreak)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from PIL import Image as PILImage


class PDFStyles:
    """Color palette and styling constants"""
    BG_LIGHT = HexColor('#f8fafc')
    CARD_WHITE = HexColor('#ffffff')
    TEXT_DARK = HexColor('#0f172a')
    ACCENT_BLUE = HexColor('#2563eb')
    ACCENT_LIGHT = HexColor('#dbeafe')
    SUCCESS_GREEN = HexColor('#16a34a')
    WARNING_ORANGE = HexColor('#ea580c')
    BORDER_GRAY = HexColor('#e2e8f0')
    GRADIENT_START = HexColor('#1e40af')
    GRADIENT_END = HexColor('#3b82f6')


class SchoolPDFGenerator:
    """Generate professional school documents"""
    
    def __init__(self, school_info=None):
        self.school = school_info or {
            'name': 'School Name',
            'address': 'School Address',
            'phone': 'Phone',
            'email': 'email@school.com',
            'website': 'www.school.com',
            'logo_path': None,
            'stamp_path': None,
            'signature_path': None,
            'motto': ''
        }
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='SchoolName',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=self.school.get('name_color', PDFStyles.TEXT_DARK),
            alignment=TA_CENTER,
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='SchoolAddress',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=PDFStyles.TEXT_DARK,
            alignment=TA_CENTER,
            spaceAfter=2
        ))
        self.styles.add(ParagraphStyle(
            name='DocTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=PDFStyles.ACCENT_BLUE,
            alignment=TA_CENTER,
            spaceBefore=10,
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=white,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='StudentName',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=PDFStyles.TEXT_DARK,
            alignment=TA_CENTER
        ))
    
    def draw_curved_header(self, c, page_width, page_height):
        """Draw a modern curved header with school branding"""
        # Background gradient effect using rectangles
        y_start = page_height - 2*inch
        
        # Draw gradient background
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.rect(0, y_start, page_width, page_height - y_start, fill=True, stroke=False)
        
        # Draw curved overlay
        c.setFillColor(PDFStyles.GRADIENT_START)
        c.circle(page_width/2, y_start, page_width/2, fill=True, stroke=False)
        
        # White curved section at bottom
        c.setFillColor(white)
        c.rect(0, y_start - 0.5*inch, page_width, 0.6*inch, fill=True, stroke=False)
        
        # Draw school info on header
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 20)
        
        # Center school name
        text_width = c.stringWidth(self.school['name'], "Helvetica-Bold", 20)
        c.drawString((page_width - text_width)/2, page_height - 0.7*inch, self.school['name'])
        
        # Draw contact info
        c.setFont("Helvetica", 9)
        contact_info = f"{self.school['address']} | Tel: {self.school['phone']} | {self.school['email']}"
        text_width = c.stringWidth(contact_info, "Helvetica", 9)
        c.drawString((page_width - text_width)/2, page_height - 1*inch, contact_info)
        
        # Draw logo if available
        if self.school.get('logo_path') and os.path.exists(self.school['logo_path']):
            try:
                img = PILImage.open(self.school['logo_path'])
                img_width, img_height = img.size
                max_width = 0.8*inch
                max_height = 0.8*inch
                
                # Scale to fit
                ratio = min(max_width/img_width, max_height/img_height)
                final_width = img_width * ratio
                final_height = img_height * ratio
                
                c.drawImage(self.school['logo_path'], 0.5*inch, page_height - 1.1*inch - final_height/2,
                           width=final_width, height=final_height, preserveAspectRatio=True)
            except:
                pass
        
        # Draw motto
        if self.school.get('motto'):
            c.setFont("Helvetica-Oblique", 10)
            c.setFillColor(PDFStyles.ACCENT_LIGHT)
            text_width = c.stringWidth(f'"{self.school["motto"]}"', "Helvetica-Oblique", 10)
            c.drawString((page_width - text_width)/2, page_height - 1.4*inch, f'"{self.school["motto"]}"')
    
    def draw_footer(self, c, page_width, page_height, page_num, total_pages):
        """Draw footer with page numbers"""
        c.setFillColor(PDFStyles.BORDER_GRAY)
        c.rect(0, 0, page_width, 0.5*inch, fill=True, stroke=False)
        
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica", 8)
        
        # Footer text
        footer_text = f"Generated on {datetime.now().strftime('%d %B %Y %H:%M')}"
        c.drawString(0.5*inch, 0.2*inch, footer_text)
        
        # Page number
        page_text = f"Page {page_num} of {total_pages}"
        text_width = c.stringWidth(page_text, "Helvetica", 8)
        c.drawString(page_width - 0.5*inch - text_width, 0.2*inch, page_text)


class ReportCardGenerator(SchoolPDFGenerator):
    """Generate student report cards"""
    
    def __init__(self, school_info=None, settings=None):
        super().__init__(school_info)
        self.settings = settings or {}
    
    def generate_report_card(self, student, results, term_info, class_position=None, comments=None):
        """Generate a complete report card PDF"""
        buffer = BytesIO()
        page_width, page_height = A4
        
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Page 1: Report Cover
        self._draw_report_page(c, student, results, term_info, class_position, comments, page_width, page_height, 1, 1)
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _draw_report_page(self, c, student, results, term_info, class_position, comments, page_width, page_height, page_num, total_pages):
        """Draw a single report card page"""
        # Draw curved header
        self.draw_curved_header(c, page_width, page_height)
        
        y_pos = page_height - 2.5*inch
        
        # Document title
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.setFont("Helvetica-Bold", 14)
        title = f"END OF {term_info['name'].upper()} REPORT"
        text_width = c.stringWidth(title, "Helvetica-Bold", 14)
        c.drawString((page_width - text_width)/2, y_pos, title)
        
        y_pos -= 0.4*inch
        
        # Student info card
        self._draw_student_card(c, student, term_info, class_position, y_pos, page_width)
        
        y_pos -= 2.2*inch
        
        # Results table
        self._draw_results_table(c, results, y_pos, page_width)
        
        # Draw footer
        self.draw_footer(c, page_width, page_height, page_num, total_pages)
        
        # Draw comments section
        if comments:
            self._draw_comments(c, comments, page_width)
    
    def _draw_student_card(self, c, student, term_info, class_position, y_pos, page_width):
        """Draw student information card"""
        card_left = 0.8*inch
        card_width = page_width - 1.6*inch
        card_height = 1.8*inch
        
        # Card background
        c.setFillColor(PDFStyles.CARD_WHITE)
        c.setStrokeColor(PDFStyles.BORDER_GRAY)
        c.roundRect(card_left, y_pos - card_height, card_width, card_height, 10, fill=True, stroke=True)
        
        # Student photo placeholder
        photo_x = card_left + 0.2*inch
        photo_size = 1.2*inch
        
        if student.get('photo_path') and os.path.exists(student['photo_path']):
            c.drawImage(student['photo_path'], photo_x, y_pos - card_height + 0.3*inch,
                       width=photo_size, height=photo_size, preserveAspectRatio=True)
        else:
            c.setFillColor(PDFStyles.ACCENT_LIGHT)
            c.circle(photo_x + photo_size/2, y_pos - card_height/2, photo_size/2, fill=True, stroke=False)
            c.setFillColor(PDFStyles.ACCENT_BLUE)
            c.setFont("Helvetica-Bold", 24)
            initials = f"{student['first_name'][0]}{student['last_name'][0]}"
            text_width = c.stringWidth(initials, "Helvetica-Bold", 24)
            c.drawString(photo_x + (photo_size - text_width)/2, y_pos - card_height/2 - 8, initials)
        
        # Student details
        details_x = photo_x + photo_size + 0.4*inch
        c.setFillColor(PDFStyles.TEXT_DARK)
        
        details = [
            ("Student Name:", f"{student['first_name']} {student['last_name']}"),
            ("Student ID:", student['student_id']),
            ("Class:", student.get('class_name', 'N/A')),
            ("Term:", term_info['name']),
            ("Position:", class_position or 'N/A'),
        ]
        
        y_offset = y_pos - 0.35*inch
        for label, value in details:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(details_x, y_offset, label)
            c.setFont("Helvetica", 10)
            c.drawString(details_x + 1.2*inch, y_offset, str(value))
            y_offset -= 0.28*inch
    
    def _draw_results_table(self, c, results, y_pos, page_width):
        """Draw exam results table"""
        table_left = 0.8*inch
        col_widths = [2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.6*inch]
        row_height = 0.35*inch
        
        # Header
        headers = ['Subject', 'CAT (30)', 'Exam (70)', 'Total', 'Grade', 'Rank']
        
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.rect(table_left, y_pos, sum(col_widths), row_height, fill=True, stroke=False)
        
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 9)
        
        x = table_left + 0.1*inch
        for i, header in enumerate(headers):
            c.drawString(x, y_pos + 0.12*inch, header)
            x += col_widths[i]
        
        # Data rows
        y_pos -= row_height
        row_count = 0
        
        for subject, data in results.items():
            bg_color = PDFStyles.CARD_WHITE if row_count % 2 == 0 else PDFStyles.BG_LIGHT
            c.setFillColor(bg_color)
            c.rect(table_left, y_pos - row_height, sum(col_widths), row_height, fill=True, stroke=False)
            
            c.setFillColor(PDFStyles.TEXT_DARK)
            c.setFont("Helvetica", 9)
            
            values = [subject, str(data.get('cat', '-')), str(data.get('exam', '-')), 
                     str(data.get('total', '-')), data.get('grade', '-'), str(data.get('rank', '-'))]
            
            x = table_left + 0.1*inch
            for i, val in enumerate(values):
                if i == 4:  # Grade
                    c.setFont("Helvetica-Bold", 9)
                    grade = val
                    if grade in ['A', 'A+']:
                        c.setFillColor(PDFStyles.SUCCESS_GREEN)
                    elif grade in ['B', 'C']:
                        c.setFillColor(PDFStyles.ACCENT_BLUE)
                    elif grade in ['D', 'E']:
                        c.setFillColor(PDFStyles.WARNING_ORANGE)
                    else:
                        c.setFillColor(PDFStyles.TEXT_DARK)
                c.drawString(x, y_pos - row_height + 0.1*inch, str(val))
                if i == 4:
                    c.setFillColor(PDFStyles.TEXT_DARK)
                x += col_widths[i]
            
            y_pos -= row_height
            row_count += 1
    
    def _draw_comments(self, c, comments, page_width):
        """Draw teacher comments section"""
        y_pos = 1.5*inch
        
        # Comments box
        c.setFillColor(PDFStyles.CARD_WHITE)
        c.setStrokeColor(PDFStyles.BORDER_GRAY)
        c.roundRect(0.8*inch, y_pos - 1.2*inch, page_width - 1.6*inch, 1.2*inch, 5, fill=True, stroke=True)
        
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_pos - 0.2*inch, "Class Teacher's Comment:")
        
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(1.2*inch, y_pos - 0.5*inch, comments.get('class_teacher', 'Good performance.'))
        
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_pos - 0.8*inch, "Head Teacher's Comment:")
        
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(1.2*inch, y_pos - 1.05*inch, comments.get('head_teacher', 'Keep up the good work.'))


class IDCardGenerator(SchoolPDFGenerator):
    """Generate student ID cards in A4 grid format"""
    
    def __init__(self, school_info=None, template='standard'):
        super().__init__(school_info)
        self.template = template
    
    def generate_id_grid(self, students, cards_per_row=3):
        """Generate A4 grid of ID cards"""
        buffer = BytesIO()
        page_width, page_height = A4
        
        c = canvas.Canvas(buffer, pagesize=A4)
        
        margin = 0.5*inch
        page_width_inner = page_width - 2*margin
        
        # Card dimensions
        card_width = page_width_inner / cards_per_row
        card_height = 2.1*inch  # Credit card ratio-ish
        card_spacing = 0.15*inch
        
        rows_per_page = int((page_height - 2*margin) / (card_height + card_spacing))
        cards_per_page = cards_per_row * rows_per_page
        
        card_count = 0
        
        for student in students:
            page_num = card_count // cards_per_page
            if page_num > 0:
                c.showPage()
                card_count = 0
            
            row = card_count // cards_per_row
            col = card_count % cards_per_row
            
            x = margin + col * card_width + card_spacing/2
            y = page_height - margin - (row + 1) * card_height - row * card_spacing
            
            self._draw_id_card(c, student, x, y, card_width, card_height)
            
            # Draw cutting guides
            c.setStrokeColor(PDFStyles.BORDER_GRAY)
            c.setLineWidth(0.5)
            c.setDash([2, 2])
            c.rect(x, y, card_width - card_spacing, card_height)
            c.setDash([])
            
            card_count += 1
        
        # Draw cutting guides on last page
        if students:
            c.showPage()
            # Print last page as cutting guide
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _draw_id_card(self, c, student, x, y, width, height):
        """Draw a single ID card"""
        # Card background with gradient effect
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.roundRect(x, y, width, height, 8, fill=True, stroke=False)
        
        # Top colored strip
        c.setFillColor(PDFStyles.GRADIENT_START)
        c.roundRect(x, y + height - 0.8*inch, width, 0.8*inch, 8, fill=True, stroke=False)
        c.rect(x, y + height - 0.4*inch, width, 0.4*inch, fill=True, stroke=False)
        
        # School name on card
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        school_name = self.school['name'][:25] if len(self.school['name']) > 25 else self.school['name']
        text_width = c.stringWidth(school_name, "Helvetica-Bold", 8)
        c.drawString(x + (width - text_width)/2, y + height - 0.5*inch, school_name)
        
        # Photo area
        photo_x = x + 0.15*inch
        photo_size = 0.9*inch
        photo_y = y + height - photo_size - 0.3*inch - 0.5*inch
        
        c.setFillColor(white)
        c.roundRect(photo_x, photo_y, photo_size, photo_size, 5, fill=True, stroke=False)
        
        if student.get('photo_path') and os.path.exists(student['photo_path']):
            c.drawImage(student['photo_path'], photo_x, photo_y, width=photo_size, height=photo_size,
                       preserveAspectRatio=True)
        else:
            c.setFillColor(PDFStyles.ACCENT_LIGHT)
            c.circle(photo_x + photo_size/2, photo_y + photo_size/2, photo_size/3, fill=True, stroke=False)
        
        # Student info
        info_x = photo_x + photo_size + 0.15*inch
        info_y = photo_y + photo_size - 0.2*inch
        
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        
        name = f"{student['first_name']} {student['last_name']}"
        if len(name) > 18:
            name = name[:16] + '..'
        c.drawString(info_x, info_y, name)
        
        c.setFont("Helvetica", 6)
        c.setFillColor(PDFStyles.ACCENT_LIGHT)
        
        fields = [
            ("ID:", student.get('student_id', 'N/A')),
            ("Class:", student.get('class_name', 'N/A')),
            ("Gender:", student.get('gender', 'N/A')),
        ]
        
        for label, value in fields:
            c.drawString(info_x, info_y - 0.2*inch * (fields.index((label, value)) + 1), f"{label} {value}")
        
        # Footer with barcode placeholder
        c.setFillColor(white)
        c.rect(x + 0.1*inch, y + 0.1*inch, width - 0.2*inch, 0.3*inch, fill=True, stroke=False)
        
        # QR code area
        qr_size = 0.25*inch
        c.drawRect(x + width - qr_size - 0.15*inch, y + 0.1*inch, qr_size, qr_size, fill=True, stroke=False)
        
        c.setFillColor(PDFStyles.GRADIENT_START)
        c.setFont("Helvetica-Bold", 5)
        c.drawString(x + 0.15*inch, y + 0.2*inch, "STUDENT ID CARD")


class FeeDemandLetterGenerator(SchoolPDFGenerator):
    """Generate fee demand letters"""
    
    def __init__(self, school_info=None):
        super().__init__(school_info)
    
    def generate_letter(self, student, fee_info, balance_info):
        """Generate a fee demand letter PDF"""
        buffer = BytesIO()
        page_width, page_height = A4
        
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Header
        self.draw_curved_header(c, page_width, page_height)
        
        y_pos = page_height - 2.8*inch
        
        # Letter title
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, y_pos, "FEE DEMAND NOTICE")
        
        y_pos -= 0.4*inch
        
        # Date and reference
        c.setFont("Helvetica", 10)
        c.drawString(1*inch, y_pos, f"Date: {datetime.now().strftime('%d %B %Y')}")
        
        y_pos -= 0.3*inch
        
        # Parent/Guardian address
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_pos, "To:")
        c.setFont("Helvetica", 10)
        y_pos -= 0.2*inch
        c.drawString(1.2*inch, y_pos, f"{fee_info.get('parent_name', 'Parent/Guardian')}")
        y_pos -= 0.2*inch
        c.drawString(1.2*inch, y_pos, f"Parent of: {student['first_name']} {student['last_name']}")
        y_pos -= 0.2*inch
        c.drawString(1.2*inch, y_pos, f"Student ID: {student['student_id']}")
        
        y_pos -= 0.4*inch
        
        # Letter body
        c.setFont("Helvetica", 10)
        c.drawString(1*inch, y_pos, "Dear Parent/Guardian,")
        
        y_pos -= 0.3*inch
        
        body_text = f"""This letter serves to inform you that there is an outstanding fee balance 
of {balance_info['currency']} {balance_info['amount']:.2f} for your child, {student['first_name']} {student['last_name']} 
(Student ID: {student['student_id']}), Class {student.get('class_name', 'N/A')}."""
        
        # Split into lines
        lines = []
        words = body_text.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            if c.stringWidth(test_line, "Helvetica", 10) < 6*inch:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        
        for line in lines:
            c.drawString(1*inch, y_pos, line)
            y_pos -= 0.22*inch
        
        y_pos -= 0.2*inch
        
        # Fee breakdown table
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_pos, "Fee Breakdown:")
        
        y_pos -= 0.3*inch
        
        # Table
        table_data = [['Description', 'Amount', 'Status']]
        for fee in fee_info.get('fees', []):
            table_data.append([fee['name'], f"{balance_info['currency']} {fee['amount']:.2f}", fee['status']])
        
        table_data.append(['', '', ''])
        table_data.append(['Total Outstanding', f"{balance_info['currency']} {balance_info['amount']:.2f}", 'UNPAID'])
        
        t = Table(table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PDFStyles.ACCENT_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, -1), (-1, -1), PDFStyles.ACCENT_LIGHT),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, PDFStyles.BORDER_GRAY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [PDFStyles.CARD_WHITE, PDFStyles.BG_LIGHT]),
        ]))
        
        t.wrapOn(c, 6*inch, 4*inch)
        t.drawOn(c, 1*inch, y_pos - len(table_data) * 0.3*inch)
        
        y_pos -= len(table_data) * 0.3*inch + 0.5*inch
        
        # Payment instructions
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_pos, "Payment Instructions:")
        
        y_pos -= 0.25*inch
        c.setFont("Helvetica", 10)
        c.drawString(1*inch, y_pos, f"Bank: {fee_info.get('bank_name', 'N/A')}")
        y_pos -= 0.2*inch
        c.drawString(1*inch, y_pos, f"Account: {fee_info.get('account_number', 'N/A')}")
        y_pos -= 0.2*inch
        c.drawString(1*inch, y_pos, f"Account Name: {fee_info.get('account_name', 'N/A')}")
        
        y_pos -= 0.4*inch
        
        # Closing
        c.drawString(1*inch, y_pos, "Please make payment on or before the due date to avoid any inconvenience.")
        
        y_pos -= 0.3*inch
        c.drawString(1*inch, y_pos, "Yours faithfully,")
        
        y_pos -= 0.5*inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_pos, "SCHOOL ADMINISTRATION")
        
        # Signature
        if self.school.get('signature_path') and os.path.exists(self.school['signature_path']):
            c.drawImage(self.school['signature_path'], 1*inch, y_pos - 0.8*inch, 
                       width=1.5*inch, height=0.7*inch, preserveAspectRatio=True)
        
        # Stamp
        if self.school.get('stamp_path') and os.path.exists(self.school['stamp_path']):
            c.drawImage(self.school['stamp_path'], 3*inch, y_pos - 0.8*inch,
                       width=1*inch, height=1*inch, preserveAspectRatio=True)
        
        # Footer
        self.draw_footer(c, page_width, page_height, 1, 1)
        
        c.save()
        buffer.seek(0)
        return buffer


class ReceiptGenerator(SchoolPDFGenerator):
    """Generate payment receipts"""
    
    def __init__(self, school_info=None, size='A5'):
        super().__init__(school_info)
        self.size = size  # A4, A5, Thermal (80mm)
    
    def generate_receipt(self, payment, student, fee_info):
        """Generate a payment receipt"""
        buffer = BytesIO()
        
        if self.size == 'A4':
            page_width, page_height = A4
        elif self.size == 'Thermal':
            page_width = 3*inch
            page_height = 8*inch
        else:  # A5
            page_width, page_height = A5
        
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        
        margin = 0.3*inch
        
        # Header
        y_pos = page_height - 0.8*inch
        
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.rect(margin, y_pos - 0.5*inch, page_width - 2*margin, 0.5*inch, fill=True, stroke=False)
        
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 12)
        title = "OFFICIAL RECEIPT"
        text_width = c.stringWidth(title, "Helvetica-Bold", 12)
        c.drawString((page_width - text_width)/2, y_pos - 0.35*inch, title)
        
        y_pos -= 0.7*inch
        
        # Receipt details
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica", 9)
        
        details = [
            ("Receipt No:", payment.get('receipt_number', 'N/A')),
            ("Date:", payment.get('payment_date', datetime.now().strftime('%d %B %Y'))),
            ("Time:", datetime.now().strftime('%H:%M:%S')),
        ]
        
        for label, value in details:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(margin + 0.1*inch, y_pos, label)
            c.setFont("Helvetica", 9)
            c.drawString(margin + 1.2*inch, y_pos, str(value))
            y_pos -= 0.25*inch
        
        y_pos -= 0.1*inch
        
        # Divider
        c.setStrokeColor(PDFStyles.BORDER_GRAY)
        c.line(margin, y_pos, page_width - margin, y_pos)
        y_pos -= 0.2*inch
        
        # Student info
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 0.1*inch, y_pos, "Student Information")
        y_pos -= 0.2*inch
        
        c.setFont("Helvetica", 9)
        c.drawString(margin + 0.1*inch, y_pos, f"Name: {student['first_name']} {student['last_name']}")
        y_pos -= 0.18*inch
        c.drawString(margin + 0.1*inch, y_pos, f"ID: {student['student_id']}")
        y_pos -= 0.18*inch
        c.drawString(margin + 0.1*inch, y_pos, f"Class: {student.get('class_name', 'N/A')}")
        
        y_pos -= 0.3*inch
        
        # Divider
        c.line(margin, y_pos, page_width - margin, y_pos)
        y_pos -= 0.2*inch
        
        # Payment details
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 0.1*inch, y_pos, "Payment Details")
        y_pos -= 0.2*inch
        
        c.setFont("Helvetica", 9)
        c.drawString(margin + 0.1*inch, y_pos, f"Amount: {fee_info.get('currency', 'KES')} {payment.get('amount', 0):,.2f}")
        y_pos -= 0.18*inch
        c.drawString(margin + 0.1*inch, y_pos, f"Mode: {payment.get('payment_method', 'Cash')}")
        y_pos -= 0.18*inch
        
        if payment.get('reference'):
            c.drawString(margin + 0.1*inch, y_pos, f"Ref: {payment['reference']}")
            y_pos -= 0.18*inch
        
        y_pos -= 0.2*inch
        
        # Total box
        c.setFillColor(PDFStyles.ACCENT_LIGHT)
        c.rect(margin + 0.1*inch, y_pos - 0.4*inch, page_width - 2*margin - 0.2*inch, 0.4*inch, fill=True, stroke=False)
        
        c.setFillColor(PDFStyles.ACCENT_BLUE)
        c.setFont("Helvetica-Bold", 10)
        total_text = f"TOTAL PAID: {fee_info.get('currency', 'KES')} {payment.get('amount', 0):,.2f}"
        text_width = c.stringWidth(total_text, "Helvetica-Bold", 10)
        c.drawString((page_width - text_width)/2, y_pos - 0.3*inch, total_text)
        
        y_pos -= 0.6*inch
        
        # Balance info
        if fee_info.get('balance', 0) > 0:
            c.setFillColor(PDFStyles.WARNING_ORANGE)
            c.setFont("Helvetica-Bold", 9)
            balance_text = f"Balance: {fee_info.get('currency', 'KES')} {fee_info['balance']:,.2f}"
            c.drawString(margin + 0.1*inch, y_pos, balance_text)
            y_pos -= 0.3*inch
        
        # Footer
        y_pos -= 0.2*inch
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica", 8)
        footer = "Thank you for your payment. Please retain this receipt for your records."
        text_width = c.stringWidth(footer, "Helvetica", 8)
        c.drawString((page_width - text_width)/2, y_pos, footer)
        
        # Signature
        y_pos -= 0.4*inch
        c.line(margin + 0.5*inch, y_pos, margin + 2*inch, y_pos)
        c.setFont("Helvetica", 7)
        c.drawString(margin + 0.5*inch, y_pos - 0.15*inch, "Bursar's Signature")
        
        c.save()
        buffer.seek(0)
        return buffer


def generate_broadsheet(student_results, class_info, term_info):
    """Generate class broadsheet for teachers"""
    buffer = BytesIO()
    page_width, page_height = A4
    
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Header
    c.setFillColor(PDFStyles.ACCENT_BLUE)
    c.rect(0, page_height - 0.6*inch, page_width, 0.6*inch, fill=True, stroke=False)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.5*inch, page_height - 0.4*inch, f"BROADSHEET - {class_info['name']} - {term_info['name']}")
    
    y_pos = page_height - 1*inch
    
    # Table
    subjects = list(student_results[0]['results'].keys()) if student_results else []
    
    col_widths = [0.6*inch] + [0.5*inch] * len(subjects) + [0.6*inch] * 3
    total_width = sum(col_widths)
    
    if total_width > page_width - inch:
        # Scale down if needed
        scale = (page_width - inch) / total_width
        col_widths = [w * scale for w in col_widths]
    
    # Header row
    c.setFillColor(PDFStyles.ACCENT_BLUE)
    c.rect(0.5*inch, y_pos - 0.3*inch, sum(col_widths), 0.3*inch, fill=True, stroke=False)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7)
    
    x = 0.5*inch
    headers = ['#'] + [s[:10] for s in subjects] + ['Total', 'Average', 'Position']
    for i, header in enumerate(headers):
        c.drawString(x + 0.05*inch, y_pos - 0.22*inch, header)
        x += col_widths[i]
    
    y_pos -= 0.3*inch
    
    # Data rows
    for idx, student in enumerate(student_results):
        bg = PDFStyles.CARD_WHITE if idx % 2 == 0 else PDFStyles.BG_LIGHT
        c.setFillColor(bg)
        c.rect(0.5*inch, y_pos - 0.25*inch, sum(col_widths), 0.25*inch, fill=True, stroke=False)
        
        c.setFillColor(PDFStyles.TEXT_DARK)
        c.setFont("Helvetica", 7)
        
        x = 0.5*inch
        values = [str(idx + 1)]
        
        for subject in subjects:
            score = student['results'].get(subject, {}).get('total', '-')
            values.append(str(score) if score != '-' else '-')
        
        # Calculate totals
        scores = [student['results'].get(s, {}).get('total', 0) for s in subjects if isinstance(student['results'].get(s, {}).get('total'), (int, float))]
        total = sum(scores) if scores else 0
        avg = total / len(scores) if scores else 0
        
        values.extend([f"{total:.1f}", f"{avg:.1f}", str(student.get('position', '-'))])
        
        for i, val in enumerate(values):
            c.drawString(x + 0.05*inch, y_pos - 0.18*inch, str(val))
            x += col_widths[i]
        
        y_pos -= 0.25*inch
        
        if y_pos < inch:
            c.showPage()
            y_pos = page_height - inch
    
    c.save()
    buffer.seek(0)
    return buffer
