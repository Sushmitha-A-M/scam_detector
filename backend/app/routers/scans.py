import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Scan, User
from ..security import current_user
from ..services.report_service import create_report

router = APIRouter()
def serialize(scan):
    return {"id": scan.id, "scan_id": scan.id, "type": scan.scan_type, "filename": scan.filename, "risk_score": scan.risk_score, "risk_level": scan.risk_level, "ai_probability": scan.ai_probability, "scam_probability": scan.scam_probability, "indicators": json.loads(scan.indicators or "[]"), "recommendations": json.loads(scan.recommendations or "[]"), "created_at": scan.created_at.isoformat()}

@router.get("/scans")
def list_scans(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return [serialize(s) for s in db.query(Scan).filter_by(user_id=user.id).order_by(Scan.created_at.desc()).all()]

@router.get("/scans/{scan_id}")
def get_scan(scan_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    scan = db.query(Scan).filter_by(id=scan_id, user_id=user.id).first()
    if not scan: raise HTTPException(404, "Scan not found")
    return serialize(scan)

@router.delete("/scans/{scan_id}")
def delete_scan(scan_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    scan = db.query(Scan).filter_by(id=scan_id, user_id=user.id).first()
    if not scan: raise HTTPException(404, "Scan not found")
    db.delete(scan); db.commit(); return {"deleted": True}

@router.get("/reports/{scan_id}")
def report(scan_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    scan = db.query(Scan).filter_by(id=scan_id, user_id=user.id).first()
    if not scan: raise HTTPException(404, "Scan not found")
    path = create_report(scan, json.loads(scan.indicators or "[]"), json.loads(scan.recommendations or "[]"))
    return FileResponse(path, media_type="application/pdf", filename=f"scamshield-{scan.id}.pdf")

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user: User = Depends(current_user)):
    items = db.query(Scan).filter_by(user_id=user.id).all()
    return {"total_scans": len(items), "high_risk": sum(s.risk_level in ("HIGH", "CRITICAL") for s in items), "medium_risk": sum(s.risk_level == "MEDIUM" for s in items), "low_risk": sum(s.risk_level == "LOW" for s in items), "voice_scans": sum(s.scan_type == "voice" for s in items), "video_scans": sum(s.scan_type == "video" for s in items), "recent": [serialize(s) for s in sorted(items, key=lambda x: x.created_at, reverse=True)[:8]]}