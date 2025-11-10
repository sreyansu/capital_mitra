import os
import requests
import random

def generate_otp(length=6):
    return str(random.randint(10**(length-1), 10**length-1))

class OTPService:
    def __init__(self):
        self.api_key = os.getenv("FAST2SMS_API_KEY")
        self.api_url = "https://www.fast2sms.com/dev/bulkV2"
        if not self.api_key:
            raise ValueError("FAST2SMS_API_KEY not set in environment variables.")

    def send_otp(self, phone: str, otp: str):
        numbers = phone.replace("+91-", "").replace("+91", "")
        data = {
            "variables_values": otp,
            "route": "otp",
            "numbers": numbers
        }
        headers = {
            "authorization": self.api_key
        }
        response = requests.post(self.api_url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
