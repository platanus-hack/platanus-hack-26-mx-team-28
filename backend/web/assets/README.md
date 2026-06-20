# Assets fijos de marca — dominikito

Carpeta servida por FastAPI en `/assets/...`. Suelta aquí los archivos con **estos nombres exactos**
y la interfaz los usa automáticamente (si falta alguno, hay fallback y no se rompe nada).

| Archivo | Qué es | Dónde se usa | Tamaño/formato sugerido |
|---|---|---|---|
| `logo.png` | Logotipo completo "dominikito" (wordmark + monito/OVNI) | **Header** (arriba, en todas las pantallas) | PNG/SVG transparente, ~380px ancho |
| `mascot.png` | Personaje solo (monito + OVNI), sin texto | **Pantalla "Crear cuento"** (hero, sobre el formulario) | PNG transparente, ~360px alto |
| `favicon.png` | Carita del OVNI o el monito | Pestaña del navegador | PNG cuadrado 256×256 |
| `star.png` `cloud.png` `moon.png` `heart.png` `rocket.png` | Íconos estilo sticker | Decoración + pilares del **dashboard de padres** (fase siguiente) | PNG transparente ~128px |

## Dónde queda cada cosa (mapa del front)
- **Header (siempre visible):** `logo.png` reemplaza el wordmark de texto. Si no está, se muestra el
  texto "dominikito" con la paleta de marca (fallback ya implementado).
- **Pantalla 1 (Crear cuento):** `mascot.png` como hero arriba del formulario, dando la bienvenida.
- **Estado de carga:** hoy hay un emoji 🚀 animado; se puede cambiar por `mascot.png` volando (avísame).
- **Lector del niño:** las ilustraciones de cada página las genera **Nano Banana** (no son assets fijos).
- **Dashboard de padres (fase siguiente):** los íconos sticker para los pilares (Educación, Creatividad,
  Afecto, Exploración).

## Notas
- Formato: preferible **PNG transparente** (o SVG para el logo). Sin fondo.
- Los nombres deben coincidir exactamente; si quieres otros nombres, dime y ajusto el markup.
