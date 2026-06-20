// Interfaz Dominikito — cuento interactivo escena a escena (ramificado por las decisiones).

const ILLUS = ["🐵", "🛸", "⭐", "🌙", "☁️", "🍌"];
const OPT_COLORS = ["blue", "orange", "green", "purple", "red"];

let profile = null;
let storySoFar = [];   // textos de todas las páginas mostradas
let choicesMade = 0;
let total = 2;
let illusIdx = 0;
let currentAudio = null;     // Audio en reproducción (ElevenLabs)
let highlightUpdateId = null; // ID para requestAnimationFrame del resaltado
let childId = null;          // id del niño (BD)
let storyId = null;          // id del cuento (BD)
let currentDilemma = null;   // dilema de la escena actual (para guardar la decisión)
let sceneShownAt = 0;        // timestamp para response_latency_ms
let dashPin = "";            // PIN del dashboard (sesión)

// Variables para paginación (formato libro)
let bookPages = [];          // Lista de páginas en el libro actual
let currentPageIndex = 0;    // Índice de la página actualmente mostrada en el libro
let pageTransitioning = false; // Flag para evitar clicks múltiples durante la transición

function esc(s) { const d = document.createElement("div"); d.textContent = s == null ? "" : String(s); return d.innerHTML; }
async function errMsg(res) { try { const j = await res.json(); return j.detail || ("HTTP " + res.status); } catch (_) { return "HTTP " + res.status; } }
function showScreen(id) { document.querySelectorAll(".screen").forEach(s => s.classList.remove("active")); document.getElementById(id).classList.add("active"); }
function toggleDev() { document.body.classList.toggle("dev"); }
function backToCreate() { stopAudio(); showScreen("screen-create"); document.getElementById("subtitle").textContent = "Cuentos que escuchan a tu peque"; }

function stopHighlightLoop() {
  if (highlightUpdateId) {
    cancelAnimationFrame(highlightUpdateId);
    highlightUpdateId = null;
  }
}

function startHighlightLoopForPage(words, pageIdx) {
  stopHighlightLoop();
  function update() {
    if (!currentAudio || currentAudio.paused) return;
    const time = currentAudio.currentTime;
    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      const el = document.getElementById(`p${pageIdx}-word-${i}`);
      if (el) {
        if (time >= w.start && time <= w.end) {
          el.classList.add("highlight");
        } else {
          el.classList.remove("highlight");
        }
      }
    }
    highlightUpdateId = requestAnimationFrame(update);
  }
  highlightUpdateId = requestAnimationFrame(update);
}

function stopAudio() {
  if (currentAudio) { try { currentAudio.pause(); } catch (_) {} currentAudio = null; }
  stopHighlightLoop();
  document.querySelectorAll(".word-span").forEach(el => el.classList.remove("highlight"));
}

function playCurrentPageAudio() {
  const page = bookPages[currentPageIndex];
  const btn = document.getElementById("read-btn");
  if (!page || page.type !== "story") {
    if (btn) btn.style.display = "none";
    stopAudio();
    return;
  }
  
  if (btn) {
    btn.style.display = "inline-block";
    btn.textContent = "⏳ preparando…";
  }
  
  stopAudio();
  
  const textToRead = page.text;
  currentAudio = new Audio("/api/tts?text=" + encodeURIComponent(textToRead));
  
  let wordsTimestamps = [];
  fetch("/api/tts/timestamps?text=" + encodeURIComponent(textToRead))
    .then(res => res.ok ? res.json() : null)
    .then(data => {
      if (data && data.words) {
        wordsTimestamps = data.words;
        if (currentAudio && !currentAudio.paused) {
          startHighlightLoopForPage(wordsTimestamps, currentPageIndex);
        }
      }
    })
    .catch(err => console.error("Error al obtener timestamps:", err));
    
  currentAudio.onplaying = () => {
    if (btn) btn.textContent = "⏸ Parar";
    if (wordsTimestamps && wordsTimestamps.length > 0) {
      startHighlightLoopForPage(wordsTimestamps, currentPageIndex);
    }
  };
  
  currentAudio.onended = () => {
    if (btn) btn.textContent = "🔊 Léemelo";
    stopAudio();
    
    // Auto-advance to next page after a brief pause
    setTimeout(() => {
      if (currentPageIndex < bookPages.length - 1) {
        nextPage(true);
      }
    }, 1200);
  };
  
  currentAudio.onerror = () => {
    if (btn) btn.textContent = "🔊 Léemelo";
    stopAudio();
  };
  
  currentAudio.play().catch(e => {
    stopAudio();
    if (btn) btn.textContent = "🔊 Léemelo";
    console.log("Autoplay blocked or audio error:", e);
  });
}

function togglePlayPause() {
  const btn = document.getElementById("read-btn");
  if (currentAudio && !currentAudio.paused) {
    stopAudio();
    if (btn) btn.textContent = "🔊 Léemelo";
  } else {
    playCurrentPageAudio();
  }
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

function wrapTextInSpans(text, startWordIdx, pageIdx) {
  let currentIdx = startWordIdx;
  const words = text.trim().split(/\s+/);
  const html = words.map(w => {
    const span = `<span class="word-span" id="p${pageIdx}-word-${currentIdx}">${esc(w)}</span>`;
    currentIdx++;
    return span;
  }).join(" ");
  return { html, nextIdx: currentIdx };
}

function renderBook() {
  let html = '<div id="book-container">';
  
  bookPages.forEach((page, idx) => {
    const activeClass = idx === currentPageIndex ? "active" : "";
    
    if (page.type === "story") {
      const emoji = ILLUS[illusIdx++ % ILLUS.length];
      const illus = page.image
        ? '<img class="illus-img" src="' + page.image + '" alt="">'
        : '<span>' + emoji + '</span><span class="tag">ilustración…</span>';
      
      const wrap = wrapTextInSpans(page.text, 0, idx);
      
      html += `
        <div class="book-page page ${activeClass}" id="page-${idx}">
          <div class="illus">${illus}</div>
          <p class="story-text">${wrap.html}</p>
        </div>
      `;
    } else if (page.type === "dilemma") {
      const d = page.dilemma;
      let dilemmaHtml = `
        <div class="book-page page ${activeClass}" id="page-${idx}">
          <div class="dilemma">
            <p class="prompt">${esc(d.prompt)}</p>
            <div class="options">
      `;
      (d.options || []).forEach((opt, j) => {
        const color = OPT_COLORS[j % OPT_COLORS.length];
        const isSample = !childId;
        const clickHandler = isSample ? `selectSampleOption(this)` : `choose(this)`;
        
        dilemmaHtml += `
          <button class="opt opt-${color}" data-dim="${esc(d.primary_dimension)}" 
            data-id="${esc(opt.id)}" data-pole="${esc(opt.pole)}" data-txt="${esc(opt.text)}" 
            onclick="${clickHandler}">
            <span class="bul">${esc(opt.id)}</span>
            <span>${esc(opt.text)}</span>
            <span class="pole-tag">${esc(opt.pole)}</span>
          </button>
        `;
      });
      dilemmaHtml += `
            </div>
          </div>
        </div>
      `;
      html += dilemmaHtml;
    } else if (page.type === "ending") {
      html += `
        <div class="book-page page ${activeClass}" id="page-${idx}" style="text-align:center">
          <p class="prompt">🌟 ¡Fin! 🌟</p>
          <button class="btn primary" onclick="backToCreate()">Crear otro cuento ✨</button>
        </div>
      `;
    }
  });
  
  html += '</div>'; // cierra book-container
  
  // Agregar barra de navegación
  html += `
    <div class="book-nav">
      <button class="btn nav-btn" id="prev-btn" onclick="prevPage()">⬅️ Ant.</button>
      <button class="btn read" id="read-btn" onclick="togglePlayPause()">🔊 Léemelo</button>
      <div class="page-indicator" id="page-indicator">Página 1 de 1</div>
      <button class="btn nav-btn" id="next-btn" onclick="nextPage()">Sig. ➡️</button>
    </div>
  `;
  
  return html;
}

function updateNavButtons() {
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const indicator = document.getElementById("page-indicator");
  const readBtn = document.getElementById("read-btn");
  
  if (!prevBtn || !nextBtn || !indicator) return;
  
  const pageCount = bookPages.length;
  indicator.textContent = `Página ${currentPageIndex + 1} de ${pageCount}`;
  
  prevBtn.disabled = currentPageIndex === 0;
  
  const currentPage = bookPages[currentPageIndex];
  
  if (currentPage.type === "story") {
    if (readBtn) {
      readBtn.style.display = "inline-block";
      if (currentAudio && !currentAudio.paused) {
        readBtn.textContent = "⏸ Parar";
      } else {
        readBtn.textContent = "🔊 Léemelo";
      }
    }
    nextBtn.style.display = "inline-block";
    nextBtn.disabled = false;
  } else if (currentPage.type === "dilemma") {
    if (readBtn) readBtn.style.display = "none";
    
    const isSample = !childId;
    if (isSample) {
      nextBtn.style.display = "inline-block";
      nextBtn.disabled = false;
    } else {
      nextBtn.style.display = "none";
    }
  } else if (currentPage.type === "ending") {
    if (readBtn) readBtn.style.display = "none";
    nextBtn.style.display = "none";
  }
}

function goToPage(idx, autoPlay = true) {
  if (idx < 0 || idx >= bookPages.length || pageTransitioning) return;
  
  pageTransitioning = true;
  stopAudio();
  
  const oldPageEl = document.getElementById(`page-${currentPageIndex}`);
  const newPageEl = document.getElementById(`page-${idx}`);
  
  if (oldPageEl && newPageEl) {
    oldPageEl.classList.add("fade-out");
    
    setTimeout(() => {
      oldPageEl.classList.remove("active", "fade-out");
      currentPageIndex = idx;
      newPageEl.classList.add("active");
      
      updateNavButtons();
      pageTransitioning = false;
      
      if (bookPages[currentPageIndex].type === "story" && autoPlay) {
        playCurrentPageAudio();
      } else {
        const btn = document.getElementById("read-btn");
        if (btn) btn.style.display = "none";
      }
    }, 400); // 400ms para coincidir con la transición CSS (0.4s)
  } else {
    currentPageIndex = idx;
    const reader = document.getElementById("reader");
    const progressHtml = renderProgressHtml();
    reader.innerHTML = progressHtml + renderBook();
    updateNavButtons();
    pageTransitioning = false;
    if (bookPages[currentPageIndex].type === "story" && autoPlay) {
      playCurrentPageAudio();
    }
  }
}

function nextPage(isAuto = false) {
  if (currentPageIndex < bookPages.length - 1) {
    goToPage(currentPageIndex + 1, true);
  }
}

function prevPage() {
  if (currentPageIndex > 0) {
    goToPage(currentPageIndex - 1, true);
  }
}

function renderProgressHtml() {
  const ending = bookPages.length > 0 && bookPages[bookPages.length - 1].type === "ending";
  if (!ending && childId) {
    return '<div class="progress">Decisión ' + (choicesMade + 1) + " de " + total + "</div>";
  }
  return "";
}

// Renderiza UN tramo (escena). data = {segment, dilemma, done?}
function renderStep(data) {
  const seg = data.segment;
  const dilemma = data.dilemma;
  const ending = seg.is_ending || data.done;

  // acumula las páginas mostradas para la continuidad
  (seg.pages || []).forEach(p => storySoFar.push(p.text));

  currentDilemma = dilemma;   // para guardar la decisión (Contrato B)
  sceneShownAt = Date.now();

  bookPages = [];
  (seg.pages || []).forEach(p => {
    bookPages.push({
      type: "story",
      text: p.text,
      image: p.image,
      isCheckpoint: p.is_checkpoint,
      pageNumber: p.page
    });
  });

  if (!ending && dilemma) {
    bookPages.push({
      type: "dilemma",
      dilemma: dilemma
    });
  } else if (ending) {
    bookPages.push({
      type: "ending"
    });
  }

  currentPageIndex = 0;
  
  const progressHtml = renderProgressHtml();
  document.getElementById("reader").innerHTML = progressHtml + renderBook();
  
  showScreen("screen-reader");
  window.scrollTo(0, 0);
  
  // Reproducir el audio de la primera página del tramo
  playCurrentPageAudio();
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
    childId = data.child_id || null;
    storyId = data.story_id || null;
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

  // guarda la decisión (lookup del polo pre-registrado) — no bloquea la historia
  if (currentDilemma) {
    fetch("/api/decision", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({
        child_id: childId, story_id: storyId,
        dilemma_id: currentDilemma.dilemma_id, page: currentDilemma.page,
        dimension: currentDilemma.primary_dimension, subaxis: currentDilemma.subaxis,
        pole: rec.pole, chosen_option_id: btn.dataset.id,
        age_at_decision: profile ? profile.age : null,
        developmental_stage: currentDilemma.developmental_stage,
        response_latency_ms: sceneShownAt ? (Date.now() - sceneShownAt) : null,
      }),
    }).catch(() => {});
  }

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

function selectSampleOption(btn) {
  const optionsDiv = btn.closest('.options');
  optionsDiv.querySelectorAll('.opt').forEach(b => b.classList.remove('sel'));
  btn.classList.add('sel');
}

// "Ver ejemplo": preview de estilo NO interactivo (cuento completo de fixture).
async function loadSample() {
  showLoading("Cargando ejemplo…");
  illusIdx = 0;
  childId = null;
  storyId = null;
  choicesMade = 0;
  try {
    const res = await fetch("/api/storybook/sample");
    const data = await res.json();
    const byPage = {}; (data.dilemmas || []).forEach(d => { byPage[d.page] = d; });
    document.getElementById("subtitle").textContent = (data.story.title || "") + " (ejemplo)";
    
    bookPages = [];
    (data.story.pages || []).forEach((page) => {
      bookPages.push({
        type: "story",
        text: page.text,
        image: page.image,
        isCheckpoint: page.is_checkpoint,
        pageNumber: page.page
      });
      const d = page.is_checkpoint ? byPage[page.page] : null;
      if (d) {
        bookPages.push({
          type: "dilemma",
          dilemma: d
        });
      }
    });
    bookPages.push({
      type: "ending"
    });
    
    currentPageIndex = 0;
    
    const progressHtml = renderProgressHtml();
    document.getElementById("reader").innerHTML = progressHtml + renderBook();
    showScreen("screen-reader"); 
    window.scrollTo(0, 0);
    
    // Autoplay the first page
    playCurrentPageAudio();
  } catch (e) {
    backToCreate();
    document.getElementById("create-err").textContent = "No se pudo cargar el ejemplo: " + e.message;
  }
}

// ---------- Dashboard de padres (protegido con PIN) ----------
const POLE_BAR_COLORS = ["var(--purple)", "var(--orange)", "var(--green)", "var(--pink)", "var(--yellow)"];
const ALERT = { watch: ["⚠️ vale la pena observar", "#FFE9C2"], elevated: ["🔔 conviene prestar atención", "#FFD1DE"] };

let activeDashboardTab = "trends"; // "trends" | "evolution" | "validity" | "privacy"
let lastDashboardData = null;      // datos cacheados para redibujo instantáneo

function showDashboardLogin() {
  stopAudio();
  activeDashboardTab = "trends";
  lastDashboardData = null;
  showScreen("screen-dashboard");
  document.getElementById("dash-login").style.display = "block";
  document.getElementById("dash-content").style.display = "none";
  document.getElementById("dash-err").textContent = "";
  document.getElementById("subtitle").textContent = "Dashboard de papás";
}

async function dashLogin() {
  const pin = document.getElementById("dash-pin").value.trim();
  const err = document.getElementById("dash-err");
  err.textContent = "";
  try {
    const res = await fetch("/api/children?pin=" + encodeURIComponent(pin));
    if (!res.ok) throw new Error(await errMsg(res));
    dashPin = pin;
    const kids = (await res.json()).children || [];
    if (!kids.length) { err.textContent = "Aún no hay datos. Crea algunos cuentos primero."; return; }
    document.getElementById("dash-child").innerHTML =
      kids.map(k => '<option value="' + k.id + '">' + esc(k.name) + " (" + k.age + " años)</option>").join("");
    document.getElementById("dash-login").style.display = "none";
    document.getElementById("dash-content").style.display = "block";
    loadChildDashboard(kids[0].id);
  } catch (e) {
    err.textContent = "No se pudo entrar: " + (e.message || e);
  }
}

async function loadChildDashboard(cid) {
  const box = document.getElementById("dash-trends");
  box.innerHTML = '<div class="loading"><div class="rocket">🛸</div></div>';
  try {
    const res = await fetch("/api/dashboard?child_id=" + encodeURIComponent(cid) + "&pin=" + encodeURIComponent(dashPin));
    if (!res.ok) throw new Error(await errMsg(res));
    lastDashboardData = await res.json();
    renderDashboard(lastDashboardData);
  } catch (e) {
    box.innerHTML = '<div class="err">' + esc(e.message || e) + "</div>";
  }
}

window.switchDashboardTab = function(tab) {
  activeDashboardTab = tab;
  if (lastDashboardData) {
    renderDashboard(lastDashboardData);
  }
};

function renderDashboard(data) {
  const dims = data.dimensions || [];
  if (!dims.length) {
    document.getElementById("dash-trends").innerHTML =
      '<div class="card">Aún no hay decisiones registradas para este niño/a.</div>';
    return;
  }

  // Cuenta alertas para el panel de resumen
  let watchCount = 0;
  let elevatedCount = 0;
  let totalDecisions = 0;
  dims.forEach(d => {
    totalDecisions += d.sample_size || 0;
    if (d.meets_min_threshold) {
      if (d.alert_level === "watch") watchCount++;
      if (d.alert_level === "elevated") elevatedCount++;
    }
  });

  // Generación de la barra de pestañas (Tabs Navigation)
  let html = `
    <div class="dash-tabs">
      <button class="dash-tab-btn ${activeDashboardTab === 'trends' ? 'active' : ''}" onclick="switchDashboardTab('trends')">📊 Tendencias</button>
      <button class="dash-tab-btn ${activeDashboardTab === 'evolution' ? 'active' : ''}" onclick="switchDashboardTab('evolution')">🎓 Perfil Evolutivo</button>
      <button class="dash-tab-btn ${activeDashboardTab === 'validity' ? 'active' : ''}" onclick="switchDashboardTab('validity')">⚖️ Rúbrica de Validez</button>
      <button class="dash-tab-btn ${activeDashboardTab === 'privacy' ? 'active' : ''}" onclick="switchDashboardTab('privacy')">🛡️ Seguridad & Ética</button>
    </div>
  `;

  if (activeDashboardTab === "trends") {
    // ---- PESTAÑA 1: TENDENCIAS CONDUCTUALES (EL GRID) ----
    const DIM_METADATA = {
      regulacion_emocional: {
        icon: "🌊",
        anchor: "CASEL · Self-Management · Erikson",
        desc: "Mide cómo el niño/a modula sus respuestas ante la frustración o el miedo en el cuento.",
      },
      confianza_apego: {
        icon: "🤝",
        anchor: "Bowlby (Apego) · CASEL Relationship",
        desc: "Refleja la tendencia a buscar vínculos seguros y pedir ayuda frente a retos y extraños.",
      },
      honestidad: {
        icon: "💎",
        anchor: "CASEL · Decisión Responsable · Ma (Moral)",
        desc: "Muestra la transparencia y asunción de errores cuando evitar o callar es más fácil.",
      },
      empatia: {
        icon: "💗",
        anchor: "CASEL · Conciencia Social · Ma Altruismo",
        desc: "Evalúa comportamientos de ayuda activa vs. indiferencia pasiva o reactividad en conflictos.",
      },
      autonomia: {
        icon: "🧭",
        anchor: "Erikson · Autonomía / Iniciativa",
        desc: "Mide la iniciativa para decidir por sí mismo frente a la búsqueda excesiva de guía del adulto.",
      },
      riesgo_cautela: {
        icon: "🚀",
        anchor: "Erikson · Iniciativa vs. Culpa (Secundario)",
        desc: "Analiza el balance entre explorar lo desconocido y quedarse en la zona segura.",
      }
    };

    const POLE_LABELS = {
      regulado: "Autorregulado 🧘‍♂️",
      desregulado: "Intenso / Reactivo ⚡",
      busca_vinculo: "Busca Apoyo / Vínculo 🤝",
      evita_desconfia: "Resuelve Solo / Evitativo 🛡️",
      asume_transparente: "Honesto / Transparente 💎",
      evade_oculta: "Evasivo / Oculta 😶",
      prosocial_asertivo: "Prosocial / Colaborador 💗",
      pasivo_evitativo: "Pasivo / Observador 💤",
      reactivo_agresivo: "Reactivo / Hostil 😡",
      autonomo: "Autónomo / Decidido 🧭",
      dependiente: "Dependiente / Busca Guía 🧑‍🤝‍🧑",
      explorador: "Explorador / Curioso 🚀",
      cauto: "Prudente / Cauto 🐾"
    };

    const ALERT_BADGES = {
      watch: '<span class="alert-tag watch-tag"><span class="dot"></span>Atención Recomendada</span>',
      elevated: '<span class="alert-tag elevated-tag"><span class="dot pulse"></span>Patrón Persistente</span>'
    };

    html += `
      <div class="dash-overview">
        <div class="overview-item card shadow-sm">
          <div class="label">Banda Evolutiva</div>
          <div class="val">${esc(data.age_band || "3-10")} años</div>
          <div class="sub">Clasificación Ma Stage / Erikson</div>
        </div>
        <div class="overview-item card shadow-sm">
          <div class="label">Muestras Totales</div>
          <div class="val">${totalDecisions}</div>
          <div class="sub">Decisiones registradas</div>
        </div>
        <div class="overview-item card shadow-sm">
          <div class="label">Observaciones Activas</div>
          <div class="val">
            ${elevatedCount > 0 ? `<span class="badge badge-red">${elevatedCount} Elevada</span>` : ""}
            ${watchCount > 0 ? `<span class="badge badge-orange">${watchCount} Atención</span>` : ""}
            ${watchCount === 0 && elevatedCount === 0 ? '<span class="badge badge-green">Estable</span>' : ""}
          </div>
          <div class="sub">Señales fuera del promedio</div>
        </div>
      </div>
      
      <div class="dash-grid">
    `;

    dims.forEach(d => {
      const meta = DIM_METADATA[d.dimension] || { icon: "📊", anchor: "CASEL Framework", desc: "" };
      const alertClass = d.alert_level !== "none" && d.meets_min_threshold ? `card-alert-${d.alert_level}` : "";
      
      html += `
        <div class="card dash-card ${alertClass} ${!d.meets_min_threshold ? 'dash-card-pending' : ''}">
          <div class="dash-card-header">
            <span class="dash-card-icon">${meta.icon}</span>
            <div class="dash-card-title-box">
              <h3>${esc(d.label)}</h3>
              <span class="anchor-ref">${esc(meta.anchor)}</span>
            </div>
            <span class="dash-n">${d.sample_size} dec.</span>
          </div>
          
          <div class="dash-card-body">
      `;

      if (!d.meets_min_threshold) {
        html += `
          <div class="pending-box">
            <div class="pending-icon">🌱</div>
            <h4>Sembrando datos...</h4>
            <p>Aún no hay suficientes decisiones registradas para trazar un patrón sólido. Sigue jugando cuentos con tu peque.</p>
            <div class="pending-progress-bar">
              <div class="pending-progress-fill" style="width: ${(d.sample_size / 5 * 100)}%"></div>
            </div>
            <span class="pending-ratio">${d.sample_size} / 5 decisiones</span>
          </div>
        `;
      } else {
        const totalN = d.sample_size || 1;
        
        html += '<div class="distribution-bar">';
        Object.keys(d.distribution).forEach((p, i) => {
          const c = d.distribution[p];
          if (!c) return;
          const w = (100 * c / totalN).toFixed(1);
          html += `<span class="dist-seg" style="width:${w}%;background:${POLE_BAR_COLORS[i % POLE_BAR_COLORS.length]}" title="${esc(p)}: ${c}"></span>`;
        });
        html += '</div>';

        html += '<div class="dist-legend">';
        Object.keys(d.distribution).forEach((p, i) => {
          const c = d.distribution[p];
          const w = (100 * c / totalN).toFixed(0);
          const color = POLE_BAR_COLORS[i % POLE_BAR_COLORS.length];
          const pLabel = POLE_LABELS[p] || p;
          html += `
            <div class="legend-item" style="opacity: ${c > 0 ? 1 : 0.4}">
              <span class="legend-color-dot" style="background:${color}"></span>
              <span class="legend-label">${esc(pLabel)}</span>
              <span class="legend-val">${c} (${w}%)</span>
            </div>
          `;
        });
        html += '</div>';

        html += `
          <div class="summary-box">
            <p class="dash-sum">« ${esc(d.neutral_summary)} »</p>
          </div>
        `;

        if (d.alert_level !== "none") {
          html += `
            <div class="alert-badge-container">
              ${ALERT_BADGES[d.alert_level] || ""}
            </div>
          `;
        }
      }

      html += `
          </div> <!-- fin body -->
          <div class="dash-card-footer">
            <button class="btn-toggle-science" onclick="toggleScience(this)">
              <span>🔍 Fundamento Científico</span> <span class="arrow">▼</span>
            </button>
            <div class="science-detail-box" style="display:none">
              <p>${esc(meta.desc)}</p>
              <small>Basado en el marco teórico de <b>${esc(meta.anchor)}</b>.</small>
            </div>
          </div>
        </div> <!-- fin card -->
      `;
    });

    html += '</div>'; // fin dash-grid

    // Directorio de derivación clínica si hay alertas
    if (watchCount > 0 || elevatedCount > 0) {
      html += `
        <div class="card clinical-handoff shadow-sm">
          <div class="handoff-header">
            <span class="handoff-icon">🩺</span>
            <div>
              <h3>Guía de Acompañamiento Profesional</h3>
              <p class="hint">Recomendaciones éticas y canales de consulta autorizados</p>
            </div>
          </div>
          <div class="handoff-body">
            <p>
              Dominikito es una herramienta lúdica diseñada para observar patrones de conducta y fomentar la comunicación familiar. 
              <b>Bajo ninguna circunstancia sustituye un diagnóstico clínico.</b>
            </p>
            <div class="clinical-tabs">
              <div class="clinical-tab">
                <h5>🧠 Cuándo Consultar</h5>
                <p>Considera conversar con un profesional si observas que las conductas mostradas interfieren con el desarrollo social, escolar o familiar de tu peque de forma persistente.</p>
              </div>
              <div class="clinical-tab">
                <h5>📞 Directorios Sugeridos</h5>
                <ul>
                  <li><b>Psicopedagogía y Apoyo Escolar:</b> Consulta con el orientador de su escuela.</li>
                  <li><b>Asociación de Psicología Infantil:</b> Directorios certificados en tu país.</li>
                  <li><b>Línea de Acompañamiento:</b> Orientación pediátrica primaria de tu localidad.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      `;
    }

  } else if (activeDashboardTab === "evolution") {
    // ---- PESTAÑA 2: PERFIL EVOLUTIVO (MA & ERIKSON) ----
    let stageTitle = "";
    let stageSubtitle = "";
    let stageDesc = "";
    let stageNorms = [];
    let eriksonStage = "";
    let eriksonDesc = "";
    
    if (data.age_band === "3-6") {
      stageTitle = "Estadio 1 de Ma (3-6 años) — Egocentrismo y Supervivencia";
      stageSubtitle = "Foco moral primario: Egocentrismo funcional y obediencia pragmática.";
      stageDesc = "A esta edad, las decisiones del niño están orientadas a la autoprotección y la satisfacción de necesidades inmediatas. El egocentrismo es evolutivamente normal y no constituye una falta de empatía o egoísmo clínico, sino la consolidación de su supervivencia básica.";
      stageNorms = [
        "Egocentrismo normativo: prioriza sus deseos y pertenencias ante extraños o amigos.",
        "Obediencia instrumental: sigue reglas principalmente para evitar castigos físicos o regaños.",
        "Comprensión concreta: percibe situaciones morales basadas únicamente en el resultado físico directo."
      ];
      eriksonStage = "Iniciativa vs. Culpa (Estadio Psicosocial de 3 a 6 años)";
      eriksonDesc = "El niño explota su creatividad, ensaya roles en mundos de fantasía y experimenta con límites. La toma de riesgos lúdicos es normal y fomenta la confianza en sí mismo.";
    } else if (data.age_band === "6-9") {
      stageTitle = "Estadio 2 de Ma (6-9 años) — Altruismo Recíproco";
      stageSubtitle = "Foco moral primario: Intercambio mutuo y conexión afectiva.";
      stageDesc = "El desarrollo moral de tu peque se encuentra en la etapa del altruismo recíproco ('te ayudo si me ayudas'). Sus acciones prosociales y de honestidad están fuertemente motivadas por la reciprocidad concreta y el afecto interpersonal cercano.";
      stageNorms = [
        "Reciprocidad pragmática: colabora activamente si percibe un intercambio justo o aprobación mutua.",
        "Apego relacional: busca validar sus elecciones bajo la mirada afectiva de padres y maestros.",
        "Empatía selectiva: mayor tendencia a socorrer a personajes cercanos, familiares o mascotas."
      ];
      eriksonStage = "Laboriosidad vs. Inferioridad (Estadio Escolar de 6 a 12 años)";
      eriksonDesc = "Centrado en el desarrollo de habilidades sociales, aprendizaje de normas y orgullo derivado de la competencia escolar y social.";
    } else { // "9-12"
      stageTitle = "Estadio 3 de Ma (9-12 años) — Altruismo de Grupo Primario";
      stageSubtitle = "Foco moral primario: Pertenencia e interdependencia del grupo.";
      stageDesc = "El razonamiento del preadolescente integra dinámicas colectivas de grupo. El deseo de pertenencia, la justicia compartida y las expectativas de los pares definen su noción de honestidad, empatía y responsabilidad social.";
      stageNorms = [
        "Altruismo comunitario: actúa de forma empática para resguardar la cohesión y armonía de su círculo de pares.",
        "Comprensión avanzada: asume verdades y dilemas morales complejos con mayor capacidad de autoanálisis.",
        "Autorregulación grupal: modula comportamientos guiado por normas del colectivo aceptadas autónomamente."
      ];
      eriksonStage = "Laboriosidad vs. Inferioridad / Identidad vs. Confusión";
      eriksonDesc = "Comienza la transición hacia la exploración de la identidad social propia dentro del colectivo escolar y comunitario.";
    }

    html += `
      <div class="card evolution-card shadow-sm">
        <div class="evo-header">
          <span class="evo-icon">🎓</span>
          <div>
            <h3>Perfil de Desarrollo Evolutivo</h3>
            <p class="hint">Anclado a las investigaciones de Ma (2013) y los estadios de Erikson</p>
          </div>
        </div>
        
        <div class="evo-timeline">
          <div class="timeline-step ${data.age_band === '3-6' ? 'active' : ''}">
            <span class="step-num">3-6</span>
            <span class="step-lbl">Estadio 1</span>
          </div>
          <div class="timeline-step ${data.age_band === '6-9' ? 'active' : ''}">
            <span class="step-num">6-9</span>
            <span class="step-lbl">Estadio 2</span>
          </div>
          <div class="timeline-step ${data.age_band === '9-12' ? 'active' : ''}">
            <span class="step-num">9-12</span>
            <span class="step-lbl">Estadio 3</span>
          </div>
        </div>
        
        <div class="evo-body">
          <div class="evo-stage-badge">Banda evolutiva activa: ${esc(data.age_band || "3-10")} años</div>
          <h4>${esc(stageTitle)}</h4>
          <p class="stage-sub">${esc(stageSubtitle)}</p>
          <p class="stage-desc">${esc(stageDesc)}</p>
          
          <div class="evo-norms">
            <h5>📋 Conductas del Desarrollo Normativas</h5>
            <ul>
              ${stageNorms.map(n => `<li>${esc(n)}</li>`).join("")}
            </ul>
          </div>
          
          <div class="erikson-box">
            <h5>🧭 Estadio Psicosocial de Erikson</h5>
            <p class="erikson-title"><b>${esc(eriksonStage)}</b></p>
            <p class="erikson-desc">${esc(eriksonDesc)}</p>
          </div>
        </div>
      </div>
    `;

  } else if (activeDashboardTab === "validity") {
    // ---- PESTAÑA 3: RÚBRICA DE VALIDEZ (COOPER & SANTILLO) ----
    const hasEnoughData = totalDecisions >= 5;
    
    html += `
      <div class="card validity-card shadow-sm">
        <div class="validity-header">
          <span class="validity-icon">⚖️</span>
          <div>
            <h3>Rúbrica de Validez Científica</h3>
            <p class="hint">Evaluación de límites psicométricos según Cooper (2013) y la revisión Santillo (2025)</p>
          </div>
        </div>
        
        <div class="validity-gauge-container">
          <div class="gauge-item">
            <div class="gauge-status ${hasEnoughData ? 'status-green' : 'status-yellow'}">
              ${hasEnoughData ? '✓' : '⚠'}
            </div>
            <div class="gauge-label-box">
              <h5>Criterio de Persistencia Temporal</h5>
              <p>Evita falsos positivos por conductas transitorias o juegos de rol aislados.</p>
              <small>Estado: <b>${totalDecisions} / 5 decisiones</b> registradas totales.</small>
            </div>
          </div>
          
          <div class="gauge-item">
            <div class="gauge-status status-blue">ℹ</div>
            <div class="gauge-label-box">
              <h5>Exclusión de Deterioro Funcional (Impairment)</h5>
              <p>El juego en casa no mide distrés o incapacidad escolar. No se pueden inducir diagnósticos.</p>
              <small>Estado: <b>Inferencia Excluida de Diagnósticos Clínicos</b>.</small>
            </div>
          </div>
          
          <div class="gauge-item">
            <div class="gauge-status status-green">✓</div>
            <div class="gauge-label-box">
              <h5>Criterio de Normalización por Edad</h5>
              <p>Las métricas e interpretaciones se ajustan automáticamente a la banda evolutiva exacta.</p>
              <small>Estado: <b>Banda evolutiva activa para ${esc(data.age_band || "3-10")} años</b>.</small>
            </div>
          </div>
        </div>
        
        <div class="validity-citation">
          <h5>📖 Revisión PRISMA (Santillo et al., 2025 — MDPI Children)</h5>
          <blockquote>
            "Las técnicas proyectivas de construcción sirven como complementos eficaces de la evaluación clínica... no deben ser tratadas como herramientas de diagnóstico independientes."
          </blockquote>
          <p class="citation-note">
            ⚠️ <b>Aviso de validez digital:</b> Dominikito es un instrumento de <b>señalización y observación lúdica</b>. Dado que no existe validación clínica documentada de pruebas proyectivas digitales sin terapeuta presente, Dominikito adopta un tono humilde, descriptivo y enfocado puramente en la derivación activa a profesionales si persisten las dudas.
          </p>
        </div>
      </div>
    `;

  } else if (activeDashboardTab === "privacy") {
    // ---- PESTAÑA 4: SEGURIDAD Y ÉTICA (COPPA & GDPR) ----
    html += `
      <div class="card privacy-card shadow-sm">
        <div class="privacy-header">
          <span class="privacy-icon">🛡️</span>
          <div>
            <h3>Seguridad, Privacidad y Cumplimiento</h3>
            <p class="hint">Protocolos éticos de resguardo del menor y la familia</p>
          </div>
        </div>
        
        <div class="privacy-body">
          <p class="privacy-intro">
            Los datos afectivos y de decisiones de menores son clasificados como información de categoría especial de alta sensibilidad. Dominikito implementa las directivas de seguridad del marco legal ético:
          </p>
          
          <div class="check-list">
            <div class="check-item">
              <div class="check-box checked">✓</div>
              <div class="check-text">
                <b>Cumplimiento de Ley COPPA (FTC EE.UU.)</b>
                <p>Verificación del consentimiento parental e inicio protegido mediante PIN de padres antes del almacenamiento de cualquier registro de menores de 13 años.</p>
              </div>
            </div>
            
            <div class="check-item">
              <div class="check-box checked">✓</div>
              <div class="check-text">
                <b>Regulación GDPR (Categoría Especial)</b>
                <p>Cifrado y minimización en el almacenamiento de datos mentales y de comportamiento socioemocional, restringiendo el acceso del menor a la capa evaluativa.</p>
              </div>
            </div>
            
            <div class="check-item">
              <div class="check-box checked">✓</div>
              <div class="check-text">
                <b>Guardrail de Integridad (Anti-Sesgo de Confirmación)</b>
                <p>Separación estricta de motores: El Agente 1 genera la trama, el Agente 2 pre-registra el dilema (lookup sin interpretación libre posterior) y el dashboard acumula con fórmulas fijas. Ningún componente genera y se autocalifica circularmente.</p>
              </div>
            </div>
            
            <div class="check-item">
              <div class="check-box checked">✓</div>
              <div class="check-text">
                <b>Lista de Exclusión de Eventos Recientes</b>
                <p>Filtro proactivo de recuerdos de los padres. Evita forzar dilemas sobre duelos, mudanzas o separaciones, protegiendo al niño de la re-activación de traumas en juego.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  document.getElementById("dash-trends").innerHTML = html;
}

// Función global para expandir/colapsar
window.toggleScience = function(btn) {
  const card = btn.closest(".dash-card");
  const box = card.querySelector(".science-detail-box");
  const arrow = btn.querySelector(".arrow");
  if (box.style.display === "none") {
    box.style.display = "block";
    arrow.textContent = "▲";
    btn.classList.add("active");
  } else {
    box.style.display = "none";
    arrow.textContent = "▼";
    btn.classList.remove("active");
  }
};
