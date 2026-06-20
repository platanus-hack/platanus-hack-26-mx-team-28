"""Texto a voz con ElevenLabs — narración del cuento.

Generación BAJO DEMANDA (solo cuando el niño toca "Léemelo") para cuidar créditos. Devuelve MP3.
Cachea por (texto, voz) para no re-pagar repeticiones.

Requiere `ELEVENLABS_API_KEY` en el entorno (cargado por api.py desde backend/.env).
Voz y modelo configurables por env.
"""

from __future__ import annotations

import hashlib
import os

ELEVENLABS_MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
# Voz por defecto (configurable). Usa GET /api/voices para listar las de tu cuenta y elegir una.
DEFAULT_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # "Rachel" (default)
OUTPUT_FORMAT = "mp3_44100_128"

_cache: dict[str, bytes] = {}
_client = None


def _client_once():
    global _client
    if _client is None:
        from elevenlabs.client import ElevenLabs
        _client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
    return _client


def synthesize(text: str, voice_id: str | None = None) -> bytes | None:
    """Narra `text` con la voz dada (o la por defecto). Devuelve MP3, o None si falla."""
    text = (text or "").strip()
    if not text:
        return None
    voice = voice_id or DEFAULT_VOICE_ID
    key = hashlib.sha256(f"{voice}|{ELEVENLABS_MODEL}|{text}".encode("utf-8")).hexdigest()
    if key in _cache:
        return _cache[key]
    try:
        audio = _client_once().text_to_speech.convert(
            text=text,
            voice_id=voice,
            model_id=ELEVENLABS_MODEL,
            output_format=OUTPUT_FORMAT,
        )
        data = audio if isinstance(audio, (bytes, bytearray)) else b"".join(audio)
        data = bytes(data)
        if data:
            _cache[key] = data
            return data
    except Exception:  # noqa: BLE001 (cuota/red/clave: el botón avisa, no rompe el cuento)
        return None
    return None


def list_voices() -> list[dict]:
    """Lista las voces de la cuenta para que el usuario elija una (id + nombre)."""
    try:
        resp = _client_once().voices.get_all()
        return [{"id": v.voice_id, "name": v.name} for v in resp.voices]
    except Exception:  # noqa: BLE001
        return []
