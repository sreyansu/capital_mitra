import os
import re
import json
import random
from pathlib import Path

# === Import submodules ===
from backend.services.email_otp_service import EmailOTPService
from backend.services.smart_advisor import SmartAdvisor, rupees
from backend.agents.sales_agent import SalesAgent
from backend.agents.verification_agent import VerificationAgent
from backend.agents.underwriting_agent import UnderwritingAgent
from backend.agents.sanction_agent import SanctionAgent

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class MasterAgent:
    """
    CapitalMitra Master Agent — full conversational orchestrator.
    Handles structured loan flow (KYC → Loan → Tenure → Sanction)
    and AI-enhanced advice via OpenRouter + SmartAdvisor.
    """

    def __init__(self):
        # === Core Modules ===
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()
        self.sanction_agent = SanctionAgent()
        self.smart_advisor = SmartAdvisor()
        self.otp_service = EmailOTPService()

        # === State & Context ===
        self.state = "GREETING"
        self.pending_otp = None
        self.otp_verified = False
        self.ctx = {
            "name": None,
            "email": None,
            "phone": None,
            "pan": None,
            "customer": None,
            "otp": None,
            "loan_type": None,
            "requested_amount": None,
            "preferred_tenure": None,
            "approved": None,
        }

    # ==============================
    # MAIN ENTRY POINT
    # ==============================
    def process_message(self, message: str) -> dict:
        text = (message or "").strip()

        # AI fallback for generic financial questions
        loan_keywords = ["loan", "interest", "emi", "limit", "credit", "borrow"]
        if any(w in text.lower() for w in loan_keywords):
            if self.state not in [
                "COLLECT_NAME", "COLLECT_EMAIL", "COLLECT_PHONE", "COLLECT_PAN", "OTP_SENT",
            ]:
                return self._ai_context_response(text)

        # Map conversation states
        state_map = {
            "GREETING": self._greet,
            "COLLECT_NAME": self._collect_name,
            "COLLECT_EMAIL": self._collect_email,
            "COLLECT_PHONE": self._collect_phone,
            "COLLECT_PAN": self._collect_pan,
            "OTP_SENT": self._verify_otp,
            "VERIFYING": self._verify_in_crm,
            "LOAN_INTENT": self._loan_intent,
            "COLLECT_AMOUNT": self._collect_amount,
            "COLLECT_TENURE": self._collect_tenure,
            "UNDERWRITING": self._underwrite_and_decide,
            "SANCTION": self._generate_sanction,
            "DONE": self._handle_post_sanction,
        }

        handler = state_map.get(self.state)
        return handler(text) if handler else self.sales_agent.provide_offer(text)

    # ==============================
    # AI CONTEXTUAL REPLIES
    # ==============================
    def _ai_context_response(self, user_text: str):
        cust = self.ctx.get("customer")
        approved = self.ctx.get("approved")

        context = "You are CapitalMitra, a professional loan advisor assisting a verified customer."
        if cust:
            context += (
                f" Customer: {cust['name']}, Credit Score: {cust['credit_score']}, "
                f"Pre-approved Limit: ₹{cust['pre_approved_limit']}."
            )
        if approved:
            context += (
                f" They were approved for ₹{approved['approved_amount']} at {approved['rate']}% "
                f"for {approved['tenure']} months."
            )

        prompt = f"{context}\nUser: {user_text}"
        return self.sales_agent.provide_offer(prompt)

    # ==============================
    # STRUCTURED CONVERSATION FLOW
    # ==============================
    def _greet(self, _):
        self.state = "COLLECT_NAME"
        return {"message": "👋 Hi! I’m CapitalMitra, your AI loan assistant. May I know your full name?"}

    def _collect_name(self, text):
        if len(text.split()) < 2:
            return {"message": "Please share your full name (first & last)."}
        self.ctx["name"] = text.title().strip()
        self.state = "COLLECT_EMAIL"
        return {"message": f"Thanks, {self.ctx['name']}! 📧 Could you share your email address?"}

    def _collect_email(self, text):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", text):
            return {"message": "That doesn’t look like a valid email. Please re-enter it."}
        self.ctx["email"] = text.strip()
        self.state = "COLLECT_PHONE"
        return {"message": "Got it! Please enter your 10-digit phone number."}

    def _collect_phone(self, text):
        phone = re.sub(r"[^\d]", "", text)
        if not re.fullmatch(r"\d{10}", phone):
            return {"message": "That didn’t look like a valid 10-digit number. Try again (e.g., 9876543210)."}
        self.ctx["phone"] = phone
        self.state = "COLLECT_PAN"
        return {"message": "Perfect! Lastly, please enter your PAN (e.g., ABCDE1234F)."}

    def _collect_pan(self, text):
        pan = text.strip().upper()
        if not re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]", pan):
            return {"message": "PAN format seems invalid. Please re-enter like ABCDE1234F."}

        self.ctx["pan"] = pan
        otp = str(random.randint(100000, 999999))
        self.pending_otp = otp
        self.otp_service.send_otp(self.ctx["email"], otp)
        self.state = "OTP_SENT"
        return {"message": f"🔐 OTP sent to {self.ctx['email']}. Please enter it to verify."}

    def _verify_otp(self, text):
        otp = re.sub(r"[^\d]", "", text)
        if otp == self.pending_otp:
            self.pending_otp = None
            self.otp_verified = True
            return self._verify_in_crm()
        return {"message": "❌ Incorrect OTP. Please try again."}

    def _verify_in_crm(self, _=None):
        cust = self._find_customer(self.ctx["pan"], self.ctx["email"], self.ctx["phone"])
        if not cust:
            self.state = "DONE"
            return {"message": "❌ No matching KYC record found. Please contact our nearest branch."}

        self.ctx["customer"] = cust
        if not self.verification_agent.verify_customer(cust):
            self.state = "DONE"
            return {"message": "❌ KYC verification failed. Please contact support."}

        self.state = "LOAN_INTENT"
        return {
            "message": (
                f"✅ KYC verified successfully! Credit Score: {cust['credit_score']} | "
                f"Pre-approved Limit: ₹{cust['pre_approved_limit']:,}.\n"
                "Which type of loan are you interested in — personal, car, or home?"
            )
        }

    def _loan_intent(self, text):
        low = text.lower()
        if any(w in low for w in ["no", "later", "not now"]):
            self.state = "DONE"
            return {"message": "No problem! You can return anytime to apply for a loan. 😊"}

        loan_types = {
            "car": "Car Loan 🚗",
            "auto": "Car Loan 🚗",
            "home": "Home Loan 🏠",
            "education": "Education Loan 🎓",
            "business": "Business Loan 💼",
            "personal": "Personal Loan 💰",
        }

        for key, loan_name in loan_types.items():
            if key in low:
                self.ctx["loan_type"] = loan_name
                self.state = "COLLECT_AMOUNT"
                return {"message": f"Got it! How much would you like to borrow for your {loan_name.lower()}?"}

        return {"message": "Please mention what type of loan you’d like — car, home, or personal?"}

    def _collect_amount(self, text):
        amt = self._extract_amount(text)
        if not amt:
            return {"message": "Please enter a valid amount (e.g., 500000)."}
        self.ctx["requested_amount"] = amt
        self.state = "COLLECT_TENURE"
        return {
            "message": (
                f"You’d like a loan of ₹{amt:,}. Now please select your preferred tenure — "
                "12, 24, or 36 months? 💡 Shorter tenure = higher EMI but lower total interest."
            )
        }

    def _collect_tenure(self, text):
        tenure = re.sub(r"[^\d]", "", text)
        if not tenure or int(tenure) not in [12, 24, 36]:
            return {"message": "Please enter a valid tenure — 12, 24, or 36 months."}
        self.ctx["preferred_tenure"] = int(tenure)
        self.state = "UNDERWRITING"
        return self._underwrite_and_decide()

    # ==============================
    # SMART UNDERWRITING
    # ==============================
    def _underwrite_and_decide(self, _=None):
        cust = self.ctx["customer"]
        amount = self.ctx["requested_amount"]
        tenure = self.ctx.get("preferred_tenure", 36)

        loan_details = {"proposed_amount": amount, "rate": 10.95, "tenure": tenure}
        result = self.underwriting_agent.evaluate_loan(cust, loan_details)
        if result["status"] == "rejected":
            self.state = "DONE"
            return {"message": f"❌ Loan rejected: {result['reason']}"}

        # Generate multiple plan comparisons
        all_options = self.smart_advisor.compare_tenures(amount, base_rate=10.95)
        summary_text = "\n".join(
            [
                f"• {opt['tenure']} months @ {opt['rate']}% → EMI {rupees(opt['emi'])}/month, Total Interest {rupees(opt['total_interest'])}"
                for opt in all_options
            ]
        )

        self.ctx["approved"] = result
        self.state = "SANCTION"

        return {
            "message": (
                f"✅ Based on your profile, here are the options for your ₹{amount:,} loan:\n\n"
                f"{summary_text}\n\n"
                f"For your selected {tenure}-month plan:\n"
                f"📆 Tenure: {tenure} months | 💰 EMI: {rupees(result['emi'])}/month\n"
                f"💸 Rate: {result['rate']}% | 🧾 Processing Fee: {rupees(result['processing_fee'])}\n\n"
                "Would you like me to proceed with this plan and generate your sanction letter?"
            )
        }

    def _generate_sanction(self, _=None):
        cust = self.ctx["customer"]
        res = self.ctx["approved"]
        path = self.sanction_agent.generate_letter(
            name=cust["name"], amount=res["approved_amount"], rate=res["rate"], tenure=res["tenure"]
        )
        self.state = "DONE"
        return {
            "message": (
                f"🎉 Congratulations {cust['name']}! Your ₹{res['approved_amount']:,} "
                f"loan has been sanctioned. 📄 Download your sanction letter: /{path}"
            ),
            "sanction_letter": f"/{path}",
        }

    def _handle_post_sanction(self, text):
        return self._ai_context_response(text)

    # ==============================
    # HELPERS
    # ==============================
    def _find_customer(self, pan, email, phone):
        customers = self._read_json(DATA_DIR / "customers.json")
        phone_norm = re.sub(r"[^\d]", "", phone or "")
        for c in customers:
            c_phone = re.sub(r"[^\d]", "", c.get("phone", ""))
            if (
                c.get("pan", "").upper() == pan.upper()
                and c.get("email", "").lower() == email.lower()
                and c_phone.endswith(phone_norm)
            ):
                return c
        return None

    @staticmethod
    def _extract_amount(text: str) -> int | None:
        digits = re.sub(r"[^\d]", "", text or "")
        return int(digits) if digits else None

    @staticmethod
    def _read_json(path: Path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)