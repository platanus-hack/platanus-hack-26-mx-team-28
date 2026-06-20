"""Tests de generación de imágenes (Nano Banana)."""

import os

import pytest

from images import attach_images, generate_image, to_data_uri


def test_to_data_uri_prefix():
    uri = to_data_uri(b"\x89PNG\r\n\x1a\nhello")
    assert uri.startswith("data:image/png;base64,")


def test_attach_images_sets_field_even_without_prompt():
    # sin prompt no se genera nada (None), pero el campo 'image' queda presente
    pages = [{"text": "x", "image_prompt": ""}]
    out = attach_images(pages)
    assert "image" in out[0] and out[0]["image"] is None


@pytest.mark.skipif(not os.environ.get("GOOGLE_API_KEY"),
                    reason="sin GOOGLE_API_KEY: test en vivo omitido")
def test_generate_image_live_returns_png():
    png = generate_image("a happy yellow cartoon monkey holding a banana on a rocket")
    assert png is not None, "no se generó imagen"
    assert png[:8] == b"\x89PNG\r\n\x1a\n", "los bytes no son un PNG válido"
    assert len(png) > 1000
