# Branding — dominikito

> Guía de estilo oficial de **dominikito** (cuentos interactivos infantiles). Alimenta la **interfaz**
> (lector del niño y, después, dashboard de padres) y el **estilo de las ilustraciones** que genera
> Nano Banana a partir de los `image_prompt`.

## 1. Personalidad de marca
- **Amigable · Divertido · Inspirador · Seguro · Cercano · Educativo** (tono de comunicación oficial).
- Mundo **espacial y lúdico**: un monito explorador y una **nave/OVNI** amable. Aventura + ternura.
- Mascotas: **monito café** (expresivo, simpático, con su banana) + **nave espacial morada** (con
  ojos grandes, simpática). Tema: exploración, descubrimiento, afecto.

## 2. Logotipo / Wordmark
- Palabra **"dominikito"** en **minúsculas**, tipografía redondeada y gruesa (Baloo 2 Bold).
- Letras multicolor: **"do"** morado, **"minik"** lila/morado, **"ito"** con un punto-estrella ⭐
  sobre la "i" y cierre en **amarillo/naranja**.
- El monito cuelga de la nave a la izquierda del wordmark.
- Versiones de color del logo según fondo (ver §7).

## 3. Paleta de color (oficial)
| Token | Hex | Rol |
|---|---|---|
| `--purple` | `#4B2AD4` | **Primario** (morado de marca) |
| `--lila` | `#9C7CF6` | Secundario (lila) |
| `--lila-soft` | `#DCC6FF` | Lila muy claro / fondos suaves |
| `--yellow` | `#FFC522` | Acento (estrella, banana, destaques) |
| `--orange` | `#FF9D1A` | Acento cálido |
| `--pink` | `#FF7BAE` | Acento (corazón / afecto) |
| `--ink` | `#2E168F` | Morado oscuro: texto y contornos |
| `--cream` | `#FFF2DA` | Fondo claro (papel cálido) |
| `--mist` | `#F6F7FA` | Gris muy claro / superficies |
| `--brown` | `#A6632A` | Café del monito |
- Contornos en `--ink` (morado oscuro, no negro). Sombras **suaves**.

## 4. Tipografía
- **Principal (títulos):** **Baloo 2 Bold**.
- **Secundaria (cuerpo):** **Nunito** (Regular / Medium; 600-800 para niños).
- Textos del cuento grandes, interlineado generoso (lectura infantil / acompañada).

## 5. Elementos gráficos e iconografía
- **Elementos:** estrella amarilla, círculos (lila/rosa), nubecita crema, **camino punteado** curvo (lila).
- **Íconos** (redondeados, con halo blanco): estrella ⭐, corazón 💗, luna 🌙, nube ☁️, cohete 🚀.
- Esquinas muy redondeadas (radios 18-28px), bordes de contorno estilo caricatura, sombras suaves.

## 6. Estilo de ilustración (para Nano Banana)
Oficial: **"Personajes redondeados, expresivos y amigables. Colores vibrantes con sombras suaves.
Ambiente lúdico y positivo."**
Sufijo recomendado para los `image_prompt`:
> `cute rounded expressive friendly characters, vibrant colors with soft shadows, playful and
> positive mood, purple and lilac dominant palette with yellow, orange and pink accents, clean
> cartoon style with soft outlines, gentle lighting, cream background, no text in the image`
- Personajes con **ojos grandes** y expresiones cálidas; escenas seguras y luminosas.
- Recurrentes de marca cuando encajen: monito café, nave/OVNI morada, estrellitas, lunas, nubes.
- Evitar: realismo, miedo, oscuridad, violencia, texto dentro de la imagen.

## 7. Uso de color del logo según fondo
- Sobre **morado** / **lila** / **oscuro** → wordmark **blanco**.
- Sobre **amarillo** → wordmark blanco u oscuro (contraste).
- Sobre **claro/crema** → wordmark **morado**.

## 8. Aplicaciones (significado de los íconos)
- 🔤 **abc** → Educación y aprendizaje · ⭐ → Creatividad y juego · 💗 → Afecto y cercanía ·
  🚀 → Exploración y descubrimiento.

## 9. No-negociables (coherentes con los guardrails)
- Para el niño, todo es **cuento y juego**; cero estética de test/encuesta.
- La capa "evaluativa" (polos, patrones) **nunca** se muestra en la pantalla del niño; vive solo en el
  dashboard de padres protegido.
