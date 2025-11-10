import os
import requests
from dotenv import load_dotenv

load_dotenv()

class SalesAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        if not self.api_key:
            raise ValueError("❌ OpenRouter API key not found. Please set OPENROUTER_API_KEY in .env")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://capitalmitra.ai",  # optional, helps OpenRouter track usage
            "Content-Type": "application/json"
        }

        # Friendly and precise tone system prompt
        self.system_prompt = (
            "You are CapitalMitra — a friendly and professional AI loan advisor. "
            "Always reply in 2–3 short, supportive sentences that make the customer feel understood. "
            "Be confident, clear, and helpful. Avoid technical jargon or long paragraphs."
        )

    def provide_offer(self, user_message: str = "Tell me about personal loans."):
        """Generate concise, friendly, and supportive AI responses using OpenRouter."""
        try:
            payload = {
                "model": "mistralai/mistral-7b-instruct",  # stable, fast & free model
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 150,
                "temperature": 0.8  # slightly creative but still focused
            }

            res = requests.post(self.api_url, headers=self.headers, json=payload)
            res.raise_for_status()
            data = res.json()

            ai_message = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "I'm here to help with your loan needs! 😊")
                .strip()
            )

            # Remove unwanted tags from AI response
            for tag in ["<s>", "</s>", "[USER]", "[/USER]"]:
                ai_message = ai_message.replace(tag, "")
            ai_message = ai_message.strip()

            # Ensure short, polished message
            if len(ai_message.split()) > 60:
                ai_message = "Here’s a quick summary: " + " ".join(ai_message.split()[:50]) + "..."

            return {"message": ai_message}

        except requests.exceptions.RequestException as e:
            return {"message": f"⚠️ Network error while contacting AI: {str(e)}"}
        except Exception as e:
            return {"message": f"⚠️ AI agent error: {str(e)}"}

    def propose_loan(self, customer: dict):
        """Create a friendly loan proposal for the given customer."""
        print(f"💼 SalesAgent: Discussing loan options with {customer['name']}")

        proposed_amount = int(customer["pre_approved_limit"] * 0.9)
        rate = 10.5
        tenure = 24

        offer_message = (
            f"🎉 Great news {customer['name']}! You’re eligible for a ₹{proposed_amount:,} loan "
            f"at {rate}% interest for {tenure} months. "
            "Let’s proceed whenever you’re ready — I’ll guide you step by step! 🤝"
        )

        return {
            "proposed_amount": proposed_amount,
            "rate": rate,
            "tenure": tenure,
            "message": offer_message
        }