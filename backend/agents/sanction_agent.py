from fpdf import FPDF
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
LETTERS_DIR = STATIC_DIR / "letters"
FONTS_DIR = STATIC_DIR / "fonts"

class SanctionAgent:
    def generate_letter(self, name, amount, rate, tenure):
        LETTERS_DIR.mkdir(parents=True, exist_ok=True)
        FONTS_DIR.mkdir(parents=True, exist_ok=True)

        pdf = FPDF()
        pdf.add_page()

        # Try Unicode (for ₹). If not present, fall back to core font + 'Rs.'
        dejavu = FONTS_DIR / "DejaVuSans.ttf"
        if dejavu.exists():
            pdf.add_font("DejaVu", "", str(dejavu), uni=True)
            pdf.set_font("DejaVu", size=12)
            rupee = "₹"
        else:
            pdf.set_font("Arial", size=12)
            rupee = "Rs."

        pdf.cell(200, 10, txt="CapitalMitra - Loan Sanction Letter", ln=True, align="C")
        pdf.ln(4)
        pdf.cell(200, 10, txt=f"Dear {name},", ln=True)
        pdf.cell(200, 10, txt=f"Your personal loan of {rupee}{amount:,} has been approved.", ln=True)
        pdf.cell(200, 10, txt=f"Interest Rate: {rate}% | Tenure: {tenure} months", ln=True)
        pdf.ln(6)
        pdf.multi_cell(0, 8, txt="Thank you for choosing CapitalMitra. This is a system-generated letter.")
        out = LETTERS_DIR / f"{name.replace(' ', '_')}_sanction_letter.pdf"
        pdf.output(str(out), "F")
        print(f"📄 Sanction letter generated at {out}")
        return str(out.relative_to(Path(__file__).resolve().parent.parent))  # 'static/letters/...'