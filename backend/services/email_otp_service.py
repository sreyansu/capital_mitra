import os
import smtplib
from email.mime.text import MIMEText
import random

def generate_otp(length=6):
    return str(random.randint(10**(length-1), 10**length-1))

class EmailOTPService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP_USER and SMTP_PASSWORD must be set in .env")

    def send_otp(self, email: str, otp: str):
        subject = "Your CapitalMitra OTP Verification Code"
        body = f"Your OTP is {otp}. Please enter this to verify your identity."
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, [email], msg.as_string())
        return True
