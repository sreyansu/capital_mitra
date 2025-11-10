# backend/agents/underwriting_agent.py

import json
import os

class UnderwritingAgent:
    def __init__(self):
        data_path = os.path.join(os.path.dirname(__file__), "../data/credit_scores.json")
        with open(data_path, "r") as f:
            self.credit_data = json.load(f)

    def evaluate_loan(self, customer, loan_details):
        print(f"📊 UnderwritingAgent: Evaluating loan for {customer['name']}")
        credit_score = self._get_credit_score(customer["customer_id"])
        amount = loan_details["proposed_amount"]
        pre_limit = customer["pre_approved_limit"]

        if credit_score < 700:
            return {"status": "rejected", "reason": "Low credit score"}

        if amount <= pre_limit:
            return {
                "status": "approved",
                "approved_amount": amount,
                "rate": loan_details["rate"],
                "tenure": loan_details["tenure"]
            }

        elif amount <= 2 * pre_limit:
            # Requires salary slip (simulate success)
            print("📂 Salary slip required. Assuming upload verified.")
            emi = (amount * loan_details["rate"] / 1200) / (1 - (1 + loan_details["rate"]/1200) ** -loan_details["tenure"])
            if emi <= 0.5 * customer["monthly_income"]:
                return {
                    "status": "approved",
                    "approved_amount": amount,
                    "rate": loan_details["rate"],
                    "tenure": loan_details["tenure"]
                }
            else:
                return {"status": "rejected", "reason": "EMI exceeds 50% of income"}

        else:
            return {"status": "rejected", "reason": "Amount exceeds 2x pre-approved limit"}

    def _get_credit_score(self, customer_id):
        for record in self.credit_data:
            if record["customer_id"] == customer_id:
                return record["credit_score"]
        return 0