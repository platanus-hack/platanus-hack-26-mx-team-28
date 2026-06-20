"""Tests de TTS (ElevenLabs)."""

import os

import pytest

from tts import synthesize


def test_empty_text_returns_none():
    assert synthesize("") is None
    assert synthesize("   ") is None


@pytest.mark.skipif(not os.environ.get("ELEVENLABS_API_KEY"),
                    reason="sin ELEVENLABS_API_KEY: test en vivo omitido")
def test_synthesize_live_returns_mp3():
    audio = synthesize("Hola, soy dominikito y te voy a contar un cuento.")
    assert audio is not None, "no se generó audio (revisa key/créditos)"
    assert len(audio) > 1000
    # MP3: empieza con 'ID3' (tag) o con un frame sync 0xFF 0xFB/0xF3/0xF2
    assert audio[:3] == b"ID3" or audio[0] == 0xFF
