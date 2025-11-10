import os
import re
import json
import random
from pathlib import Path
from backend.services.email_otp_service import EmailOTPService
from backend.agents.sales_agent import SalesAgent
from backend.agents.verification_agent import VerificationAgent
from backend.agents.underwriting_agent import UnderwritingAgent
from backend.agents.sanction_agent import SanctionAgent

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class MasterAgent:
    """
    AI-integrated conversational orchestrator.
    Handles structured flow + dynamic AI responses for CapitalMitra.
    """

    def __init__(self):
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()
        self.sanction_agent = SanctionAgent()
        self.otp_service = EmailOTPService()

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
            "approved": None
        }

    # ==============================
    # ENTRY POINT
    # ==============================
    def process_message(self, message: str) -> dict:
        text = (message or "").strip()

        # Step 1 — Allow AI chat for general loan queries anytime
        if any(word in text.lower() for word in ["loan", "limit", "emi", "interest", "credit score", "pre-approved"]):
            if self.state not in ["COLLECT_NAME", "COLLECT_EMAIL", "COLLECT_PHONE", "COLLECT_PAN", "OTP_SENT"]:
                return self._ai_context_response(text)

        # Step 2 — Handle structured conversation states
        state_methods = {
            "GREETING": self._greet,
            "COLLECT_NAME": self._collect_name,
            "COLLECT_EMAIL": self._collect_email,
            "COLLECT_PHONE": self._collect_phone,
            "COLLECT_PAN": self._collect_pan,
            "OTP_SENT": self._verify_otp,
            "VERIFYING": self._verify_in_crm,
            "LOAN_INTENT": self._loan_intent,
            "COLLECT_AMOUNT": self._collect_amount,
            "UNDERWRITING": self._underwrite_and_decide,
            "SANCTION": self._generate_sanction,
            "DONE": self._handle_post_sanction
        }

        handler = state_methods.get(self.state, None)
        if handler:
            return handler(text)
        else:
            return self.sales_agent.provide_offer(text)

    # ==============================
    # AI SMART REPLIES
    # ==============================
    def _ai_context_response(self, user_text: str):
        """AI response enriched with current loan context."""
        cust = self.ctx.get("customer")
        approved = self.ctx.get("approved")

        context = "You are an expert loan advisor helping a verified customer."
        if cust:
            context += f" The user's name is {cust['name']}, credit score {cust['credit_score']}, and pre-approved limit ₹{cust['pre_approved_limit']}."
        if approved:
            context += f" They were approved for ₹{approved['approved_amount']} at {approved['rate']}% for {approved['tenure']} months."
        
        prompt = f"{context}\nUser: {user_text}"
        return self.sales_agent.provide_offer(prompt)

    # ==============================
    # STRUCTURED FLOW HANDLERS
    # ==============================
    def _greet(self, _):
        self.state = "COLLECT_NAME"
        return {"message": "👋 Hi! I’m CapitalMitra, your AI loan assistant. May I know your full name?"}

    def _collect_name(self, text):
        name = text.strip()
        if len(name.split()) < 2:
            return {"message": "Please share your full name (first & last)."}
        self.ctx["name"] = name.title()
        self.state = "COLLECT_EMAIL"
        return {"message": f"Thanks, {self.ctx['name']}! 📧 Please share your email address."}

    def _collect_email(self, text):
        email = text.strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return {"message": "That doesn’t look like a valid email. Please re-enter your email."}
        self.ctx["email"] = email
        self.state = "COLLECT_PHONE"
        return {"message": "Got it! Please enter your 10-digit phone number."}

    def _collect_phone(self, text):
        phone = re.sub(r"[^\d]", "", text)
        if not re.fullmatch(r"\d{10}", phone):
            return {"message": "That didn’t look like a valid 10-digit mobile number. Please re-enter (e.g., 9876543210)."}
        self.ctx["phone"] = phone
        self.state = "COLLECT_PAN"
        return {"message": "Perfect! Lastly, please enter your PAN (e.g., ABCDE1234F)."}

    def _collect_pan(self, text):
        pan = text.strip().upper()
        if not re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]", pan):
            return {"message": "PAN format seems invalid. Please re-enter like ABCDE1234F."}
        self.ctx["pan"] = pan

        # Generate OTP and send via email
        otp = str(random.randint(100000, 999999))
        self.pending_otp = otp
        self.ctx["otp"] = otp
        self.otp_service.send_otp(self.ctx["email"], otp)

        self.state = "OTP_SENT"
        return {"message": f"🔐 OTP sent to {self.ctx['email']}. Please enter it here to verify."}

    def _verify_otp(self, text):
        otp = re.sub(r"[^\d]", "", text)
        if otp == self.pending_otp:
            self.otp_verified = True
            self.pending_otp = None
            return self._verify_in_crm()
        return {"message": "❌ Incorrect OTP. Please try again."}

    def _verify_in_crm(self, _=None):
        cust = self._find_customer(self.ctx["pan"], self.ctx["email"], self.ctx["phone"])
        if not cust:
            self.state = "DONE"
            return {"message": "❌ Couldn’t match your KYC record. Please visit our branch for manual verification."}

        self.ctx["customer"] = cust
        if not self.verification_agent.verify_customer(cust):
            self.state = "DONE"
            return {"message": "❌ KYC verification failed. Please contact support."}

        self.state = "LOAN_INTENT"
        ai_msg = self.sales_agent.provide_offer(
            f"Congratulate {cust['name']} for KYC success. Credit score: {cust['credit_score']}, Limit: ₹{cust['pre_approved_limit']}. "
            "Ask politely which type of loan they’re interested in (e.g., car, home, business, personal)."
        )
        return {"message": f"✅ KYC verified successfully! {ai_msg['message']}"}

    def _loan_intent(self, text: str):
        low = text.lower()

        # 1️⃣ User postpones
        if any(w in low for w in ["no", "later", "not now"]):
            self.state = "DONE"
            return {"message": "No worries! You can return anytime for your loan needs. 😊"}

        # 2️⃣ Detect loan type
        loan_types = {
            "car": "Car Loan 🚗",
            "auto": "Car Loan 🚗",
            "home": "Home Loan 🏠",
            "house": "Home Loan 🏠",
            "education": "Education Loan 🎓",
            "study": "Education Loan 🎓",
            "business": "Business Loan 💼",
            "personal": "Personal Loan 💰"
        }

        for key, loan_name in loan_types.items():
            if key in low:
                self.ctx["loan_type"] = loan_name
                self.state = "COLLECT_AMOUNT"
                ai_msg = self.sales_agent.provide_offer(
                    f"The user chose {loan_name}. Greet them and briefly explain eligibility. Then ask how much they’d like to borrow."
                )
                return {"message": f"{ai_msg['message']} How much amount would you like to borrow for your {loan_name.lower()}?"}

        # 3️⃣ Generic loan confirmation
        if any(w in low for w in ["yes", "apply", "loan", "proceed"]):
            self.state = "COLLECT_AMOUNT"
            return {"message": "Great! What loan amount would you like to apply for? (e.g., 300000)"}

        # 4️⃣ Unclear intent → AI fallback
        ai_msg = self.sales_agent.provide_offer(
            f"The user said: '{text}'. They just completed KYC and were asked about loan type. Interpret and respond helpfully."
        )
        return {"message": ai_msg["message"]}

    def _collect_amount(self, text):
        amt = self._extract_amount(text)
        if not amt:
            return {"message": "Please enter a valid numeric amount (e.g., 250000)."}
        self.ctx["requested_amount"] = amt
        self.state = "UNDERWRITING"
        return self._underwrite_and_decide()

    def _underwrite_and_decide(self, _=None):
        cust = self.ctx["customer"]
        amount = self.ctx["requested_amount"]
        loan_details = {"proposed_amount": amount, "rate": 10.5, "tenure": 36}
        result = self.underwriting_agent.evaluate_loan(cust, loan_details)

        if result["status"] == "rejected":
            self.state = "DONE"
            return {"message": f"❌ Loan rejected: {result['reason']}"}

        self.ctx["approved"] = result
        self.state = "SANCTION"

        ai_msg = self.sales_agent.provide_offer(
            f"Congratulate {cust['name']} for loan approval of ₹{result['approved_amount']} at {result['rate']}%."
        )

        return {
            "message": (
                f"✅ Approved! Amount: ₹{result['approved_amount']:,}, Rate: {result['rate']}%, Tenure: {result['tenure']} months.\n"
                f"{ai_msg['message']}\nGenerating your sanction letter..."
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
                f"🎉 Congratulations {cust['name']}! Your loan of ₹{res['approved_amount']:,} "
                f"has been sanctioned. 📄 Download your sanction letter: /{path}"
            ),
            "sanction_letter": f"/{path}"
        }

    def _handle_post_sanction(self, text):
        """Continue chatting naturally after sanction (AI takeover)."""
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