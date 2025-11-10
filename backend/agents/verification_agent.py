# backend/agents/verification_agent.py

import json
import os

class VerificationAgent:
    def __init__(self):
        data_path = os.path.join(os.path.dirname(__file__), "../data/crm_data.json")
        with open(data_path, "r") as f:
            self.crm_data = json.load(f)

    def verify_customer(self, customer):
        print(f"✅ VerificationAgent: Verifying KYC for {customer['name']}")
        for record in self.crm_data:
            if record["customer_id"] == customer["customer_id"]:
                if record["verified"]:
                    print("KYC verified successfully.")
                    return True
        print("❌ Verification failed.")
        return False