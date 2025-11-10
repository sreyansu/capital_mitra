# backend/agents/sanction_agent.py

from fpdf import FPDF
import os

class SanctionAgent:
    def generate_letter(self, name, amount, rate, tenure):
        os.makedirs("static/letters", exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="CapitalMitra - Loan Sanction Letter", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Dear {name},", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Your personal loan of ₹{amount} has been approved!", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Interest Rate: {rate}% | Tenure: {tenure} months", ln=True, align="L")
        pdf.cell(200, 10, txt="Thank you for choosing CapitalMitra!", ln=True, align="L")

        file_path = f"static/letters/{name.replace(' ', '_')}_sanction_letter.pdf"
        pdf.output(file_path)
        print(f"📄 Sanction letter generated at {file_path}")
        return file_path