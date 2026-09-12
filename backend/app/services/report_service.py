from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ..config import REPORT_DIR

def create_report(scan, indicators, recommendations):
    path = REPORT_DIR / f"{scan.id}.pdf"
    pdf = canvas.Canvas(str(path), pagesize=letter)
    text = pdf.beginText(48, 740)
    text.setFont("Helvetica-Bold", 18); text.textLine("RedFlag AI Report")
    text.setFont("Helvetica", 11)
    for label, value in [("Scan ID", scan.id), ("File", scan.filename), ("Type", scan.scan_type), ("Risk score", f"{scan.risk_score}/100"), ("Risk level", scan.risk_level)]: text.textLine(f"{label}: {value}")
    text.textLine(""); text.textLine("Indicators:")
    for item in indicators: text.textLine(f"- {item}")
    text.textLine(""); text.textLine("Recommendations:")
    for item in recommendations: text.textLine(f"- {item}")
    text.textLine(""); text.textLine("Prototype detection model. Results are experimental, not definitive proof.")
    pdf.drawText(text); pdf.save(); return path