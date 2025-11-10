import json
import math
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class UnderwritingAgent:
    def __init__(self):
        with open(DATA_DIR / "credit_scores.json", "r", encoding="utf-8") as f:
            self.credit_data = json.load(f)

    def evaluate_loan(self, customer, loan_details):
        print(f"📊 UnderwritingAgent: Evaluating optimal loan for {customer['name']}")

        score = self._get_credit_score(customer["customer_id"])
        amount = int(loan_details["proposed_amount"])
        base_rate = float(loan_details.get("rate", 10.95))
        preferred_tenure = int(loan_details.get("tenure", 36))
        pre_limit = int(customer["pre_approved_limit"])
        income = int(customer.get("monthly_income", 0))

        # 🔴 Rule 1: Hard rejections
        if score < 650:
            return {"status": "rejected", "reason": "Credit score below 650 — not eligible for a loan."}
        if amount > 2 * pre_limit:
            return {"status": "rejected", "reason": "Requested amount exceeds 2× pre-approved limit."}
        if income <= 0:
            return {"status": "rejected", "reason": "Monthly income details missing."}

        # ✅ Evaluate multiple tenure options (12, 24, 36, 48, 60 months)
        options = []
        for tenure in [12, 24, 36, 48, 60]:
            rate = self._adjust_rate(base_rate, tenure, score)
            emi = self._calc_emi(amount, rate, tenure)
            total_payment = emi * tenure
            total_interest = total_payment - amount
            processing_fee = max(999, round(amount * 0.008))
            affordability = round((emi / income) * 100, 2)

            options.append({
                "tenure": tenure,
                "rate": round(rate, 2),
                "emi": round(emi, 2),
                "total_interest": round(total_interest, 2),
                "processing_fee": processing_fee,
                "affordability": affordability,
            })

        # 🔍 Filter affordable plans (EMI <= 50% of monthly income)
        feasible = [opt for opt in options if opt["affordability"] <= 50]
        if not feasible:
            return {"status": "rejected", "reason": "EMI exceeds 50% of income for all plans."}

        # ✅ Choose best (lowest total interest) and chosen (preferred or fallback)
        best = min(feasible, key=lambda x: (x["total_interest"], x["emi"]))
        chosen = next((opt for opt in feasible if opt["tenure"] == preferred_tenure), best)

        # Final decision
        return {
            "status": "approved",
            "approved_amount": amount,
            "preferred_tenure": preferred_tenure,
            "chosen_plan": chosen,
            "best_plan": best,
            "all_options": feasible,
        }

    # ------------------------------------
    # Helper: Interest Rate Adjustment
    # ------------------------------------
    def _adjust_rate(self, base_rate, tenure, credit_score):
        """
        Adjust rate based on tenure and credit score.
        Shorter tenure → lower rate. Longer tenure → higher rate.
        Excellent credit score → discount.
        """
        # tenure-based adjustment
        if tenure <= 12:
            adj = -0.5
        elif tenure <= 24:
            adj = -0.25
        elif tenure <= 36:
            adj = 0.0
        elif tenure <= 48:
            adj = 0.25
        else:
            adj = 0.5

        # credit score impact
        if credit_score >= 800:
            adj -= 0.25
        elif credit_score < 700:
            adj += 0.25

        return base_rate + adj

    # ------------------------------------
    # Helper: EMI Calculation
    # ------------------------------------
    @staticmethod
    def _calc_emi(principal, annual_rate_percent, months):
        r = (annual_rate_percent / 100.0) / 12.0
        if r == 0:
            return principal / months
        return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)

    # ------------------------------------
    # Helper: Credit Score Fetch
    # ------------------------------------
    def _get_credit_score(self, customer_id):
        for r in self.credit_data:
            if r.get("customer_id") == customer_id:
                return int(r.get("credit_score", 0))
        return 700  # default fallback