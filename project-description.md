# Dominikito 🐵🛸

## ¿Qué es Dominikito?
**Dominikito** es una plataforma web innovadora que fusiona literatura infantil interactiva, inteligencia artificial generativa y psicología del desarrollo para trazar el perfil socioemocional de los niños de manera lúdica, orgánica y no invasiva. A través de cuentos interactivos ramificados, los niños toman decisiones que se convierten en señales conductuales y morales, permitiendo a los padres visualizar patrones emocionales a lo largo del tiempo. 

---

## 👁️ La Nueva Interfaz (Ruta: New Interfaces)
Los instrumentos tradicionales de evaluación psicológica para niños suelen ser impersonales, aburridos o intimidantes. **Dominikito redefine esta experiencia con una interfaz inmersiva e interactiva:**
* **Cuento Interactivo Multimodal:** El niño experimenta una historia personalizada generada dinámicamente escena a escena, acompañada de ilustraciones a medida y narración de voz fluida.
* **Toma de Decisiones Natural:** En momentos clave de la narrativa, la historia presenta dilemas morales o conductuales. El niño elige cómo debe actuar el protagonista, integrando la evaluación directamente dentro de la mecánica de juego.
* **Dashboard para Padres:** Un panel analítico privado (protegido por PIN) donde se visualizan los patrones de desarrollo acumulados del niño, sin invadir su privacidad ni condicionar su experiencia de lectura.

---

## 🧠 ¿Cómo funciona el Mapeo Socioemocional?
Para garantizar rigor científico y evitar sesgos de interpretación comunes en los modelos de lenguaje:
1. **Dilemas Pre-registrados:** En cada checkpoint de la historia, un agente de IA diseña un dilema con opciones cerradas. Cada opción está asociada a un polo conductual y de desarrollo (taxonomía CASEL + desarrollo infantil de Erikson) *antes* de que el niño responda.
2. **Evaluación Determinista:** La respuesta del niño se clasifica mediante un simple mapeo de lookup (no por una interpretación libre posterior del modelo), eliminando sesgos de confirmación.
3. **Guardrails de Seguridad:** Dominikito **nunca diagnostica ni da consejos psicológicos**. Su objetivo es describir y consolidar patrones conductuales observados para que sirvan de insumo a los padres o a profesionales de la salud mental infantil.

---

## 🛠️ Arquitectura y Stack Tecnológico
El proyecto cuenta con una robusta arquitectura desacoplada que separa la generación de contenido de la lógica de evaluación:
* **Backend de Agentes (Google ADK & Gemini):** Implementado en Python con el **Agent Development Kit (ADK)** de Google.
  * **Agente Cuentista:** Estructura y da continuidad narrativa al cuento a partir de la configuración inicial del niño (gustos, edad, temática).
  * **Agente de Dilemas:** Genera e introduce dilemas éticos relevantes y coherentes con la trama, asignando previamente cada opción de respuesta a los polos correspondientes de la taxonomía.
* **Ilustraciones de Escena:** Generadas en tiempo real usando el modelo de imágenes de Gemini, manteniendo la coherencia visual.
* **Narración por Voz (ElevenLabs):** Síntesis de voz de alta calidad con soporte multilingüe y generación de marcas de tiempo por palabra para permitir resaltado de lectura en tiempo real en la pantalla.
* **Frontend y Persistencia:** Aplicación web estática (FastAPI) comunicada directamente con **Firebase / Firestore** para la gestión de usuarios (Google Auth) y el almacenamiento local seguro del progreso de lectura y las decisiones tomadas.
