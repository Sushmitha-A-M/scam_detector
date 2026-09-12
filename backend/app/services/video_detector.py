from pathlib import Path
import hashlib
from .risk_engine import score_risk

class BaseVideoDetector:
    def predict(self, video_path): raise NotImplementedError

class PrototypeVideoDetector(BaseVideoDetector):
    """File-level development fallback. A trained frame model can replace this class."""
    def predict(self, video_path):
        digest = hashlib.sha256(Path(video_path).read_bytes()).digest()
        probability = round(0.18 + digest[0] / 255 * 0.62, 2)
        return {"deepfake_probability": probability, "authentic_probability": round(1 - probability, 2), **score_risk(manipulation_probability=probability), "frames_analyzed": 0, "faces_detected": 0, "indicators": ["Prototype video analysis", "Frame-level model integration is pending"]}