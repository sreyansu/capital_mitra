class SalesAgent:
    def provide_offer(self):
        # Placeholder for AI agent logic
        return {}
    def propose_loan(self, customer):
        print(f"💼 SalesAgent: Discussing loan options with {customer['name']}")

        # For simplicity, offer 90% of pre-approved limit
        proposed_amount = int(customer["pre_approved_limit"] * 0.9)
        rate = 10.5  # fixed for demo
        tenure = 24  # months

        print(f"💰 Proposed loan: ₹{proposed_amount}, {rate}% for {tenure} months")
        return {
            "proposed_amount": proposed_amount,
            "rate": rate,
            "tenure": tenure
        }