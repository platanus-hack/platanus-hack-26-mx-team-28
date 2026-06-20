# Fase 6 — Lectura en voz alta con ElevenLabs (TTS)

> Contexto en `todo/`. Una voz natural narra el cuento. Botón "🔊 Léemelo" por escena.

## Objetivo
El niño toca "🔊 Léemelo" en una escena → ElevenLabs (`eleven_multilingual_v2`) narra el texto.
Generación bajo demanda (cuida créditos), audio cacheado por texto+voz.

## Estado
- [x] `backend/tts.py` (synthesize + list_voices + caché)
- [x] `api.py` +POST /api/tts (audio/mpeg) +GET /api/voices
- [x] `web/app.js` botón "🔊 Léemelo" por escena + reproducción + parar al cambiar de escena
- [x] `web/styles.css` .btn.read · `requirements.txt` +elevenlabs (instalado)
- [x] `tests/test_tts.py`
- [ ] PENDIENTE usuario: `ELEVENLABS_API_KEY` en `backend/.env`
- [ ] Verificación en vivo (synthesize PNG/MP3) + elegir voz vía /api/voices

## Config (env)
`ELEVENLABS_API_KEY` (requerida), `ELEVENLABS_MODEL=eleven_multilingual_v2`,
`ELEVENLABS_VOICE_ID` (opcional; default "Rachel" 21m00Tcm4TlvDq8ikWAM).

## Fuera de alcance
Karaoke/resaltado, descargar audiocuento, selector de voz en la UI del niño.
