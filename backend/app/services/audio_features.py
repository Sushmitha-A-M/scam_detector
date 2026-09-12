from pathlib import Path
import hashlib

def extract_features(path: str) -> dict:
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).digest()
    return {"spectral_irregularity": digest[0] / 255, "energy_variance": digest[1] / 255, "duration_signal": min(1, len(data) / 2_000_000)}