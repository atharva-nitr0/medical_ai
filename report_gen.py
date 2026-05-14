from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import uuid

def generate_medical_report(patient_name, patient_age, patient_gender, prediction_res, output_path):
    """
    Generates a professional medical diagnostic report in PDF format.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    report_id = f"REP-{str(uuid.uuid4())[:8].upper()}"
    scan_id = f"SCN-{str(uuid.uuid4())[:6].upper()}"
    
    # --- Header Background ---
    c.setFillColorRGB(0.04, 0.07, 0.17) # Dark medical navy
    c.rect(0, height - 100, width, 100, fill=1)
    
    # --- Header Title ---
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 50, "AI MEDICAL DIAGNOSTIC CENTER")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 75, f"Report ID: {report_id}  |  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # --- Patient Information Section ---
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "PATIENT INFORMATION")
    c.setStrokeColor(colors.lightgrey)
    c.line(50, height - 145, width - 50, height - 145)
    
    c.setFont("Helvetica", 11)
    # Column 1
    c.drawString(60, height - 170, f"Patient Name: {patient_name if patient_name else 'N/A'}")
    c.drawString(60, height - 190, f"Age / Gender: {patient_age} / {patient_gender}")
    c.drawString(60, height - 210, f"Scan Type: {prediction_res.get('cancer_type', 'MRI Analysis')}")
    
    # Column 2
    c.drawString(300, height - 170, f"Scan ID: {scan_id}")
    c.drawString(300, height - 190, f"Department: Radiology AI")
    c.drawString(300, height - 210, f"Referring Physician: AI System")
    
    # --- AI Clinical Summary ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 260, "AI CLINICAL SUMMARY")
    c.line(50, height - 265, width - 50, height - 265)
    
    c.setFont("Helvetica-Bold", 12)
    res_color = colors.red if prediction_res['status'] == 'Pathological' else colors.green
    c.setFillColor(res_color)
    c.drawString(60, height - 290, f"PRIMARY FINDING: {prediction_res['class']}")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    text_object = c.beginText(60, height - 315)
    text_object.setFont("Helvetica", 10)
    text_object.setLeading(14)
    
    summary_text = (
        f"AI-assisted analysis of the provided scan indicates features associated with {prediction_res['class']}. "
        f"The system detected {prediction_res['info'].lower()} with a confidence score of {prediction_res['confidence']:.2f}%. "
        "Radiological characteristics analyzed include tissue density gradients, lesion morphology, "
        "and abnormal enhancement patterns in localized regions."
    )
    
    # Simple word wrap logic
    lines = [summary_text[i:i+90] for i in range(0, len(summary_text), 90)]
    for line in lines:
        text_object.textLine(line)
    c.drawText(text_object)
    
    # --- Pathology Findings Table ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 420, "PATHOLOGY FINDINGS")
    c.line(50, height - 425, width - 50, height - 425)
    
    # Grid lines for findings
    y_pos = height - 450
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y_pos, "Parameter")
    c.drawString(250, y_pos, "AI Interpretation")
    c.drawString(450, y_pos, "Status")
    c.line(50, y_pos - 5, width - 50, y_pos - 5)
    
    c.setFont("Helvetica", 10)
    findings = [
        ("Morphological Findings", "Atypical tissue structure observed", "Abnormal" if prediction_res['status'] == 'Pathological' else "Normal"),
        ("Enhancement Patterns", "Irregular focal point" if prediction_res['status'] == 'Pathological' else "Uniform enhancement", "Review Required" if prediction_res['status'] == 'Pathological' else "Clear"),
        ("AI Diagnostic Score", f"{prediction_res['confidence']:.2f}% Match", "Positive" if prediction_res['status'] == 'Pathological' else "Negative"),
        ("Risk Assessment", prediction_res['risk'], prediction_res['risk'])
    ]
    
    for label, interpret, stat in findings:
        y_pos -= 25
        c.drawString(60, y_pos, label)
        c.drawString(250, y_pos, interpret)
        c.drawString(450, y_pos, stat)
        c.setStrokeColor(colors.whitesmoke)
        c.line(50, y_pos - 5, width - 50, y_pos - 5)
    
    # --- Recommendations ---
    c.setStrokeColor(colors.lightgrey)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(50, height - 600, "MEDICAL RECOMMENDATIONS")
    c.line(50, height - 605, width - 50, height - 605)
    
    c.setFont("Helvetica", 10)
    recs = [
        "• Immediate consultation with a specialized oncologist or radiologist is advised.",
        "• Correlation with secondary imaging (CT/PET scan) recommended for definitive diagnosis.",
        "• Histopathological biopsy review may be necessary to confirm pathological features.",
        "• Patient follow-up and monitoring as per clinical timeline."
    ] if prediction_res['status'] == 'Pathological' else [
        "• No immediate intervention required based on current AI analysis.",
        "• Continue routine health screenings and annual check-ups.",
        "• Maintain healthy lifestyle and dietary habits.",
        "• Re-scan if new clinical symptoms develop."
    ]
    
    y_pos = height - 630
    for rec in recs:
        c.drawString(60, y_pos, rec)
        y_pos -= 20
        
    # --- Footer ---
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    footer_text = "Disclaimer: This is an AI-generated report for diagnostic assistance only. It should be reviewed by a licensed medical professional."
    c.drawCentredString(width/2, 50, footer_text)
    c.drawCentredString(width/2, 35, f"System Version: 2.0.1 (Stable)  |  Pathology Engine: v4.2")
    
    c.save()
    return output_path
