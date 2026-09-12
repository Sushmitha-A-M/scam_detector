def score_risk(*, ai_probability=0, scam_probability=0, manipulation_probability=0, urgency=0, financial=0, credential=0):
    score = round(max(ai_probability, manipulation_probability) * 55 + scam_probability * 25 + max(urgency, financial, credential) * 20)
    score = max(0, min(100, score))
    level = "LOW" if score <= 30 else "MEDIUM" if score <= 60 else "HIGH" if score <= 80 else "CRITICAL"
    return {"risk_score": score, "risk_level": level}