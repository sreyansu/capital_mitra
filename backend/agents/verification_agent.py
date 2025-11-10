import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class VerificationAgent:
    def __init__(self):
        with open(DATA_DIR / "crm_data.json", "r", encoding="utf-8") as f:
            self.crm_data = json.load(f)

    def verify_customer(self, customer: dict) -> bool:
        print(f"✅ VerificationAgent: Verifying KYC for {customer['name']}")
        cid = customer.get("customer_id")
        for rec in self.crm_data:
            if rec.get("customer_id") == cid and rec.get("verified") is True:
                print("KYC verified successfully.")
                return True
        print("❌ Verification failed.")
        return False