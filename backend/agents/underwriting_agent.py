import json
from pathlib import Path
import math

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class UnderwritingAgent:
    def __init__(self):
        with open(DATA_DIR / "credit_scores.json", "r", encoding="utf-8") as f:
            self.credit_data = json.load(f)

    def evaluate_loan(self, customer, loan_details):
        print(f"📊 UnderwritingAgent: Evaluating loan for {customer['name']}")
        score = self._get_credit_score(customer["customer_id"])
        amount = int(loan_details["proposed_amount"])
        pre = int(customer["pre_approved_limit"])
        income = int(customer.get("monthly_income", 0))
        rate = float(loan_details["rate"])
        tenure = int(loan_details["tenure"])

        # Rule A: Credit score < 700 → reject
        if score < 700:
            return {"status": "rejected", "reason": "Credit score below 700"}

        # Rule B: amount <= pre-approved → instant approve
        if amount <= pre:
            return {"status": "approved", "approved_amount": amount, "rate": rate, "tenure": tenure}

        # Rule C: amount <= 2x pre-approved → need salary slip + DTI <= 50%
        if amount <= 2 * pre:
            emi = self._calc_emi(amount, rate, tenure)
            if income == 0:
                return {"status": "rejected", "reason": "Income not available for DTI"}
            dti = emi / income
            if dti <= 0.5:
                return {"status": "approved", "approved_amount": amount, "rate": rate, "tenure": tenure}
            else:
                return {"status": "rejected", "reason": "EMI exceeds 50% of monthly income (DTI > 50%)"}

        # Rule D: amount > 2x pre-approved → reject
        return {"status": "rejected", "reason": "Requested amount exceeds 2× pre-approved limit"}

    def _get_credit_score(self, customer_id):
        for r in self.credit_data:
            if r.get("customer_id") == customer_id:
                return int(r.get("credit_score", 0))
        return 0

    @staticmethod
    def _calc_emi(principal, annual_rate_percent, months):
        r = (annual_rate_percent / 100.0) / 12.0
        if r == 0:
            return principal / months
        return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)