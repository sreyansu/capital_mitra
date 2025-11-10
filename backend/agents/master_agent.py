from backend.agents.sales_agent import SalesAgent
from backend.agents.verification_agent import VerificationAgent
from backend.agents.underwriting_agent import UnderwritingAgent
from backend.agents.sanction_agent import SanctionAgent

class MasterAgent:
    def __init__(self, customer: dict = None):  # ✅ made optional
        self.customer = customer
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()
        self.sanction_agent = SanctionAgent()

    def process_message(self, query: str):
        return self.handle_customer_query(query)

    def handle_customer_query(self, query: str):
        # Example logic — you’ll improve this later
        if "loan" in query.lower():
            return self.sales_agent.provide_offer()
        elif "verify" in query.lower():
            return self.verification_agent.verify_documents()
        elif "sanction" in query.lower():
            return self.sanction_agent.generate_sanction_letter()
        else:
            return {"message": "I'm CapitalMitra — your AI loan advisor!"}