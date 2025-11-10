from fpdf import FPDF
import os
from datetime import datetime

def create_sanction_letter(name, amount, rate, tenure):
    # Ensure output folder exists
    os.makedirs("static/letters", exist_ok=True)

    # Create unique file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_").lower()
    file_path = f"static/letters/sanction_letter_{safe_name}_{timestamp}.pdf"

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="CapitalMitra - Loan Sanction Letter", ln=True, align="C")
    pdf.ln(10)

    # Letter Body
    pdf.cell(200, 10, txt=f"Dear {name},", ln=True, align="L")
    pdf.cell(200, 10, txt=f"We are delighted to inform you that your loan of ₹{amount:,} has been approved.", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Interest Rate: {rate}% per annum", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Tenure: {tenure} months", ln=True, align="L")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Thank you for choosing CapitalMitra.", ln=True, align="L")
    pdf.cell(200, 10, txt="Funds will be disbursed within 24 hours of acceptance.", ln=True, align="L")

    # Footer
    pdf.ln(20)
    pdf.cell(200, 10, txt="-- CapitalMitra Loan Services Pvt. Ltd. --", ln=True, align="C")

    # Save File
    pdf.output(file_path)

    # Return public link (for API response)
    return f"/{file_path}"