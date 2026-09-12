import re

PATTERNS = {"financial": r"otp|upi|pin|password|send money|bank account|payment|refund", "urgency": r"urgent|immediately|account blocked|now", "authority": r"police|tax department|kyc|verification code"}

def detect_scam_text(text: str):
    text = text.lower()
    hits = [name for name, pattern in PATTERNS.items() if re.search(pattern, text)]
    financial = 0.75 if "financial" in hits else 0
    urgency = 0.65 if "urgency" in hits else 0
    credential = 0.8 if re.search(r"otp|pin|password|verification code", text) else 0
    overall = min(1, financial * 0.45 + urgency * 0.25 + credential * 0.3)
    return {"suspicious_phrases": hits, "urgency_score": urgency, "financial_request_score": financial, "credential_request_score": credential, "overall_scam_probability": round(overall, 2)}