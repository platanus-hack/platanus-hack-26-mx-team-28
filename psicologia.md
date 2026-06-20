# Fundamento psicológico de la feature — Perfil Emocional Infantil

> Documento de respaldo teórico para [`idea.md`](./idea.md). Destila la literatura citable que ancla
> las decisiones de diseño: qué validez tienen las técnicas proyectivas narrativas, qué marco define
> las dimensiones (Sección 4 de la idea), qué umbrales separan "señal" de "variación normal", y qué
> exige el marco legal/ético. **Cada afirmación de producto debe poder rastrearse a una fila de la
> tabla de fuentes al final.**

---

## 0. TL;DR para el equipo (lo que hay que internalizar)

1. **Las técnicas proyectivas narrativas tienen validez real pero limitada.** Sirven como
   **suplemento** de una evaluación clínica, **nunca como diagnóstico**. Esto no es una opinión
   cautelosa nuestra: es la conclusión explícita de la revisión sistemática más reciente del campo
   (Santillo et al., 2025).
2. **No existe evidencia de validación de estas técnicas en formato digital, gamificado y sin
   terapeuta presente.** Cero. La revisión PRISMA 2025 cubre solo instrumentos en papel
   administrados por profesionales. Nuestro producto opera en un terreno *sin respaldo psicométrico
   publicado* → esto obliga a un lenguaje de producto humilde y a no afirmar precisión clínica.
3. **El marco que define nuestras dimensiones es CASEL** (5 competencias socioemocionales, validado
   3–18 años), complementado por **Ma (2013)** para el eje moral por edad y **Erikson** para la
   lente del estadio evolutivo. Esto reemplaza dimensiones "inventadas por el equipo" (guardrail de
   `idea.md` §8).
4. **El mayor riesgo del producto es el falso positivo.** La literatura de DSM exige tres
   condiciones acumulativas antes de hablar de algo "clínicamente relevante": **persistencia**,
   **impairment funcional** (distrés o disfunción real) y **rareza respecto a la norma evolutiva**.
   Un comportamiento de juego/ensayo de límites es desarrollo normal, no una señal.
5. **Legalmente, datos emocionales de menores = categoría especial.** COPPA (consentimiento parental
   verificable, <13 años) y GDPR (mental data = dato sensible) aplican. El enfoque "nunca
   diagnostica, nunca aconseja, deriva a profesional" no es solo ético: es el mínimo legal.

---

## 1. ¿Sirve la premisa? Validez de las técnicas proyectivas narrativas

La premisa de `idea.md` §7 — *que las decisiones de un niño dentro de una narrativa revelan estados
internos* — está respaldada por una tradición clínica real (tests de apercepción y storytelling
terapéutico), pero con un techo de validez que hay que respetar.

### Hallazgo central (Santillo et al., 2025 — revisión sistemática PRISMA, *Children*)

- Revisión de literatura **2010–2024** (PubMed, PEP, Cochrane), técnicas proyectivas **constructivas**
  en edades **4–18 años** (excluye Rorschach por estar ya muy cubierto).
- **Calidad metodológica media-baja: score promedio 4.36/9** (mediana 4.0; rango 2–8) → "fair quality".
- **52% de los estudios (13 de 25) no reportan ningún dato psicométrico** del test usado.
- Donde sí hay datos, la **confiabilidad inter-evaluador puede ser alta** en estudios bien hechos:
  - Bears Family Test: Cohen's κ = 0.96
  - Draw-a-Person: test-retest 0.74
  - CAT: ICC = 0.97
  - TAT + funciones ejecutivas: ICC 0.89–0.94
  - → La señal **existe y puede ser confiable cuando el instrumento y el evaluador están calibrados**.
- **Conclusión textual de los autores:** *"While not definitive diagnostic tools, they serve as
  effective supplements in clinical assessments... when applied with awareness of their limitations"*
  y *"should not be regarded as standalone diagnostic instruments, but rather as adjuncts... when
  applied by trained professionals."*

### Estado de los instrumentos clásicos relevantes

| Instrumento | Origen | Validez / confiabilidad | Validación digital |
|---|---|---|---|
| **CAT** (Children's Apperception Test) | Bellak & Adelman, 1949 | Validez moderada; baja confiabilidad inter-evaluador; estandarización pobre, normas débiles, alta subjetividad, susceptible a *faking* | **No existe** |
| **RATC** (Roberts Apperception Test for Children) | McArthur & Roberts, 1982 | Validez convergente/discriminante adecuada; confiabilidad mínimamente aceptable. Un estudio forense 2023 (N=75) lo revalidó | **No existe** (el estudio 2023 es en papel) |
| **Mutual Storytelling Technique** | Gardner, 1968/1971 | Uso clínico con terapeuta; **sin validación psicométrica formal**; interpretación subjetiva, requiere experto | **No existe** |

### Implicaciones de diseño (qué hacer con esto)

- ✅ **Usar como "instrumento de señal", no de diagnóstico.** Es exactamente el framing de `idea.md`
  §4–§6. La literatura lo respalda.
- ⚠️ **El cuello de botella es la confiabilidad de la interpretación.** Donde los tests fallan es en
  la **subjetividad del evaluador**. En nuestro caso el "evaluador" es un LLM clasificador → la
  confiabilidad depende enteramente de una **rúbrica de clasificación cerrada y auditable** (mapear
  cada opción de respuesta a un polo de dimensión *antes* de mostrarla, no interpretar texto libre
  post-hoc). Esto refuerza la **separación de motores** de `idea.md` §2/§8: el motor que clasifica
  no debe "interpretar" creativamente, debe aplicar un mapeo pre-registrado.
- 🚩 **No reclamar precisión clínica en ningún copy.** No hay un solo estudio que valide esto en
  digital sin terapeuta. El producto debe presentarse como **"observación de patrones para
  conversar con un profesional"**, no como screening.

---

## 2. Marco que define las dimensiones (reemplaza heurísticas inventadas)

`idea.md` §4 propone 6 dimensiones y pide anclarlas a teoría reconocida (§8). Recomendación:
**CASEL como columna vertebral**, con **Ma (2013)** para calibrar expectativas por edad y **Erikson**
para la lente evolutiva.

### Por qué elegimos esta combinación (la razón de fondo)

El guardrail de `idea.md` §8 dice que las dimensiones "deben estar respaldadas por literatura
citable, no ser heurísticas inventadas por el equipo". Eso obliga a una decisión: **¿qué teoría
define los ejes que medimos?** Evaluamos los cuatro marcos candidatos contra tres criterios que
nuestro producto necesita sí o sí, y ninguno los cumple todos solo — por eso combinamos tres.

Los tres criterios que el marco debía cumplir:

1. **Cubrir el rango 3–10 años** (la edad de nuestros usuarios), no un tramo distinto.
2. **Incluir lo afectivo, no solo lo cognitivo.** Medimos emociones y conducta (miedo, empatía,
   frustración), no solo razonamiento abstracto.
3. **Mapear 1-a-1 con nuestras 6 dimensiones** sin forzar, y dar un lenguaje de constructos
   reconocido que un profesional pueda validar.

| Marco | ¿3–10 años? | ¿Afectivo? | ¿Mapea a las 6 dimensiones? | Rol que le dimos |
|---|---|---|---|---|
| **CASEL** | ✅ validado 3–18 | ✅ afectivo + cognitivo | ✅ 5 competencias cubren regulación, empatía, decisión, relación | **Columna vertebral** |
| **Ma (2013)** | ✅ kínder–primaria | ✅ necesidades + altruismo | Parcial (eje moral) | **Calibrador por edad** |
| **Erikson** | ✅ por estadios | ✅ | Parcial (autonomía/iniciativa) | **Lente evolutiva** |
| **Kohlberg** | ❌ Stage 2 recién a los 9+ | ❌ puramente cognitivo | ❌ solo justicia/obediencia | Descartado como base (solo matiz) |
| **Bowlby (apego)** | ✅ 0–5 crítico | ✅ | Solo 1 eje (confianza/apego) | Anclaje puntual de 1 dimensión |

**Por qué CASEL es la columna y no los otros:** es el único de los cinco que cumple los tres
criterios a la vez. Sus 5 competencias **ya son**, casi literalmente, nuestras dimensiones:
self-management = regulación emocional, social awareness = empatía, responsible decision-making =
honestidad/decisión, relationship skills = confianza/cooperación. No tenemos que inventar nada — solo
mapear. Además está validado en contexto **educativo** (no clínico), que es exactamente nuestro
terreno: observamos a un niño jugando, no a un paciente en consulta. Eso baja el riesgo de sobre-
interpretar (ver Sección 3 y 4).

**Por qué necesitamos a Ma y Erikson además de CASEL:** CASEL te dice *qué* competencias existen,
pero no *qué es normal a cada edad*. Un niño de 4 años egocéntrico no tiene un "déficit de empatía" —
está justo donde Ma (Estadio 1) y Erikson predicen. Sin esta capa de calibración por edad, el
producto generaría falsos positivos masivos (el riesgo #1, Sección 3). Ma aporta la norma del eje
**moral/altruista** por edad; Erikson aporta la del eje **autonomía/iniciativa**. Son el "cero" contra
el cual CASEL mide.

**Por qué descartamos a Kohlberg como base:** es el candidato "obvio" para lo moral, pero falla los
tres criterios para nuestra edad. Su Stage 1 preconvencional (<9 años) solo captura
obediencia-castigo, es **puramente cognitivo** (ignora el afecto) y su Stage 2 recién aparece a los
9+. Para un niño de 4–8 años no tiene resolución. Lo dejamos solo como *matiz* del eje
honestidad/justicia, nunca como marco.

### Por qué CASEL (y no Kohlberg) es el marco base

- **CASEL** (Collaborative for Academic, Social, and Emotional Learning) define **5 competencias
  socioemocionales interrelacionadas**, validadas y usadas en educación **3–18 años**, integrando lo
  afectivo y lo cognitivo:
  1. **Self-awareness** — reconocer emociones/valores propios.
  2. **Self-management** — *regular* emociones, pensamientos y conductas (incluye manejo de
     frustración/impulso).
  3. **Social awareness** — empatía, tomar perspectiva del otro.
  4. **Relationship skills** — cooperar, comunicar, pedir/ofrecer ayuda, resolver conflicto.
  5. **Responsible decision-making** — decisiones éticas y responsables.
- **Kohlberg NO sirve como base** para 3–10 años: su Stage 1 preconvencional (<9 años) solo captura
  obediencia/castigo, es muy cognitivo y poco afectivo. Útil solo como matiz para el eje
  honestidad/justicia, no como marco.
- **Bowlby (apego)** es apropiado y específico para el eje confianza/apego, sobre todo 3–6 años
  (apego seguro vs. inseguro, base de la regulación emocional).

### Mapeo: dimensiones de `idea.md` §4 → marco citable

| Dimensión (idea.md) | Anclaje teórico principal | Competencia / constructo |
|---|---|---|
| **Regulación emocional** | CASEL · Erikson (confianza básica) | Self-management |
| **Confianza / apego** | Bowlby (teoría del apego) · CASEL | Relationship skills / apego seguro-inseguro |
| **Honestidad / integridad** | CASEL · Kohlberg (matiz) · Ma | Responsible decision-making |
| **Empatía / agresión** | CASEL · Ma (altruismo) | Social awareness |
| **Autonomía / dependencia** | Erikson (Autonomía vs. Vergüenza; Iniciativa vs. Culpa) | Self-management / iniciativa |
| **Riesgo / cautela** | Erikson (Iniciativa vs. Culpa) | (eje exploratorio; el más débilmente anclado — ver nota) |

> **Nota sobre "Riesgo / cautela":** es la dimensión con menor anclaje directo en un marco
> validado. Se sostiene vía Erikson (Iniciativa vs. Culpa, 3–6 años), pero conviene tratarla como
> dimensión secundaria/exploratoria y **no escalar alertas** basándose en ella sola.

### Calibración por edad (Ma, 2013 — modelo moral integrado, *Frontiers in Public Health*)

Ma integra necesidades psicológicas + altruismo + razonamiento de justicia en 3 estadios. Úsalo para
**no esperar de un niño de 4 años lo que es propio de uno de 9**:

- **Estadio 1 (≈3–6 años):** supervivencia, egocentrismo, obediencia a la autoridad. *Egoísmo
  funcional es normal aquí — no es "falta de empatía".*
- **Estadio 2 (≈6–9 años):** necesidades de afecto, altruismo recíproco ("te ayudo si me ayudas").
- **Estadio 3 (≈9–12 años):** pertenencia, altruismo de grupo primario, expectativas interpersonales
  mutuas.

**Uso en producto:** el generador de dilemas (idea.md §2) debe calibrar la *dificultad moral* del
dilema al estadio del niño, y el dashboard debe interpretar tendencias **contra la norma de su
edad**, no contra un ideal adulto. Erikson aporta la misma lógica: el "trabajo" evolutivo de 3–6 es
iniciativa vs. culpa, y el de 6–12 es **industria vs. inferioridad** (competencia, logro).

---

## 3. Evitar falsos positivos (el riesgo #1 del producto)

El daño más probable de este producto no es fallar un diagnóstico — es **generar ansiedad innecesaria
en padres** marcando como problema lo que es desarrollo normal. La literatura DSM da los umbrales.

### Las 3 condiciones que deben cumplirse *juntas* (Cooper, 2013, *Can J Psychiatry*)

1. **Persistencia:** el patrón debe ser sostenido, no eventos aislados. *Una decisión nunca cuenta.*
2. **Impairment / harm:** debe causar **distrés significativo o afectar el funcionamiento** real del
   niño (DSM "clinical significance criterion"). La *presencia* de un síntoma no basta. (Cooper
   matiza que el harm no siempre correlaciona con intensidad/frecuencia → por eso no se puede
   automatizar un umbral simple; se deriva, no se concluye.)
3. **Rareza respecto a la norma ("zones of rarity"):** el patrón debe ser **raro fuera del contexto
   normativo de su edad** + persistente. Comportamiento de juego, fantasía y ensayo de límites =
   desarrollo normal.

### Reglas cuantitativas accionables (para el motor de alertas)

- **Mínimo de muestra antes de mostrar tendencia:** nunca reportar patrón con 1–2 decisiones. El
  dashboard ya exige "indicador de cuántos datos hay detrás" (idea.md §5) → fijar un **piso (ej.
  ≥5–8 observaciones de la misma dimensión)** antes de cualquier lenguaje de tendencia.
- **Heurística de carga sintomática 2×:** la literatura de screening (estudios de nominación docente)
  encuentra que los falsos positivos exhiben ~2× la carga sintomática para acercarse al nivel
  clínico. Traducción: el umbral de alerta debe ser **conservador y alto**, no sensible.
- **Variación normal del desarrollo:** niños más jóvenes dentro de un mismo grado muestran mayor tasa
  de "diagnóstico" (ej. ADHD) solo por estar evolutivamente atrás → **siempre normalizar por edad
  exacta**, no por curso/grado.

### Implicaciones de diseño

- El dashboard describe **patrones observables**, nunca causas ni etiquetas (ya en idea.md §5).
- El agente de insights (idea.md §6) describe el patrón en términos neutros y **deriva**; el único
  momento de **escalamiento inmediato** son banderas de seguridad (señales repetidas de miedo
  extremo, autolesión, indicios de abuso) — y aun ahí el lenguaje es "consulta a un profesional ya",
  no "tu hijo tiene X".
- Construir una **lista de exclusión** por eventos de vida (idea.md §3): no activar dilemas de
  pérdida/separación en duelo reciente. Esto también evita inducir respuestas que el sistema luego
  malinterprete como señal (riesgo de contaminación de datos).

---

## 4. Antecedentes y críticas éticas de productos similares

No somos los primeros; los problemas conocidos de la categoría deben tratarse como requisitos, no
sorpresas:

- **Gamified digital mental health interventions** (scoping reviews): preocupaciones de *accuracy,
  bias, privacy*; riesgo de **over/under-reporting**; **falta de validación clínica**.
- **Digital Psychological Screening Tools / wearables para niños** (2024): *accuracy y bias*,
  vulnerabilidades de privacidad, necesidad de validación **antes** de implementar en práctica
  pediátrica.
- **Interactive storytelling for children**: riesgos de aislamiento social, desensibilización,
  privacidad/datos.
- **Contaminación de datos fuera del setting clínico:** *"observation and inference outside sterile
  clinical settings may lead to data contamination"* — observar a un niño jugando en casa no es lo
  mismo que evaluarlo en consulta. Nuestra señal es **ruidosa por construcción** → otra razón para
  el lenguaje humilde y el "consulta a un profesional".
- **Preocupación parental documentada:** apps que infieren "características sensibles de la salud del
  niño" y cómo eso podría **afectar su futuro**. → transparencia total sobre qué se guarda y por qué.

---

## 5. Marco legal/ético (mínimos no negociables)

| Regulación | Jurisdicción | Qué exige (relevante para nosotros) |
|---|---|---|
| **COPPA** | EE.UU. (FTC) | **Consentimiento parental verificable** para recolectar datos personales de menores de 13. Datos emocionales/sensibles incluidos. |
| **GDPR** | Europa | Datos sobre **estados mentales = categoría especial** de dato sensible → protección reforzada. El *affective computing* que infiere estados mentales cae aquí. |
| **DSM-5 (criterio de significancia clínica)** | Práctica psicológica (internacional) | Ningún producto debe **afirmar diagnóstico** sin cumplir el criterio de impairment significativo. |

### Checklist de cumplimiento para el producto

- [ ] **Nunca diagnostica** (idea.md §8) — alineado con DSM y con la conclusión "supplement, not
      diagnostic" de Santillo.
- [ ] **Nunca da consejo psicológico** directo (idea.md §8).
- [ ] **Consentimiento parental verificable** antes de recolectar (COPPA).
- [ ] **Datos emocionales tratados como categoría especial**: minimización, cifrado, propósito
      declarado, retención limitada, derecho a borrado (GDPR).
- [ ] **Transparencia con los padres** sobre qué se infiere y se guarda (preocupación parental
      documentada).
- [ ] **Derivación con umbrales claros**: persistencia + impairment + múltiples observaciones
      consistentes antes de recomendar profesional (no 1–2 decisiones).
- [ ] **Directorio/canal de derivación real** (idea.md §6), no un "habla con alguien" genérico.
- [ ] **El niño no se siente evaluado** — sigue siendo un cuento (idea.md §8).

---

## 6. Cómo esto modifica/confirma el diseño de `idea.md`

| Decisión de `idea.md` | Veredicto de la literatura |
|---|---|
| Usar decisiones narrativas como señal emocional (§1, §7) | ✅ **Respaldado** como *suplemento*, con techo de validez bajo. No reclamar más. |
| Separar motor que genera el dilema del que clasifica (§2, §8) | ✅ **Reforzado**: la confiabilidad proyectiva muere en la subjetividad del evaluador → clasificación debe ser mapeo pre-registrado, no interpretación libre. |
| Dimensiones de §4 | ⚠️ **Re-anclar a CASEL + Ma + Erikson** (Sección 2 aquí). "Riesgo/cautela" es la más débil. |
| Dashboard de tendencias, no decisiones aisladas (§5) | ✅ **Crítico y correcto.** Fijar piso de muestra (≥5–8) y normalizar por edad exacta. |
| Agente sin diagnóstico, deriva a profesional (§6) | ✅ **Legal y éticamente obligatorio**, no opcional. |
| Escalamiento inmediato para banderas de seguridad (§6) | ✅ Correcto, pero con lenguaje "consulta ya", nunca etiqueta. |
| Guardrails §8 | ✅ Todos respaldados por fuente citable (ver tabla final). |
| **Lo que falta** | 🚩 Reconocer explícitamente en el producto que **no hay validación digital sin terapeuta** y diseñar el copy en consecuencia (humildad, no precisión clínica). |

---

## 7. Fuentes citables

| # | Tema | Cita | Enlace |
|---|---|---|---|
| 1 | Validez técnicas proyectivas (revisión sistemática) | Santillo, G., et al. (2025). *Projective in Time: A Systematic Review on the Use of Construction Projective Techniques in the Digital Era—Beyond Inkblots.* **Children, 12(4):406.** DOI: 10.3390/children12040406 | [MDPI](https://www.mdpi.com/2227-9067/12/4/406) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12025577/) |
| 2 | Marco moral por edad | Ma, H. K. (2013). *The Moral Development of the Child: An Integrated Model.* **Frontiers in Public Health, 1:57.** DOI: 10.3389/fpubh.2013.00057 | [Frontiers](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2013.00057/full) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3860007/) |
| 3 | Marco socioemocional (dimensiones) | CASEL. *What Is the CASEL Framework? — 5 Core Competencies.* | [CASEL](https://casel.org/fundamentals-of-sel/what-is-the-casel-framework/) |
| 4 | Falsos positivos / umbral clínico | Cooper, R. V. (2013). *Avoiding False Positives: Zones of Rarity, the Threshold Problem, and the DSM Clinical Significance Criterion.* **Can J Psychiatry, 58(11):606–611.** | [SAGE](https://journals.sagepub.com/doi/10.1177/070674371305801105) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/24246430/) |
| 5 | Validación RATC (muestra forense) | RATC validation study, forensic sample (2023), N=75. PubMed 37004420 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/37004420/) |
| 6 | Límites de proyectivas | Piotrowski (2015); Lilienfeld et al. (2000); Minulescu (2000) — citados en literatura de assessment infantil proyectivo | — |
| 7 | Erikson (estadios socioemocionales) | LibreTexts Psychology — *Socioemotional Development in Middle and Late Childhood* | [LibreTexts](https://socialsci.libretexts.org/) |
| 8 | Ética salud mental digital jóvenes | Heubeck, J., et al. (2021). *Digital Mental Health for Young People: A Scoping Review of Ethical Promises and Challenges.* | TUM Portal |
| 9 | Ética screening con wearables en niños | *Using Wearable Digital Devices to Screen Children for Mental Health Conditions* (2024). PubMed 38794067 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/38794067/) |
| 10 | Privacidad de menores | FTC — *Children's Online Privacy Protection Rule (COPPA)* | [FTC](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa) |
| 11 | Datos mentales / dato sensible | *Mental data protection and the GDPR* (2022). PMC/NIH | [PMC](https://pmc.ncbi.nlm.nih.gov/) |
| 12 | Perspectivas multi-stakeholder screening | *Multi-stakeholder Perspectives on Mental Health Screening Tools* (2024). ACM Digital Health | ACM |

> **Correcciones a la nota original de Perplexity:** (a) Cooper 2013 es **pp. 606–611** (no 600–601);
> (b) el review de Santillo cubre **2010–2024, edades 4–18, instrumentos en papel** — su quality
> score promedio es **4.36/9** (la cifra "4.4/9" es el mismo dato redondeado); (c) el review **no**
> evalúa adaptaciones digitales: confirma que la **ausencia de validación digital es total**, lo que
> es un argumento de diseño, no un detalle.
