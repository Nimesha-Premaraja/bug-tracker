"""
PDF Report Generator for Bug Tracking System
Generates summary PDF reports for multiple bugs
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from flask import current_app


class BugReportGenerator:
    """
    Generates a summary PDF report containing multiple bugs with their details.
    """
    
    def __init__(self, bugs, current_user=None, filters_applied=None):
        """
        Initialize the PDF generator.
        
        Args:
            bugs: List of Bug objects to include in the report
            current_user: User object representing who generated the report
            filters_applied: Dictionary containing applied filters for reference
        """
        self.bugs = bugs
        self.current_user = current_user
        self.filters_applied = filters_applied or {}
        self.buffer = BytesIO()
        self.doc = None
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Bug title style
        self.styles.add(ParagraphStyle(
            name='BugTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Update Normal text style (don't add, modify existing)
        self.styles['Normal'].fontSize = 9
        self.styles['Normal'].leading = 11
        self.styles['Normal'].textColor = colors.HexColor('#374151')
        
        # Label style
        self.styles.add(ParagraphStyle(
            name='Label',
            fontSize=8,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica-Bold'
        ))
        
    def generate_pdf(self) -> BytesIO:
        """
        Generate and return the PDF as a BytesIO buffer.
        
        Returns:
            BytesIO object containing PDF content
        """
        # Create the PDF document
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=current_app.config.get('PDF_MARGIN', 20),
            leftMargin=current_app.config.get('PDF_MARGIN', 20),
            topMargin=current_app.config.get('PDF_MARGIN', 20),
            bottomMargin=current_app.config.get('PDF_MARGIN', 20)
        )
        
        # Build the story
        story = []
        
        # Add header
        story.extend(self._add_header())
        
        # Add summary
        story.extend(self._add_summary())
        
        # Add bugs section
        if self.bugs:
            story.extend(self._add_bugs_details())
        else:
            story.append(Paragraph("No bugs found matching the selected criteria.", self.styles['Normal']))
        
        # Add footer will be added by onFirstPage and onLaterPages
        self.doc.build(
            story,
            onFirstPage=self._add_footer,
            onLaterPages=self._add_footer
        )
        
        # Reset buffer position to beginning for reading
        self.buffer.seek(0)
        
        return self.buffer
    
    def _add_header(self):
        """Add report header with title and metadata."""
        elements = []
        
        # Title
        title = Paragraph("BUG REPORT", self.styles['ReportTitle'])
        elements.append(title)
        
        # Generated date and time
        generated_date = datetime.utcnow().strftime("%B %d, %Y at %H:%M:%S UTC")
        generated_by = self.current_user.username if self.current_user else "System"
        
        header_info = f"Generated: {generated_date} | By: {generated_by}"
        elements.append(Paragraph(header_info, self.styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _add_summary(self):
        """Add summary section with report statistics."""
        elements = []
        
        # Summary section
        elements.append(Paragraph("Report Summary", self.styles['SectionHeader']))
        
        # Summary details
        summary_data = [
            ["Total Bugs:", str(len(self.bugs))],
            ["Report Date:", datetime.utcnow().strftime("%B %d, %Y")],
        ]
        
        # Add filter information
        if self.filters_applied:
            filters_list = []
            if self.filters_applied.get('search'):
                filters_list.append(f"Search: {self.filters_applied['search']}")
            if self.filters_applied.get('status'):
                filters_list.append(f"Status: {self.filters_applied['status']}")
            if self.filters_applied.get('priority'):
                filters_list.append(f"Priority: {self.filters_applied['priority']}")
            if self.filters_applied.get('assignee_id'):
                filters_list.append(f"Assignee: {self.filters_applied.get('assignee_name', 'Unknown')}")
            
            if filters_list:
                summary_data.append(["Filters Applied:", "; ".join(filters_list)])
            else:
                summary_data.append(["Filters Applied:", "None"])
        else:
            summary_data.append(["Filters Applied:", "None"])
        
        # Create summary table
        summary_table = Table(summary_data, colWidths=[2 * inch, 4 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _add_bugs_details(self):
        """Add detailed bugs information to the report."""
        elements = []
        
        elements.append(Paragraph("Bugs Details", self.styles['SectionHeader']))
        
        # Add bugs in groups to manage page breaks
        bugs_per_page = current_app.config.get('PDF_BUGS_PER_PAGE', 20)
        
        for idx, bug in enumerate(self.bugs):
            # Add page break after every N bugs
            if idx > 0 and idx % bugs_per_page == 0:
                elements.append(PageBreak())
                elements.append(Paragraph("Bugs Details (continued)", self.styles['SectionHeader']))
            
            # Add bug details
            elements.extend(self._format_bug_block(bug, idx + 1))
            elements.append(Spacer(1, 0.15 * inch))
        
        return elements
    
    def _format_bug_block(self, bug, bug_number):
        """
        Format a single bug as a block of information.
        
        Args:
            bug: Bug object
            bug_number: Sequential number in the report
            
        Returns:
            List of reportlab elements
        """
        elements = []
        
        # Bug title with number
        bug_header = f"Bug #{bug.id}: {bug.title}"
        elements.append(Paragraph(bug_header, self.styles['BugTitle']))
        
        # Description
        if bug.description:
            description_text = f"<b>Description:</b> {bug.description}"
            elements.append(Paragraph(description_text, self.styles['Normal']))
        
        # Bug details table
        bug_details = [
            ["Status:", bug.status.capitalize()],
            ["Priority:", bug.priority.capitalize()],
            ["Reporter:", bug.reporter.email if bug.reporter else "N/A"],
            ["Assignee:", bug.assignee.email if bug.assignee else "Unassigned"],
            ["Created:", bug.created_at.strftime("%Y-%m-%d %H:%M") if bug.created_at else "N/A"],
            ["Updated:", bug.updated_at.strftime("%Y-%m-%d %H:%M") if bug.updated_at else "N/A"],
        ]
        
        # Add closed date if bug is closed
        if bug.status == 'closed' and bug.closed_at:
            bug_details.append(["Closed:", bug.closed_at.strftime("%Y-%m-%d %H:%M")])
        
        # Add comments and attachments count
        bug_details.append(["Comments:", str(len(bug.comments))])
        bug_details.append(["Attachments:", str(len(bug.attachments))])
        
        # Create details table
        details_table = Table(bug_details, colWidths=[1.5 * inch, 4.5 * inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f9fafb')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#f0f0f0')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
        ]))
        
        elements.append(details_table)
        
        # Add separator line
        elements.append(Spacer(1, 0.1 * inch))
        
        return elements
    
    def _add_footer(self, canvas, doc):
        """Add footer with page numbers and generation info."""
        canvas.saveState()
        
        # Footer text
        footer_text = f"Generated by {self.current_user.username if self.current_user else 'System'} on {datetime.utcnow().strftime('%Y-%m-%d')}"
        
        # Draw page number and footer
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor('#9ca3af'))
        
        # Page number on the right
        page_num = canvas.getPageNumber()
        canvas.drawRightString(
            A4[0] - 20,
            20,
            f"Page {page_num}"
        )
        
        # Footer text on the left
        canvas.drawString(
            20,
            20,
            footer_text
        )
        
        canvas.restoreState()
