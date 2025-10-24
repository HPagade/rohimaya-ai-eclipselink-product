"""PDF Export Utility for SBAR Reports"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

def generate_sbar_pdf(handoff_data):
    """
    Generate a professional PDF for an SBAR report

    Args:
        handoff_data: Dictionary containing handoff information

    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )

    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=6
    )

    # Title
    elements.append(Paragraph("⚡ EclipseLink AI™", title_style))
    elements.append(Paragraph("Clinical Handoff Report - SBAR Format", styles['Heading2']))
    elements.append(Spacer(1, 20))

    # Patient Information Table
    patient_info = [
        ['Patient Information', ''],
        ['Patient Name:', handoff_data.get('patient_name', 'N/A')],
        ['Patient ID:', handoff_data.get('patient_id', 'N/A')],
        ['Handoff Type:', handoff_data.get('handoff_type', 'N/A').replace('_', ' ').title()],
        ['Priority:', handoff_data.get('priority', 'N/A').title()],
        ['Date/Time:', handoff_data.get('created_at', 'N/A')],
    ]

    # Add staff information if available
    if handoff_data.get('from_staff'):
        patient_info.append(['From:', handoff_data['from_staff']])
    if handoff_data.get('to_staff'):
        patient_info.append(['To:', handoff_data['to_staff']])
    if handoff_data.get('specialty'):
        patient_info.append(['Specialty:', handoff_data['specialty']])

    patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))

    elements.append(patient_table)
    elements.append(Spacer(1, 20))

    # Quality Scores (if available)
    if handoff_data.get('quality_score'):
        scores_info = [
            ['Quality Metrics', '', ''],
            ['Quality Score', 'Completeness Score', 'Critical Elements'],
            [
                f"{handoff_data.get('quality_score', 0)}%",
                f"{handoff_data.get('completeness_score', 0)}%",
                f"{handoff_data.get('critical_elements_score', 0)}%"
            ]
        ]

        scores_table = Table(scores_info, colWidths=[2*inch, 2*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e5e7eb')),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 10),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8fafc')),
            ('FONTSIZE', (0, 2), (-1, 2), 14),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#10b981')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))

        elements.append(scores_table)
        elements.append(Spacer(1, 20))

    # SBAR Sections
    elements.append(Paragraph("SBAR Report", header_style))
    elements.append(Spacer(1, 12))

    # Situation
    elements.append(Paragraph("📘 SITUATION", header_style))
    situation_text = handoff_data.get('sbar_situation', 'No situation information available.')
    elements.append(Paragraph(situation_text, normal_style))
    elements.append(Spacer(1, 12))

    # Background
    elements.append(Paragraph("📗 BACKGROUND", header_style))
    background_text = handoff_data.get('sbar_background', 'No background information available.')
    elements.append(Paragraph(background_text, normal_style))
    elements.append(Spacer(1, 12))

    # Assessment
    elements.append(Paragraph("📙 ASSESSMENT", header_style))
    assessment_text = handoff_data.get('sbar_assessment', 'No assessment information available.')
    elements.append(Paragraph(assessment_text, normal_style))
    elements.append(Spacer(1, 12))

    # Recommendation
    elements.append(Paragraph("📕 RECOMMENDATION", header_style))
    recommendation_text = handoff_data.get('sbar_recommendation', 'No recommendation information available.')
    elements.append(Paragraph(recommendation_text, normal_style))
    elements.append(Spacer(1, 30))

    # Footer
    elements.append(Spacer(1, 20))
    footer_text = f"""
    <para align=center>
    <font size=8 color="#64748b">
    This report was generated by EclipseLink AI™ on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}<br/>
    Rohimaya Health AI • HIPAA Compliant • AI-Powered Clinical Handoff Platform<br/>
    For questions or support, contact: support@eclipselink.ai
    </font>
    </para>
    """
    elements.append(Paragraph(footer_text, info_style))

    # Build PDF
    doc.build(elements)

    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data


def generate_batch_pdf(handoffs_list):
    """
    Generate a PDF report for multiple handoffs

    Args:
        handoffs_list: List of handoff dictionaries

    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    elements = []
    styles = getSampleStyleSheet()

    # Title page
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    elements.append(Paragraph("⚡ EclipseLink AI™", title_style))
    elements.append(Paragraph(f"Batch Handoff Report - {len(handoffs_list)} Handoffs", styles['Heading2']))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(PageBreak())

    # Add each handoff on a new page
    for idx, handoff in enumerate(handoffs_list):
        # Generate individual handoff content (simplified version)
        elements.append(Paragraph(f"Handoff {idx + 1} of {len(handoffs_list)}", styles['Heading2']))
        elements.append(Paragraph(f"Patient: {handoff.get('patient_name', 'N/A')}", styles['Normal']))
        elements.append(Paragraph(f"ID: {handoff.get('patient_id', 'N/A')}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Add SBAR sections (simplified)
        if handoff.get('sbar_situation'):
            elements.append(Paragraph("Situation:", styles['Heading3']))
            elements.append(Paragraph(handoff['sbar_situation'], styles['Normal']))
            elements.append(Spacer(1, 12))

        if idx < len(handoffs_list) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data
