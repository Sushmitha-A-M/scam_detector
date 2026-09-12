# RedFlag AI

RedFlag AI is a full-stack scam risk assessment workspace for audio, video, and explicitly authorized call audio. It returns probabilistic risk estimates, not proof of fraud or manipulation.

## Stack

- React, TypeScript, Vite, Lucide, Recharts-ready frontend
- FastAPI, SQLAlchemy, SQLite, JWT, bcrypt backend
- Replaceable Python detector interfaces for voice and video

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Create an account, then upload a supported file. The API is available at `http://localhost:8000/docs`.

## Deploy to Render

This repository includes `render.yaml`, which creates the `redflag-ai-api` backend and `redflag-ai` static frontend. Push the project to GitHub, select **New > Blueprint** in Render, connect the repository, and apply the blueprint. After deployment, open `https://redflag-ai.onrender.com`.

For a custom Render service name or domain, update `ALLOWED_ORIGINS` on the API service and `VITE_API_URL` on the frontend service before redeploying.

## Architecture

Authentication and scan ownership are handled by FastAPI dependencies and SQLite models. Upload endpoints validate MIME type and size, write to a randomized temporary path, run a detector service, persist only scan metadata, and remove the raw file in a `finally` block. Reports are generated on demand as PDFs.

`BaseVoiceDetector` and `BaseVideoDetector` are the model boundaries. The included `PrototypeVoiceDetector` uses deterministic extracted file signals and `PrototypeVideoDetector` is a clearly marked development fallback. They are not scientifically validated deepfake detectors and do not download large models automatically. Put a trained model behind these interfaces and configure its path with `VOICE_MODEL_PATH` or `VIDEO_MODEL_PATH` when integrating production inference.

## API

`POST /api/auth/register`, `POST /api/auth/login`, `GET /api/dashboard`, `POST /api/voice/analyze`, `POST /api/video/analyze`, `POST /api/calls/analyze`, `GET /api/scans`, `GET /api/scans/{scan_id}`, `DELETE /api/scans/{scan_id}`, and `GET /api/reports/{scan_id}`.

## Incoming call limitation

A normal browser cannot intercept ordinary cellular phone calls. Incoming call protection accepts audio explicitly supplied by an authorized VoIP, SIP, mobile/native, or call-center integration. This project does not access a device microphone, contacts, SMS, phone network, or private files without explicit user action.

## Security and privacy

Passwords are hashed and never stored in plain text. JWTs protect private routes. Upload names are sanitized through `Path.name`, file sizes and MIME types are checked, and temporary media is deleted after analysis. For production, set a strong `SECRET_KEY`, configure `ALLOWED_ORIGINS`, add rate limiting, and use PostgreSQL plus object storage with retention controls.

## Limitations and next steps

The prototype detectors provide integration points and honest experimental signals, not production-grade AI. Add a trained voice anti-spoofing model, frame sampling and face detection via OpenCV, optional speech-to-text, scam-language scoring, migrations, and a native authorized call-audio adapter before production deployment.