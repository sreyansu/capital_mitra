from fpdf import FPDF
import os
from datetime import datetime
import math

class SanctionLetter(FPDF):
    def header(self):
        # Brand Header
        self.set_fill_color(255, 102, 0)  # Orange strip
        self.rect(0, 0, 210, 20, "F")
        self.set_xy(10, 6)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "CapitalMitra - Loan Sanction Letter", align="L")
        self.ln(20)

    def footer(self):
        # Footer Section
        self.set_y(-20)
        self.set_font("Arial", "I", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "CapitalMitra Loan Services Pvt. Ltd. | www.capitalmitra.ai", align="C")

def create_sanction_letter(name, amount, rate, tenure, processing_fee=0.01):
    """
    Generates a polished, professional sanction letter with brand styling.
    :param name: Customer full name
    :param amount: Sanctioned loan amount (int)
    :param rate: Interest rate (float)
    :param tenure: Tenure in months (int)
    :param processing_fee: Fee percentage (default 1%)
    :return: Public PDF file path
    """

    os.makedirs("static/letters", exist_ok=True)

    # File name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_").lower()
    file_path = f"static/letters/sanction_letter_{safe_name}_{timestamp}.pdf"

    # Calculations
    monthly_rate = rate / (12 * 100)
    emi = (amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
    total_payment = emi * tenure
    proc_fee = amount * processing_fee
    net_disbursal = amount - proc_fee

    # Create PDF
    pdf = SanctionLetter()
    pdf.add_page()

    # Body text color
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d %B %Y')}", ln=True, align="R")
    pdf.ln(5)
    pdf.cell(0, 10, f"To,", ln=True)
    pdf.cell(0, 10, f"{name}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Subject: Loan Sanction Confirmation", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, (
        f"Dear {name},\n\n"
        f"We are pleased to inform you that your loan application has been successfully approved by CapitalMitra. "
        f"The following are the details of your sanctioned loan:\n"
    ))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 8, "Loan Details", ln=True)
    pdf.set_font("Arial", "", 12)

    pdf.cell(90, 8, "Sanctioned Amount:", 0, 0)
    pdf.cell(0, 8, f"₹{amount:,.2f}", 0, 1)

    pdf.cell(90, 8, "Interest Rate (per annum):", 0, 0)
    pdf.cell(0, 8, f"{rate:.2f}%", 0, 1)

    pdf.cell(90, 8, "Tenure:", 0, 0)
    pdf.cell(0, 8, f"{tenure} months", 0, 1)

    pdf.cell(90, 8, "Monthly EMI:", 0, 0)
    pdf.cell(0, 8, f"₹{emi:,.2f}", 0, 1)

    pdf.cell(90, 8, "Processing Fee (1%):", 0, 0)
    pdf.cell(0, 8, f"₹{proc_fee:,.2f}", 0, 1)

    pdf.cell(90, 8, "Net Disbursal Amount:", 0, 0)
    pdf.cell(0, 8, f"₹{net_disbursal:,.2f}", 0, 1)

    pdf.ln(8)
    pdf.multi_cell(0, 8, (
        f"The EMI of ₹{emi:,.2f} will be auto-debited monthly from your registered account for {tenure} months. "
        "Please ensure sufficient balance to avoid any penalties.\n\n"
        "Your funds will be disbursed within 24 working hours of your acceptance.\n\n"
        "We sincerely thank you for choosing CapitalMitra and look forward to serving your financial needs."
    ))

    pdf.ln(20)
    pdf.cell(0, 10, "Warm regards,", ln=True)
    pdf.cell(0, 10, "Team CapitalMitra", ln=True)
    pdf.cell(0, 10, "support@capitalmitra.ai", ln=True)

    pdf.output(file_path)

    print(f"📄 Sanction letter generated: {file_path}")
    return f"/{file_path}"