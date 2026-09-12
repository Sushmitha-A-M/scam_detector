from .audio_features import extract_features
from .risk_engine import score_risk

class BaseVoiceDetector:
    def load_model(self): pass
    def predict(self, audio_path): raise NotImplementedError

class PrototypeVoiceDetector(BaseVoiceDetector):
    """Development fallback; replace with a trained detector through this interface."""
    def predict(self, audio_path):
        features = extract_features(audio_path)
        probability = round(0.2 + features["spectral_irregularity"] * 0.55 + features["energy_variance"] * 0.15, 2)
        risk = score_risk(ai_probability=probability)
        indicators = ["Prototype acoustic feature analysis"]
        if probability > 0.62: indicators.append("Irregular spectral patterns may warrant review")
        return {"ai_probability": probability, "human_probability": round(1 - probability, 2), **risk, "confidence": round(0.55 + probability * 0.3, 2), "indicators": indicators}