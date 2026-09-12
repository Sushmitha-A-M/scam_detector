import json
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..config import MAX_UPLOAD_SIZE, UPLOAD_DIR
from ..database import get_db
from ..models import Scan, User
from ..security import current_user
from ..services.voice_detector import PrototypeVoiceDetector
from ..services.video_detector import PrototypeVideoDetector

router = APIRouter()
VOICE_TYPES = {"audio/wav", "audio/mpeg", "audio/mp4", "audio/ogg", "audio/x-m4a"}
VIDEO_TYPES = {"video/mp4", "video/quicktime", "video/x-msvideo", "video/x-matroska", "video/webm"}

async def save_upload(upload: UploadFile, allowed):
    if upload.content_type not in allowed: raise HTTPException(415, "Unsupported file type")
    data = await upload.read()
    if not data: raise HTTPException(400, "Uploaded file is empty")
    if len(data) > MAX_UPLOAD_SIZE: raise HTTPException(413, "File exceeds the upload limit")
    path = UPLOAD_DIR / f"{uuid4()}_{Path(upload.filename or 'upload').name}"
    path.write_bytes(data); return path

def persist(db, user, scan_type, filename, result):
    scan_id = str(uuid4()); indicators = result.get("indicators", [])
    scan = Scan(id=scan_id, user_id=user.id, scan_type=scan_type, filename=filename, risk_score=result["risk_score"], risk_level=result["risk_level"], ai_probability=result.get("ai_probability", result.get("deepfake_probability", 0)), scam_probability=result.get("scam_probability", 0), indicators=json.dumps(indicators), recommendations=json.dumps(["Do not share OTPs, passwords, or financial information.", "Verify the sender independently."]))
    db.add(scan); db.commit(); return {"scan_id": scan_id, **result, "prototype_model": True, "recommendation": "Results are experimental and should not be treated as definitive proof."}

@router.post("/voice/analyze")
async def analyze_voice(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    path = await save_upload(file, VOICE_TYPES)
    try: return persist(db, user, "voice", file.filename or "audio", PrototypeVoiceDetector().predict(str(path)))
    finally: path.unlink(missing_ok=True)

@router.post("/video/analyze")
async def analyze_video(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    path = await save_upload(file, VIDEO_TYPES)
    try: return persist(db, user, "video", file.filename or "video", PrototypeVideoDetector().predict(str(path)))
    finally: path.unlink(missing_ok=True)

@router.post("/calls/analyze")
async def analyze_call(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    path = await save_upload(file, VOICE_TYPES)
    try:
        result = PrototypeVoiceDetector().predict(str(path)); result["call_id"] = str(uuid4()); result["scam_probability"] = round(result["ai_probability"] * 0.8, 2)
        return persist(db, user, "call", file.filename or "call audio", result)
    finally: path.unlink(missing_ok=True)