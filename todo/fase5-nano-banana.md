# Fase 5 — Nano Banana (ilustraciones reales)

> Contexto en `todo/`. Estilo en [`../branding.md`](../branding.md) §7.

## Objetivo
Generar la ilustración real de cada página (modelo `gemini-2.5-flash-image`), con el estilo de marca,
y mostrarla en el lector. Se generan **junto con la escena** (servidor → data-URI embebido).

## Estado — ✅ NANO BANANA CABLEADO Y PROBADO
- [x] `backend/images.py` (generate_image + attach_images + caché + sufijo de marca)
- [x] `api.py` adjunta imágenes en /api/story/start y /api/story/next
- [x] `web/app.js` muestra `<img>` (placeholder si falla)
- [x] `web/styles.css` .illus-img
- [x] Verificación: test en vivo PNG válido en 6.5s (gemini-2.5-flash-image); deterministas verde
- [ ] PENDIENTE: probar end-to-end en el navegador (crear cuento → ver ilustraciones)

## Decisiones
- Modelo: `gemini-2.5-flash-image` (env `IMAGE_MODEL`).
- Generación junto con la escena (no perezosa).
- Si una imagen falla (cuota/error) → placeholder, el cuento no se rompe.

## Fuera de alcance
Persistir imágenes en disco/CDN (hoy van como data-URI), imágenes del dashboard.
