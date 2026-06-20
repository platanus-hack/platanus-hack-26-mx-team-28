// Interfaz Dominikito — cuento interactivo escena a escena (ramificado por las decisiones).

const ILLUS = ["🐵", "🛸", "⭐", "🌙", "☁️", "🍌"];
const OPT_COLORS = ["blue", "orange", "green", "purple", "red"];

let profile = null;
let storySoFar = [];   // textos de todas las páginas mostradas
let choicesMade = 0;
let total = 2;
let illusIdx = 0;
let currentAudio = null;     // Audio en reproducción (ElevenLabs)
let currentSceneText = "";   // texto de la escena actual para narrar

function esc(s) { const d = document.createElement("div"); d.textContent = s == null ? "" : String(s); return d.innerHTML; }
async function errMsg(res) { try { const j = await res.json(); return j.detail || ("HTTP " + res.status); } catch (_) { return "HTTP " + res.status; } }
function showScreen(id) { document.querySelectorAll(".screen").forEach(s => s.classList.remove("active")); document.getElementById(id).classList.add("active"); }
function toggleDev() { document.body.classList.toggle("dev"); }
function backToCreate() { stopAudio(); showScreen("screen-create"); document.getElementById("subtitle").textContent = "Cuentos que escuchan a tu peque"; }

function stopAudio() {
  if (currentAudio) { try { currentAudio.pause(); } catch (_) {} currentAudio = null; }
}

function readScene() {
  const btn = document.getElementById("read-btn");
  // si ya está sonando, este toque lo detiene
  if (currentAudio && !currentAudio.paused) {
    stopAudio(); if (btn) btn.textContent = "🔊 Léemelo"; return;
  }
  if (!currentSceneText) return;
  // IMPORTANTE: play() debe iniciarse SINCRÓNICO dentro del clic; si no, el navegador bloquea el audio.
  // Por eso usamos una URL GET como src y NO hacemos await antes de play().
  currentAudio = new Audio("/api/tts?text=" + encodeURIComponent(currentSceneText));
  if (btn) btn.textContent = "⏳ preparando…";
  currentAudio.onplaying = () => { if (btn) btn.textContent = "⏸ Parar"; };
  currentAudio.onended = () => { if (btn) btn.textContent = "🔊 Léemelo"; currentAudio = null; };
  currentAudio.onerror = () => { if (btn) btn.textContent = "🔊 Léemelo"; currentAudio = null; };
  currentAudio.play().catch(e => {
    stopAudio();
    if (btn) btn.textContent = "🔊 Léemelo";
    alert("No se pudo leer en voz alta: " + (e && e.message ? e.message : e));
  });
}

function profileFromForm() {
  const likes = document.getElementById("f-likes").value.split(",").map(s => s.trim()).filter(Boolean);
  const events = document.getElementById("f-events").value.trim();
  return {
    name: document.getElementById("f-name").value.trim() || "Dominik",
    age: parseFloat(document.getElementById("f-age").value) || 6,
    likes,
    temperament: document.getElementById("f-temp").value.trim(),
    recent_events: events ? [events] : [],
    story_theme: document.getElementById("f-theme").value.trim(),
  };
}

function showLoading(msg) {
  showScreen("screen-reader");
  document.getElementById("reader").innerHTML =
    '<div class="loading"><div class="rocket">🚀</div><p>' + esc(msg || "Creando la aventura…") +
    '</p><p style="opacity:.6;font-size:14px">(unos segundos)</p></div>';
}

function pagesHtml(pages) {
  let html = "";
  (pages || []).forEach(page => {
    const emoji = ILLUS[illusIdx++ % ILLUS.length];
    const illus = page.image
      ? '<img class="illus-img" src="' + page.image + '" alt="">'
      : '<span>' + emoji + '</span><span class="tag">ilustración…</span>';
    html += '<section class="page"><div class="illus">' + illus + "</div>" +
      '<p class="story-text">' + esc(page.text) + "</p></section>";
  });
  return html;
}

// Renderiza UN tramo (escena). data = {segment, dilemma, done?}
function renderStep(data) {
  const seg = data.segment;
  const dilemma = data.dilemma;
  const ending = seg.is_ending || data.done;

  // acumula las páginas mostradas para la continuidad
  (seg.pages || []).forEach(p => storySoFar.push(p.text));

  // prepara la narración de esta escena y detiene cualquier audio anterior
  stopAudio();
  currentSceneText = (seg.pages || []).map(p => p.text).join("  ");

  let html = "";
  if (!ending) html += '<div class="progress">Decisión ' + (choicesMade + 1) + " de " + total + "</div>";
  html += '<button class="btn read" id="read-btn" onclick="readScene()">🔊 Léemelo</button>';
  html += pagesHtml(seg.pages);

  if (!ending && dilemma) {
    html += '<div class="page"><div class="dilemma"><p class="prompt">' + esc(dilemma.prompt) + "</p>";
    html += '<div class="options">';
    (dilemma.options || []).forEach((opt, j) => {
      const color = OPT_COLORS[j % OPT_COLORS.length];
      html += '<button class="opt opt-' + color + '" data-dim="' + esc(dilemma.primary_dimension) + '" ' +
        'data-pole="' + esc(opt.pole) + '" data-txt="' + esc(opt.text) + '" onclick="choose(this)">' +
        '<span class="bul">' + esc(opt.id) + "</span><span>" + esc(opt.text) + "</span>" +
        '<span class="pole-tag">' + esc(opt.pole) + "</span></button>";
    });
    html += "</div></div></div>";
  } else {
    html += '<div class="page" style="text-align:center"><p class="prompt">🌟 ¡Fin! 🌟</p>' +
      '<button class="btn primary" onclick="backToCreate()">Crear otro cuento ✨</button></div>';
  }

  document.getElementById("reader").innerHTML = html;
  showScreen("screen-reader");
  window.scrollTo(0, 0);
}

async function createStory() {
  document.getElementById("create-err").textContent = "";
  profile = profileFromForm();
  storySoFar = []; choicesMade = 0; illusIdx = 0;
  document.getElementById("devlog-body").innerHTML = "";
  document.getElementById("subtitle").textContent = "Tu aventura";
  showLoading("Creando la aventura…");
  try {
    const res = await fetch("/api/story/start", {
      method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(profile),
    });
    if (!res.ok) throw new Error(await errMsg(res));
    const data = await res.json();
    total = data.total || 2;
    renderStep(data);
  } catch (e) {
    backToCreate();
    document.getElementById("create-err").textContent = "Ups, no se pudo crear el cuento: " + e.message;
  }
}

async function choose(btn) {
  const group = btn.closest(".options");
  group.querySelectorAll(".opt").forEach(b => b.classList.remove("sel"));
  btn.classList.add("sel");

  const rec = { dimension: btn.dataset.dim, pole: btn.dataset.pole, text: btn.dataset.txt };
  const line = document.createElement("div");
  line.textContent = "→ [" + rec.dimension + '] eligió: "' + rec.text + '"  ⇒  polo=' + rec.pole;
  document.getElementById("devlog-body").appendChild(line);

  choicesMade += 1;
  showLoading("La historia cambia según tu elección…");
  try {
    const res = await fetch("/api/story/next", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile, story_so_far: storySoFar, choice: rec.text, choices_made: choicesMade }),
    });
    if (!res.ok) throw new Error(await errMsg(res));
    renderStep(await res.json());
  } catch (e) {
    document.getElementById("reader").innerHTML = '<div class="err">No se pudo continuar: ' + esc(e.message) + "</div>";
  }
}

// "Ver ejemplo": preview de estilo NO interactivo (cuento completo de fixture).
async function loadSample() {
  showLoading("Cargando ejemplo…");
  illusIdx = 0;
  try {
    const res = await fetch("/api/storybook/sample");
    const data = await res.json();
    const byPage = {}; (data.dilemmas || []).forEach(d => { byPage[d.page] = d; });
    document.getElementById("subtitle").textContent = (data.story.title || "") + " (ejemplo)";
    let html = "";
    (data.story.pages || []).forEach(page => {
      html += pagesHtml([page]);
      const d = page.is_checkpoint ? byPage[page.page] : null;
      if (d) {
        html += '<div class="page"><div class="dilemma"><p class="prompt">' + esc(d.prompt) + '</p><div class="options">';
        (d.options || []).forEach((opt, j) => {
          html += '<button class="opt opt-' + OPT_COLORS[j % OPT_COLORS.length] + '" data-pole="' + esc(opt.pole) +
            '" onclick="this.closest(\'.options\').querySelectorAll(\'.opt\').forEach(b=>b.classList.remove(\'sel\'));this.classList.add(\'sel\')">' +
            '<span class="bul">' + esc(opt.id) + "</span><span>" + esc(opt.text) + "</span>" +
            '<span class="pole-tag">' + esc(opt.pole) + "</span></button>";
        });
        html += "</div></div></div>";
      }
    });
    document.getElementById("reader").innerHTML = html;
    showScreen("screen-reader"); window.scrollTo(0, 0);
  } catch (e) {
    backToCreate();
    document.getElementById("create-err").textContent = "No se pudo cargar el ejemplo: " + e.message;
  }
}
