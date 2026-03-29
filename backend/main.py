import os
import json
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import asyncio
from dotenv import load_dotenv

load_dotenv()

from agents.coordinator import run_disaster_pipeline
from services.geo import resolve_place
from services.imd_scraper import get_live as get_imd_live
from services.openweather import get_current_weather
from services.voice import generate_voice_alert
from services.pdf_export import generate_pdf


app = FastAPI(title="INDRA AI v2", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    version: str
    env_check: dict


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "env_check": {
            "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
            "openweather_key_set": bool(os.getenv("OPENWEATHER_API_KEY")),
        },
    }


class GenerateRequest(BaseModel):
    place: str


@app.post("/api/generate/stream")
async def generate_stream(request: GenerateRequest):
    """
    Stream disaster response brief using SSE.
    API key is read from environment variables.
    """
    if not request.place:
        raise HTTPException(status_code=400, detail="Place parameter required")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured in server environment")

    async def event_stream():
        async for event in run_disaster_pipeline(request.place, openai_api_key):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/imd/live")
def get_imd():
    """Get live IMD cyclone data."""
    return get_imd_live()


@app.get("/api/weather")
def get_weather(place: str):
    """Get current weather for a place."""
    if not place:
        raise HTTPException(status_code=400, detail="place parameter required")

    return get_current_weather(place)


@app.get("/api/place/resolve")
def resolve_geo(q: str):
    """Resolve a place name to geographic coordinates."""
    if not q:
        raise HTTPException(status_code=400, detail="q parameter required")

    try:
        result = resolve_place(q)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class VoiceRequest(BaseModel):
    text: str
    lang: str


@app.post("/api/voice")
def generate_voice(request: VoiceRequest):
    """Generate voice alert for text in specified language."""
    if not request.text:
        raise HTTPException(status_code=400, detail="text required")

    if request.lang not in ["te", "hi", "en", "or", "ta"]:
        raise HTTPException(status_code=400, detail="Invalid language code")

    try:
        audio_base64 = generate_voice_alert(request.text, request.lang)
        return {"audio_base64": audio_base64, "lang": request.lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PDFRequest(BaseModel):
    brief: dict


@app.post("/api/pdf")
def export_pdf(request: PDFRequest):
    """Generate PDF report from disaster brief."""
    try:
        pdf_bytes = generate_pdf(request.brief)
        return FileResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            filename=f"INDRA-Brief-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
