from fpdf import FPDF
from datetime import datetime
import io


def generate_pdf(brief: dict):
    """
    Generate a PDF report from the complete disaster brief.
    Returns: PDF file as bytes
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)

    pdf.cell(0, 15, "INDRA AI - Disaster Response Brief", ln=True, align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.ln(5)

    location = f"{brief.get('district', 'N/A')}, {brief.get('state', 'N/A')}"
    pdf.cell(0, 10, f"Location: {location}", ln=True)

    timestamp = brief.get("generated_at", datetime.utcnow().isoformat())
    pdf.cell(0, 10, f"Generated: {timestamp}", ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Hazard Assessment", ln=True)
    pdf.set_font("Helvetica", "", 10)

    hazard = brief.get("hazard", {})
    if hazard:
        pdf.cell(0, 8, f"System: {hazard.get('system_name', 'N/A')}", ln=True)
        pdf.cell(
            0,
            8,
            f"Category: {hazard.get('category', 'N/A')} | Warning: {hazard.get('warning_color', 'N/A')}",
            ln=True,
        )
        pdf.cell(
            0,
            8,
            f"Wind Speed: {hazard.get('wind_speed_kmh', 0)} km/h | Pressure: {hazard.get('pressure_hpa', 0)} hPa",
            ln=True,
        )
        pdf.multi_cell(
            0, 8, f"Bulletin: {hazard.get('bulletin_text', 'No bulletin available')}"
        )

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Risk Assessment", ln=True)
    pdf.set_font("Helvetica", "", 10)

    risk = brief.get("risk", {})
    if risk:
        pdf.cell(
            0,
            8,
            f"INDRA Risk Score: {risk.get('indra_risk_score', 0)}/100 ({risk.get('risk_label', 'N/A')})",
            ln=True,
        )
        pdf.multi_cell(0, 8, f"Assessment: {risk.get('narrative', 'No narrative available')}")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Resource Deployment", ln=True)
    pdf.set_font("Helvetica", "", 10)

    resource = brief.get("resource", {})
    if resource:
        nearest = resource.get("nearest_ndrf", {})
        pdf.cell(
            0,
            8,
            f"Nearest NDRF: {nearest.get('name', 'N/A')} ({nearest.get('eta_hours', 0):.1f}h ETA)",
            ln=True,
        )
        pdf.cell(
            0, 8, f"Food Packets: {resource.get('food_packets_required', 0)}", ln=True
        )
        pdf.cell(0, 8, f"Water: {resource.get('water_litres_required', 0)} L", ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 8, brief.get("executive_summary", "No summary available"))

    pdf_bytes = pdf.output()
    return pdf_bytes
