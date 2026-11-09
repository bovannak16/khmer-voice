"""Khmer Voice Studio - backend (FastAPI + edge-tts)

Run:  uvicorn server:app --host 0.0.0.0 --port 8000
"""
import asyncio
from pathlib import Path

import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE = Path(__file__).parent
VOICES = {
    "male": "km-KH-PisethNeural",     # សំឡេងប្រុស
    "female": "km-KH-SreymomNeural",  # សំឡេងស្រី
}

app = FastAPI(title="Khmer Voice Studio")


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    voice: str = "female"      # male | female
    rate: int = Field(0, ge=-50, le=100)     # % speed
    pitch: int = Field(0, ge=-50, le=50)     # Hz
    volume: int = Field(0, ge=-50, le=50)    # %


@app.get("/api/voices")
def voices():
    return {"voices": VOICES}


@app.post("/api/tts")
async def tts(req: TTSRequest):
    voice = VOICES.get(req.voice)
    if not voice:
        raise HTTPException(400, "voice must be 'male' or 'female'")
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "empty text")

    last_err = None
    for attempt in range(3):
        try:
            comm = edge_tts.Communicate(
                text,
                voice,
                rate=f"{req.rate:+d}%",
                pitch=f"{req.pitch:+d}Hz",
                volume=f"{req.volume:+d}%",
            )
            audio = bytearray()
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
            if audio:
                return Response(bytes(audio), media_type="audio/mpeg")
            last_err = "no audio returned"
        except Exception as e:  # network / service errors
            last_err = str(e)
        await asyncio.sleep(0.6 * (attempt + 1))
    return JSONResponse({"error": f"TTS failed: {last_err}"}, status_code=502)


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")
