// S12.3: sohbet sayfası. Cevap Server-Sent Events ile akar.
// S12.11: kaynaklara ya da alıntıya dokununca metin Kaynaklar panelinde bağlamıyla açılır, cevap yanında kalır.
// S13.1: solda konuşmalar (geçmiş, "Yeni konuşma", en altta ayarlar), sağda Kaynaklar; ikisi de açılıp kapanır, dar
// ekranda çekmecedir. Konuşmalar hesapta saklanır (ayar açıksa; sunucu geçmişi kendisi okur). Ayar kapalıyken konuşma
// S12'deki gibi yalnız bu tarayıcıda (localStorage) durur ve her soruda önceki sorular ve cevaplar yeniden gönderilir.
// Açık konuşmanın kimliği adreste (#k/<kimlik>): sayfa yenilenince ve geri tuşunda aynı konuşma açılır.
// S13.2: panellerin genişliği aradaki çizgiyi sürükleyerek (ya da odaklanıp ok tuşlarıyla) ayarlanır; ayarlar
// sekmelidir (Hesap, Konuşmalar, Görünüm, Belgeler); görünüm (tema, cevapların yazı boyutu) ve genişlikler bu cihazda.
// S13.3: yeni konuşmada örnek sorular sayfanın yeteneklerinden seçilir; cevap beklenirken yapılan adımlar ("… okunuyor")
// dizilir, cevabın üstünde açılır bir özet olarak kalır.
"use strict";

const P = document.body.dataset.prefix;
const KEY = "sohbet:konusma";          // geçici konuşma (saklama kapalıyken)
const PANELS = "sohbet:paneller";      // geniş ekranda panellerin açık/kapalı tercihi
const WIDTHS = "sohbet:genislik";      // geniş ekranda panellerin genişliği
const LOOK = "sohbet:gorunum";         // tema ve yazı boyutu
const $ = (id) => document.getElementById(id);
const els = { list: $("konusma"), empty: $("bos"), form: $("soru-formu"), input: $("soru"), send: $("gonder"),
  fresh: $("yeni"), side: $("yan"), sideList: $("yan-liste"), sideText: $("yan-metin"), sideTitle: $("yan-baslik"),
  back: $("yan-geri"), close: $("yan-kapat"), open: $("yan-ac"), count: $("yan-sayi"), shade: $("perde"),
  dpath: $("metin-yol"), dsource: $("metin-kaynak"), dbody: $("metin-govde"),
  left: $("sol"), leftOpen: $("sol-ac"), leftClose: $("sol-kapat"), history: $("gecmis"), title: $("baslik"),
  quota: $("hak"), settings: $("ayarlar"), settingsOpen: $("ayarlar-ac"), settingsClose: $("ayarlar-kapat"),
  keep: $("sakla"), wipe: $("hepsini-sil"), wipeAsk: $("hepsini-sil-onay"), wipeYes: $("hepsini-sil-evet"),
  wipeNo: $("hepsini-sil-vazgec"), settingsError: $("ayar-hata") };
const SIDE_EMPTY = els.sideList.innerHTML;
const docked = { left: window.matchMedia("(min-width: 960px)"), right: window.matchMedia("(min-width: 1200px)") };

const state = { keep: true, questions: null, remaining: null, conversations: [] };
let cur = { id: null, title: "", turns: [] };    // açık konuşma; turda q, markdown, sources, corrected, feedback, n, a
let busy = false;

function loadLocal() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}
function saveLocal() {
  if (cur.id) return;                  // saklanan konuşma sunucuda
  try { localStorage.setItem(KEY, JSON.stringify(cur.turns)); } catch { /* dolu ya da kapalı: konuşma yalnız sayfada */ }
}

async function api(path, body) {
  const r = await fetch(`${P}api/${path}`, body === undefined ? { credentials: "same-origin" } : {
    method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body) });
  if (r.status === 401) { location.href = `${P}giris?next=${encodeURIComponent(P)}`; throw new Error("Oturum kapandı."); }
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || "İstek yerine getirilemedi.");
  return data;
}

// ------------------------------------------------------------ Markdown (küçük, yalnız cevabın kullandıkları)

function esc(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function inline(s, refs) {
  let t = esc(s);
  t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
  t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  t = t.replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
  t = t.replace(/\[\[[^\[\]\s]+\]\]/g, '<span class="isaret">◦</span>');        // akış sırasında: henüz numarasız
  if (refs) {
    t = t.replace(/\[(\d+)\]/g, (m, n) => {
      const src = refs.get(Number(n));
      if (!src) return m;
      const bad = src.problem ? " kotu" : "";
      return `<button type="button" class="ref${bad}" data-n="${n}" title="${esc(src.cite_as || "Adresi bulunamadı")}">[${num(src)}]</button>`;
    });
  }
  return t;
}

function markdown(text, refs) {
  const lines = text.replace(/\r/g, "").split("\n");
  const out = [];
  let i = 0;
  const para = [];
  const flush = () => {
    if (para.length) out.push(`<p dir="auto">${para.map((l) => inline(l, refs)).join("<br>")}</p>`);
    para.length = 0;
  };
  while (i < lines.length) {
    const line = lines[i];
    let m;
    if (!line.trim()) { flush(); i++; continue; }
    if ((m = line.match(/^(#{1,6})\s+(.*)$/))) {
      flush();
      const level = Math.min(4, m[1].length + 1);
      out.push(`<h${level} dir="auto">${inline(m[2], refs)}</h${level}>`);
      i++; continue;
    }
    if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) { flush(); out.push("<hr>"); i++; continue; }
    if (/^\s*>/.test(line)) {
      flush();
      const block = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) { block.push(lines[i].replace(/^\s*>\s?/, "")); i++; }
      // bloğun altındaki yalnız işaretli/numaralı satır bloğa katılır
      if (i < lines.length && /^\s*(\[\[[^\]]+\]\]|\[\d+\])(\s*(\[\[[^\]]+\]\]|\[\d+\]))*\s*$/.test(lines[i])) {
        block[block.length - 1] += " " + lines[i].trim(); i++;
      }
      out.push(`<blockquote>${markdown(block.join("\n"), refs)}</blockquote>`);
      continue;
    }
    if (/^\s*([-*+]|\d+[.)])\s+/.test(line)) {
      flush();
      const ordered = /^\s*\d+[.)]/.test(line);
      const items = [];
      while (i < lines.length && /^\s*([-*+]|\d+[.)])\s+/.test(lines[i])) {
        let item = lines[i].replace(/^\s*([-*+]|\d+[.)])\s+/, ""); i++;
        while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*([-*+]|\d+[.)])\s+/.test(lines[i])) {
          item += " " + lines[i].trim(); i++;
        }
        items.push(`<li dir="auto">${inline(item, refs)}</li>`);
      }
      out.push(ordered ? `<ol>${items.join("")}</ol>` : `<ul>${items.join("")}</ul>`);
      continue;
    }
    para.push(line); i++;
  }
  flush();
  return out.join("\n");
}

// ------------------------------------------------------------ görünüm (bu cihazda)

function stored(key) {
  try { return JSON.parse(localStorage.getItem(key)) || {}; } catch { return {}; }
}
function store(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* yok */ }
}

const look = { tema: "", boyut: "", ...stored(LOOK) };
function applyLook() {
  const root = document.documentElement;
  for (const k of ["tema", "boyut"]) {
    if (look[k]) root.dataset[k] = look[k]; else delete root.dataset[k];
  }
}
applyLook();

// ------------------------------------------------------------ panel genişlikleri (S13.2)

const SIZE = { left: { def: 272, min: 200, max: 440 }, right: { def: 380, min: 280, max: 720 } };
const MIN_MIDDLE = 420;                 // sohbetin en dar hâli
const widths = { left: SIZE.left.def, right: SIZE.right.def, ...stored(WIDTHS) };

function clampWidth(which, w) {
  const other = which === "left" ? "right" : "left";
  const otherDocked = docked[other].matches && panels[other] ? widths[other] : 0;
  const room = window.innerWidth - otherDocked - MIN_MIDDLE;
  return Math.round(Math.max(SIZE[which].min, Math.min(SIZE[which].max, room, w)));
}

function applyWidths() {
  const root = document.documentElement.style;
  root.setProperty("--sol-w", `${widths.left}px`);
  root.setProperty("--yan-w", `${widths.right}px`);
  for (const [which, handle] of [["left", $("ayir-sol")], ["right", $("ayir-yan")]]) {
    handle.setAttribute("aria-valuenow", widths[which]);
    handle.setAttribute("aria-valuemin", SIZE[which].min);
    handle.setAttribute("aria-valuemax", SIZE[which].max);
  }
}

function setWidth(which, w, save = true) {
  widths[which] = clampWidth(which, w);
  applyWidths();
  if (save) store(WIDTHS, { left: widths.left, right: widths.right });
}

function resizer(handle, which) {
  // sol panel sağ kenarından, Kaynaklar sol kenarından büyür
  const sign = which === "left" ? 1 : -1;
  handle.addEventListener("pointerdown", (ev) => {
    if (ev.button !== 0) return;
    ev.preventDefault();
    handle.setPointerCapture(ev.pointerId);
    const startX = ev.clientX, startW = widths[which];
    handle.classList.add("suruklenen");
    document.body.classList.add("suruklenir");
    const move = (e) => setWidth(which, startW + sign * (e.clientX - startX), false);
    const up = () => {
      handle.removeEventListener("pointermove", move);
      handle.removeEventListener("pointerup", up);
      handle.removeEventListener("pointercancel", up);
      handle.classList.remove("suruklenen");
      document.body.classList.remove("suruklenir");
      setWidth(which, widths[which]);
    };
    handle.addEventListener("pointermove", move);
    handle.addEventListener("pointerup", up);
    handle.addEventListener("pointercancel", up);
  });
  handle.addEventListener("dblclick", () => setWidth(which, SIZE[which].def));
  handle.addEventListener("keydown", (ev) => {
    const step = ev.shiftKey ? 48 : 16;
    const delta = { ArrowLeft: -step * sign, ArrowRight: step * sign }[ev.key];
    if (delta) { ev.preventDefault(); setWidth(which, widths[which] + delta); }
    else if (ev.key === "Home" || ev.key === "End") {
      ev.preventDefault();
      setWidth(which, ev.key === "Home" ? SIZE[which].min : SIZE[which].max);
    } else if (ev.key === "Enter") { ev.preventDefault(); setWidth(which, SIZE[which].def); }
  });
}

// ------------------------------------------------------------ paneller

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function prefs() {
  try { return { left: true, right: true, ...JSON.parse(localStorage.getItem(PANELS)) }; } catch { return { left: true, right: true }; }
}
const panels = { left: prefs().left, right: prefs().right };     // geniş ekranda tercih
const drawers = { left: false, right: false };                     // dar ekranda çekmece

function isOpen(which) { return docked[which].matches ? panels[which] : drawers[which]; }

function layout() {
  for (const which of ["left", "right"]) {
    const node = which === "left" ? els.left : els.side;
    node.classList.toggle("acik", isOpen(which));
  }
  document.body.classList.toggle("sol-yerinde", docked.left.matches && panels.left);
  document.body.classList.toggle("yan-yerinde", docked.right.matches && panels.right);
  els.leftOpen.setAttribute("aria-expanded", String(isOpen("left")));
  els.open.setAttribute("aria-expanded", String(isOpen("right")));
  els.shade.hidden = !((!docked.left.matches && drawers.left) || (!docked.right.matches && drawers.right));
  for (const which of ["left", "right"]) {          // pencere daraldıysa ya da öbür panel açıldıysa sığdır
    if (docked[which].matches && panels[which]) widths[which] = clampWidth(which, widths[which]);
  }
  applyWidths();
}

function setPanel(which, open) {
  if (docked[which].matches) {
    panels[which] = open;
    try { localStorage.setItem(PANELS, JSON.stringify(panels)); } catch { /* yok */ }
  } else {
    drawers[which] = open;
    if (open) drawers[which === "left" ? "right" : "left"] = false;     // tek çekmece
  }
  layout();
}

function closeDrawers() { drawers.left = drawers.right = false; layout(); }

// ------------------------------------------------------------ Kaynaklar

// S13.5: konuşmanın tek kaynakçası. Sunucu her cevabı kendi kaynakçasıyla (1'den) verir ve saklar; sayfa numaraları
// konuşma boyunca yeniden verir: kaynak ilk geçtiği yerde numarasını alır, sonra hep onunla anılır. Cevaplar yalnız
// sona eklendiği için önceki numaralar değişmez.
// S13.6: kaynak, bir bölümün kesintisiz bir parçasıdır. Aynı bölümde örtüşen ya da bitişik cümleler tek kaynakta
// (parça) birleşir, en çok PIECE_MAX cümle; hâşiye cümlesi, bölüm atfı ve doğrulanamayan alıntı birleşmez. Parça
// tıklanınca açılır; o atfın cümleleri koyu, parçanın öbürleri açık vurgulu. Liste bölüm başlıklarıyla gruplu.
// Numara ve parça kaynağın nesnesine yazılmaz (yerel kayda girmesin): `pieceOf`.
const PIECE_MAX = 8;
const pieceOf = new WeakMap();          // kaynak -> parça
let catalog = [];                       // parçalar, numara sırasıyla

function num(src) { const p = pieceOf.get(src); return p ? p.g : src.n; }

const SENTENCE_ID = /^(.+)\/c(\d{3,})(?:\.\.c(\d{3,}))?$/;
const pad = (n) => String(n).padStart(3, "0");

function span(src) {                    // birleşebilen kaynakta {node, start, end}
  if (!src.id || src.problem || src.unverified) return null;
  const m = src.id.match(SENTENCE_ID);
  if (!m || /\/c\d{3,}\/[hs]\d+$/.test(m[1])) return null;          // hâşiye ve şerh cümlesi birleşmez
  return { node: m[1], start: Number(m[2]), end: Number(m[3] || m[2]) };
}

function splitCite(cite) {              // "Yol › Bölüm › “İlk kelimeler…” ile başlayan 3 cümle" -> [yol, son parça]
  const i = (cite || "").lastIndexOf(" › ");
  return i < 0 ? [cite || "Adresi bulunamadı", ""] : [cite.slice(0, i), cite.slice(i + 3)];
}

function numberSources() {
  catalog = [];
  const byKey = new Map();              // birleşmeyenler: kimlik -> parça
  cur.turns.forEach((t, i) => {
    for (const src of t.sources || []) {
      const sp = span(src);
      let piece = null;
      if (sp) {
        piece = catalog.find((p) => p.node === sp.node && sp.start <= p.end + 1 && sp.end >= p.start - 1
          && Math.max(p.end, sp.end) - Math.min(p.start, sp.start) + 1 <= PIECE_MAX);
        if (piece) {
          if (sp.start < piece.start) { piece.start = sp.start; piece.first = src; }
          piece.end = Math.max(piece.end, sp.end);
        }
      } else {
        piece = byKey.get(src.id ? src.id + (src.problem || src.unverified ? "!" : "") : `#${i}:${src.n}`) || null;
      }
      if (!piece) {
        piece = { g: catalog.length + 1, node: sp && sp.node, start: sp && sp.start, end: sp && sp.end,
          first: src, header: splitCite(src.cite_as)[0], members: [], turns: [] };
        catalog.push(piece);
        if (!sp) byKey.set(src.id ? src.id + (src.problem || src.unverified ? "!" : "") : `#${i}:${src.n}`, piece);
      }
      piece.members.push(src);
      if (!piece.turns.includes(i)) piece.turns.push(i);
      pieceOf.set(src, piece);
    }
  });
}

function pieceId(piece) {               // parçanın metni istenirken
  if (!piece.node) return piece.first.id;
  return piece.start === piece.end ? `${piece.node}/c${pad(piece.start)}`
    : `${piece.node}/c${pad(piece.start)}..c${pad(piece.end)}`;
}

function pieceLabel(piece) {            // "“İlk kelimeler…”" ya da "“İlk kelimeler…” ile başlayan 3 cümle"
  const tail = splitCite(piece.first.cite_as)[1];
  if (!piece.node) return tail;
  const incipit = tail.replace(/ ile başlayan \d+ cümle$/, "");
  const count = piece.end - piece.start + 1;
  return count > 1 ? `${incipit} ile başlayan ${count} cümle` : incipit;
}

function pieceCite(piece) { const l = pieceLabel(piece); return l ? `${piece.header} › ${l}` : piece.header; }

function turnNote(turns) {              // "1. soruda", "1. ve 3. soruda", "1., 2. ve 4. soruda"
  const ns = turns.map((i) => `${i + 1}.`);
  return (ns.length > 1 ? `${ns.slice(0, -1).join(", ")} ve ${ns[ns.length - 1]}` : ns[0]) + " soruda";
}

function sourceList(pieces) {           // bölüm başlıklarıyla gruplu; gruplar ilk numaralarının sırasıyla
  const box = el("div", "kaynak-listesi");
  const groups = new Map();
  for (const p of pieces) {
    if (!groups.has(p.header)) groups.set(p.header, []);
    groups.get(p.header).push(p);
  }
  const names = new Set(pieces.map((p) => p.first.source_name).filter(Boolean));
  for (const [header, items] of groups) {
    const group = el("section", "kaynak-grup");
    group.append(el("h3", "", esc(header)));
    const ol = el("ol");
    for (const p of items) {
      const s = p.first;
      const bad = p.members.some((m) => m.problem);
      const li = el("li");
      const b = el("button", "kaynak" + (bad ? " kotu" : ""));
      b.type = "button";
      b.dataset.g = p.g;
      const label = pieceLabel(p) || "Bölümün tamamı";
      const meta = [names.size > 1 && s.source_name ? `Kaynak: ${esc(s.source_name)}` : "",
        cur.turns.length > 1 ? turnNote(p.turns) : ""].filter(Boolean).join(" · ");
      b.innerHTML = `<span class="no">[${p.g}]</span><span class="yol-metin">${esc(label)}</span>`
        + (meta ? `<span class="kaynak-adi">${meta}</span>` : "");
      li.append(b);
      const seen = new Set();
      for (const m of p.members) {
        for (const e of m.embedded || []) {
          if (!seen.has(e.line)) { seen.add(e.line); li.append(el("div", "gomulu", "– " + esc(e.line))); }
        }
      }
      if (bad) li.append(el("div", "uyari", "⚠ Bu alıntı eserlerin metniyle doğrulanamadı."));
      ol.append(li);
    }
    group.append(ol);
    box.append(group);
  }
  if (names.size === 1) box.append(el("p", "kaynak-adi", `Kaynak: ${esc([...names][0])}`));
  return box;
}

function turnPieces(sources) {
  return [...new Set((sources || []).map((s) => pieceOf.get(s)).filter(Boolean))].sort((a, b) => a.g - b.g);
}

function renderSources(box, sources) {          // cevabın altında (Kaynaklar paneli yerinde açık değilse görünür)
  if (!sources || !sources.length) return;
  const wrap = el("div", "kaynaklar");
  wrap.append(el("h4", "", "Kaynaklar"));
  wrap.append(sourceList(turnPieces(sources)));
  box.append(wrap);
}

function renderSide() {                          // konuşmanın tek kaynakçası (S13.5, S13.6)
  els.sideList.innerHTML = "";
  if (catalog.length) els.sideList.append(sourceList(catalog));
  else els.sideList.innerHTML = SIDE_EMPTY;
  els.count.textContent = catalog.length;
  els.count.hidden = !catalog.length;
}

function showList() {
  els.sideText.hidden = true;
  els.sideList.hidden = false;
  els.back.hidden = true;
  els.sideTitle.textContent = "Kaynaklar";
}

// ------------------------------------------------------------ yeni konuşma: örnek sorular (S13.3)

const EXAMPLES = [
  ["Konu taraması", ["Risale-i Nur'da şefkat hangi eserlerde, nasıl anlatılır?", "Tevekkül hangi risalelerde işlenir?",
    "Haşir meselesi hangi eserlerde ele alınır?"]],
  ["Bugünün diliyle", ["Hayatı anlamsız bulan birine Risale ne söyler?", "Ümitsizliğe düşen birine ne tavsiye edilir?",
    "Yalnızlık duygusuyla nasıl baş edilir?"]],
  ["Bir bölümü anlamak", ["Onuncu Söz'ün Dokuzuncu Hakikati'ni sade bir dille özetler misin?",
    "Hastalar Risalesi'nin ilk devalarını özetler misin?", "Yirmi Üçüncü Söz imanın insana ne kazandırdığını nasıl anlatır?"]],
  ["Temsiller", ["Birinci Söz'deki iki yolcu temsili neyi anlatır?", "Sekizinci Söz'deki kuyu temsilini açıklar mısın?",
    "Altıncı Söz'deki alışveriş temsili ne anlatır?"]],
  ["Âyetler", ["Âyetü'l-Kürsî Risale-i Nur'da nerelerde geçer?", "Yâsîn Sûresi'nin son âyetleri hangi bağlamlarda anılır?",
    "“Her nefis ölümü tadacaktır” âyeti nerelerde geçer?"]],
  ["Kelimeler", ["“Mânâ-yı harfî” ne demek, Risale'de nasıl kullanılır?", "“Tefekkür” ile “tezekkür” arasında fark var mı?",
    "“Hiss-i kable'l-vuku” ne demektir?"]],
  ["Hadisler", ["“Bir saat tefekkür” hadisi Risale'de nerede geçer, kaynağı nedir?",
    "“Dünya âhiretin tarlasıdır” sözü nerede geçer, kaynağı ne?"]],
  ["Meseleler", ["Kader ile cüz-i ihtiyarî nasıl bağdaşır?", "Musibetler insan için neden hayır olabilir?"]],
];
const pick = (list) => list[Math.floor(Math.random() * list.length)];

function renderExamples() {
  const box = $("ornekler");
  const groups = [...EXAMPLES].sort(() => Math.random() - .5).slice(0, 6);
  box.replaceChildren(...groups.map(([label, questions]) => {
    const b = el("button", "ornek");
    b.type = "button";
    const q = pick(questions);
    b.dataset.q = q;
    b.append(el("span", "ornek-tur", esc(label)), el("span", "", esc(q)));
    return b;
  }));
}

// ------------------------------------------------------------ cevaplar

const SHOWN_STEPS = 5;                   // beklerken görünen son adımlar

function stepList(steps, all = false) {
  const ol = el("ol", "adimlar");
  const shown = all ? steps : steps.slice(-SHOWN_STEPS);
  if (shown.length < steps.length) ol.append(el("li", "daha", `${steps.length - shown.length} adım daha`));
  for (const s of shown) ol.append(el("li", "", esc(s)));
  return ol;
}

function stepSummary(steps) {
  const d = el("details", "adim-ozet");
  const reads = steps.filter((s) => s.endsWith(" okunuyor")).length;
  d.append(el("summary", "", `${steps.length} adımda hazırlandı${reads ? ` · ${reads} yer okundu` : ""}`));
  d.append(stepList(steps, true));
  return d;
}

function renderTurn(turn) {
  const box = el("section", "tur");
  box.append(el("div", "soru-balon", esc(turn.q)));
  if (turn.markdown && turn.steps && turn.steps.length) box.append(stepSummary(turn.steps));
  const answer = el("div", "cevap");
  box.append(answer);
  if (turn.markdown) {
    const refs = new Map((turn.sources || []).map((s) => [s.n, s]));
    answer.innerHTML = markdown(turn.markdown, refs);
    renderSources(box, turn.sources);
    if (turn.corrected) box.append(el("p", "alt-bilgi", "Alıntılar denetimde düzeltildi."));
    box.append(feedbackBox(turn));
  }
  box._turn = turn;
  return box;
}

// ------------------------------------------------------------ geri bildirim (S12.12)

function answerText(turn) {          // okuyucunun gördüğü cevap, düz metin: yalnız kullanıcı onaylarsa gönderilir
  const local = new Map((turn.sources || []).map((s) => [s.n, s]));     // sayfadaki numaralarla (S13.5)
  const text = turn.markdown.replace(/\[(\d+)\]/g, (m, n) => (local.has(Number(n)) ? `[${num(local.get(Number(n)))}]` : m));
  const lines = turnPieces(turn.sources).map((p) => `[${p.g}] ${pieceCite(p)}`        // parçalarıyla (S13.6)
    + (p.first.source_name ? ` (${p.first.source_name})` : "") + (p.members.some((m) => m.problem) ? " ⚠ doğrulanamadı" : ""));
  return text + (lines.length ? "\n\nKaynaklar\n" + lines.join("\n") : "");
}

// S13.4: oy tıklanınca gider; not yazmayı bırakınca (ya da kutudan çıkınca) ve onay kutusu değişince aynı kayıt
// güncellenir (`fid`, sunucunun verdiği numara). Gönder düğmesi yok. Sayfa yenilenince oy görünür, değiştirilemez.
const THUMB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10v11M15 5.9 14 10h5.8a2 2 0 0 1 1.9 2.6l-2.3 7'
  + 'A2 2 0 0 1 17.5 21H4a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1h2.8a2 2 0 0 0 1.8-1.1L12 2a3.1 3.1 0 0 1 3 3.9Z"/></svg>';
const NOTE_PAUSE = 1500;             // yazmayı bırakınca bu kadar sonra gider (ms)

function feedbackBox(turn) {
  const wrap = el("div", "geri");
  const row = el("div", "geri-satir");
  const up = el("button", "oy", THUMB); up.type = "button";
  up.setAttribute("aria-label", "İşime yaradı"); up.title = "İşime yaradı";
  const down = el("button", "oy asagi", THUMB); down.type = "button";
  down.setAttribute("aria-label", "İşime yaramadı"); down.title = "İşime yaramadı";
  const status = el("span", "alt-bilgi geri-durum");
  status.setAttribute("aria-live", "polite");
  row.append(up, down, status);
  wrap.append(row);
  const mark = (vote) => {
    for (const [b, v] of [[up, 1], [down, -1]]) {
      b.classList.toggle("secili", v === vote); b.setAttribute("aria-pressed", String(v === vote));
    }
  };
  if (turn.feedback && !turn.fid) {          // önceki oturumda verilmiş
    mark(turn.feedback); up.disabled = down.disabled = true;
    status.textContent = "Geri bildiriminiz alındı. Teşekkürler.";
    return wrap;
  }
  const owner = cur;
  let form = null, timer = null, last = "", queue = Promise.resolve();
  const current = () => ({ vote: turn.feedback, note: form ? form.querySelector("textarea").value.trim() : "",
    share: form ? form.querySelector("input").checked : false });
  const send = async () => {
    const now = current(), key = JSON.stringify(now);
    if (key === last) return;
    status.classList.remove("hata"); status.textContent = "Gönderiliyor…";
    try {
      const r = await api("geri-bildirim", { ...now, ...(turn.fid ? { id: turn.fid } : {}),
        ...(now.share ? { question: turn.q, answer: answerText(turn) } : {}),
        ...(owner.id && Number.isInteger(turn.n) ? { conversation: owner.id, n: turn.n } : {}) });
      if (typeof r.id === "number") turn.fid = r.id;
      last = key; turn.fnote = now.note; turn.fshare = now.share;
      if (owner === cur) saveLocal();
      status.textContent = now.note || now.share ? "Notunuz alındı. Teşekkürler." : "Teşekkürler.";
    } catch (e) {
      status.textContent = e.message; status.classList.add("hata");
      if (!turn.fid) { turn.feedback = 0; mark(0); }        // kayıt açılmadı: oya yeniden basılabilsin
    }
  };
  const enqueue = () => { clearTimeout(timer); queue = queue.then(send); };   // sırayla: ilk kayıt numarasını alsın
  const openForm = () => {
    if (form) return;
    form = el("div", "geri-form");
    form.innerHTML = `<textarea rows="2" maxlength="1000" aria-label="Not"
      placeholder="İsterseniz not ekleyin: ne iyiydi, ne eksik ya da yanlıştı? Yazdığınız kendiliğinden gönderilir."></textarea>
      <label class="alt-bilgi"><input type="checkbox"> Soruyu ve bu cevabı da gönder (yalnız bu cevap; ekip
      saklanan konuşmalarınızı okumaz, yalnız böyle gönderdiklerinizi okur)</label>`;
    const area = form.querySelector("textarea");
    area.value = turn.fnote || ""; form.querySelector("input").checked = !!turn.fshare;
    area.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(enqueue, NOTE_PAUSE); });
    area.addEventListener("blur", enqueue);
    form.querySelector("input").addEventListener("change", enqueue);
    wrap.append(form);
  };
  const vote = (v) => {
    if (turn.feedback === v) return;
    turn.feedback = v; mark(v); openForm(); enqueue();
  };
  if (turn.feedback) { mark(turn.feedback); openForm(); last = JSON.stringify(current()); }   // bu oturumda yeniden çizildi
  up.addEventListener("click", () => vote(1));
  down.addEventListener("click", () => vote(-1));
  return wrap;
}

// ------------------------------------------------------------ açık konuşma

function renderTitle() {
  els.title.textContent = cur.title || "Yeni konuşma";
  if (!cur.id && !state.keep && cur.turns.length) {
    els.title.append(el("span", "gecici", "· yalnız bu tarayıcıda"));
  }
  document.title = `${cur.title ? cur.title + " · " : ""}Sohbet`;
}

function renderAll() {
  numberSources();
  els.list.innerHTML = "";
  cur.turns.forEach((t, i) => { const box = renderTurn(t); box._index = i; els.list.append(box); });
  els.empty.hidden = cur.turns.length > 0;
  renderSide();
  renderTitle();
  renderHistory();
}

function setHash(id) {
  const want = id ? `#k/${id}` : "";
  if (location.hash !== want) history.replaceState(null, "", want || location.pathname + location.search);
}

function newConversation() {
  if (busy) return;
  cur = { id: null, title: "", turns: [] };
  if (!state.keep) saveLocal();                          // geçici konuşmada "Yeni" eskisini siler
  setHash(null);
  showList();
  renderExamples();
  renderAll();
  if (!docked.left.matches) closeDrawers();
  els.input.focus();
}

async function openConversation(id, { push = true } = {}) {
  if (busy || !id) return;
  if (!docked.left.matches) closeDrawers();
  if (cur.id === id) return;
  els.list.innerHTML = '<p class="yukleniyor">Konuşma açılıyor…</p>';
  els.empty.hidden = true;
  try {
    const data = await api(`konusma?id=${encodeURIComponent(id)}`);
    cur = { id: data.id, title: data.title, turns: data.turns };
  } catch (e) {
    cur = { id: null, title: "", turns: [] };
    renderAll();
    els.list.innerHTML = `<p class="hata">${esc(e.message)}</p>`;
    els.empty.hidden = true;
    setHash(null);
    return;
  }
  if (push && location.hash !== `#k/${id}`) history.pushState(null, "", `#k/${id}`);
  showList();
  renderAll();
  const last = els.list.lastElementChild;
  if (last) last.scrollIntoView({ block: "start" });
}

window.addEventListener("popstate", () => {
  const m = location.hash.match(/^#k\/([\w-]+)$/);
  if (m) openConversation(m[1], { push: false });
  else if (cur.id) newConversation();
});

// ------------------------------------------------------------ sol panel: geçmiş konuşmalar

const GROUPS = [["Bugün", 0], ["Dün", 1], ["Son 7 gün", 7], ["Son 30 gün", 30], ["Daha eski", Infinity]];

function groupOf(ts) {
  const start = new Date(); start.setHours(0, 0, 0, 0);
  const days = Math.max(0, Math.ceil((start.getTime() / 1000 - ts) / 86400));
  return GROUPS.find(([, limit]) => days <= limit)[0];
}

function renderHistory() {
  els.history.innerHTML = "";
  if (!state.keep) {
    els.history.append(el("p", "small bilgi", "Saklama kapalı: yeni konuşmalar yalnız bu tarayıcıda durur. "
      + "Ayarlardan açabilirsiniz."));
  }
  if (!state.conversations.length) {
    if (state.keep) els.history.append(el("p", "small bilgi", "Konuşmalarınız burada listelenir."));
    return;
  }
  let group = null, ul = null;
  for (const c of state.conversations) {
    const g = groupOf(c.updated);
    if (g !== group) {
      group = g;
      els.history.append(el("h3", "", g));
      ul = el("ul");
      els.history.append(ul);
    }
    ul.append(historyItem(c));
  }
}

const PEN = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M13.5 3.5l3 3L7 16H4v-3z"/></svg>';
const BIN = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 6h12M8 6V4h4v2M6 6l1 10h6l1-10"/></svg>';

function historyItem(c) {
  const li = el("li", c.id === cur.id ? "secili" : "");
  const open = el("button", "ac");
  open.type = "button";
  open.textContent = c.title;
  open.title = c.title;
  if (c.id === cur.id) open.setAttribute("aria-current", "page");
  open.addEventListener("click", () => openConversation(c.id));
  const tools = el("div", "islem");
  const pen = el("button", "ikon", PEN); pen.type = "button"; pen.setAttribute("aria-label", `Adını değiştir: ${c.title}`);
  pen.title = "Adını değiştir";
  const bin = el("button", "ikon", BIN); bin.type = "button"; bin.setAttribute("aria-label", `Sil: ${c.title}`);
  bin.title = "Sil";
  tools.append(pen, bin);
  li.append(open, tools);

  pen.addEventListener("click", () => {
    const input = el("input");
    input.value = c.title;
    input.maxLength = 80;
    input.setAttribute("aria-label", "Konuşmanın adı");
    li.replaceChildren(input);
    input.focus(); input.select();
    let done = false;
    const finish = async (saveIt) => {
      if (done) return; done = true;
      const title = input.value.trim();
      if (saveIt && title && title !== c.title) {
        try {
          await api("konusma/ad", { id: c.id, title });
          c.title = title;
          if (cur.id === c.id) { cur.title = title; renderTitle(); }
        } catch { /* eski ad kalır */ }
      }
      renderHistory();
    };
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") { ev.preventDefault(); finish(true); }
      else if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); finish(false); }
    });
    input.addEventListener("blur", () => finish(true));
  });

  bin.addEventListener("click", () => {
    const ask = el("div", "onay");
    ask.append(el("span", "", "Silinsin mi?"));
    const yes = el("button", "dolu-tehlike", "Sil"); yes.type = "button";
    const no = el("button", "ghost", "Vazgeç"); no.type = "button";
    ask.append(yes, no);
    li.replaceChildren(ask);
    no.focus();
    no.addEventListener("click", renderHistory);
    yes.addEventListener("click", async () => {
      yes.disabled = true;
      try {
        await api("konusma/sil", { id: c.id });
        state.conversations = state.conversations.filter((x) => x.id !== c.id);
        if (cur.id === c.id) newConversation(); else renderHistory();
      } catch (e) {
        ask.replaceChildren(el("span", "hata", esc(e.message)));
        setTimeout(renderHistory, 2500);
      }
    });
  });
  return li;
}

async function refreshHistory() {
  try { state.conversations = (await api("konusmalar")).conversations; } catch { /* liste eski kalır */ }
  const mine = cur.id && state.conversations.find((c) => c.id === cur.id);
  if (mine && mine.title !== cur.title) { cur.title = mine.title; renderTitle(); }    // başlığı sunucu koyar
  renderHistory();
}

// ------------------------------------------------------------ alt satır: günün kalan hakkı

function renderQuota() {
  if (state.questions === null || state.remaining === null) { els.quota.hidden = true; return; }
  els.quota.hidden = false;
  els.quota.textContent = `Bugünkü soru hakkı: ${state.remaining}/${state.questions}`;
  els.quota.classList.toggle("bitti", state.remaining <= 0);
  els.quota.title = state.remaining > 0 ? "Bugün sorabileceğiniz soru sayısı" : "Yarın yeniden sorabilirsiniz";
}

// ------------------------------------------------------------ ayarlar (S13.2: sekmeli)

const tabs = [...els.settings.querySelectorAll('[role="tab"]')];
function selectTab(tab, focus = false) {
  for (const t of tabs) {
    const on = t === tab;
    t.setAttribute("aria-selected", String(on));
    t.tabIndex = on ? 0 : -1;
    $(t.getAttribute("aria-controls")).hidden = !on;
  }
  if (focus) tab.focus();
}
for (const tab of tabs) {
  tab.addEventListener("click", () => selectTab(tab));
  tab.addEventListener("keydown", (ev) => {
    const i = tabs.indexOf(tab);
    const next = { ArrowDown: i + 1, ArrowRight: i + 1, ArrowUp: i - 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[ev.key];
    if (next === undefined) return;
    ev.preventDefault();
    selectTab(tabs[(next + tabs.length) % tabs.length], true);
  });
}
for (const name of ["tema", "boyut"]) {
  for (const input of els.settings.querySelectorAll(`input[name="${name}"]`)) {
    input.addEventListener("change", () => {
      if (!input.checked) return;
      look[name] = input.value;
      store(LOOK, look);
      applyLook();
    });
  }
}
$("genislik-sifirla").addEventListener("click", () => {
  widths.left = SIZE.left.def; widths.right = SIZE.right.def;
  try { localStorage.removeItem(WIDTHS); } catch { /* yok */ }
  layout();
});

els.settingsOpen.addEventListener("click", () => {
  els.keep.checked = state.keep;
  for (const name of ["tema", "boyut"]) {
    for (const input of els.settings.querySelectorAll(`input[name="${name}"]`)) input.checked = input.value === look[name];
  }
  els.wipeAsk.hidden = true; els.wipe.hidden = false; els.settingsError.hidden = true;
  els.settings.showModal();
});
els.settingsClose.addEventListener("click", () => els.settings.close());
els.settings.addEventListener("click", (ev) => { if (ev.target === els.settings) els.settings.close(); });
els.keep.addEventListener("change", async () => {
  const want = els.keep.checked;
  els.keep.disabled = true;
  try {
    await api("ayarlar", { keep: want });
    state.keep = want;
    els.settingsError.hidden = true;
    if (!cur.id && !busy) newConversation(); else renderAll();
  } catch (e) {
    els.keep.checked = !want;
    els.settingsError.textContent = e.message; els.settingsError.hidden = false;
  } finally {
    els.keep.disabled = false;
  }
});
els.wipe.addEventListener("click", () => { els.wipe.hidden = true; els.wipeAsk.hidden = false; els.wipeNo.focus(); });
els.wipeNo.addEventListener("click", () => { els.wipeAsk.hidden = true; els.wipe.hidden = false; });
els.wipeYes.addEventListener("click", async () => {
  els.wipeYes.disabled = true;
  try {
    await api("konusma/sil", { all: true });
    state.conversations = [];
    try { localStorage.removeItem(KEY); } catch { /* yok */ }
    els.wipeAsk.hidden = true; els.wipe.hidden = false;
    if (!busy) { cur = { id: null, title: "", turns: [] }; newConversation(); }
    els.settingsError.hidden = true;
    els.settings.close();
  } catch (e) {
    els.settingsError.textContent = e.message; els.settingsError.hidden = false;
  } finally {
    els.wipeYes.disabled = false;
  }
});

// ------------------------------------------------------------ olaylar

function sourceOf(box, n) {
  return (box._turn.sources || []).find((s) => s.n === Number(n));
}

els.list.addEventListener("click", (ev) => {
  const box = ev.target.closest(".tur");
  if (!box || !box._turn) return;
  let target = ev.target.closest(".ref, .kaynak");
  if (!target) {
    const quote = ev.target.closest("blockquote");
    if (quote) target = quote.querySelector(".ref");
  }
  if (!target) return;
  if (target.classList.contains("kaynak")) {           // cevabın altındaki liste: parçanın tamamı
    const piece = catalog.find((p) => p.g === Number(target.dataset.g));
    if (piece) openText(piece);
    return;
  }
  const src = sourceOf(box, target.dataset.n);
  if (src) openText(pieceOf.get(src) || null, src);
});

els.sideList.addEventListener("click", (ev) => {
  const b = ev.target.closest(".kaynak");
  if (!b) return;
  const piece = catalog.find((p) => p.g === Number(b.dataset.g));
  if (piece) openText(piece);
});
els.back.addEventListener("click", showList);
els.open.addEventListener("click", () => {
  const open = !isOpen("right");
  if (open) showList();
  setPanel("right", open);
});
els.close.addEventListener("click", () => setPanel("right", false));
els.leftOpen.addEventListener("click", () => setPanel("left", !isOpen("left")));
els.leftClose.addEventListener("click", () => setPanel("left", false));
els.shade.addEventListener("click", closeDrawers);
document.addEventListener("keydown", (ev) => {
  if (ev.key !== "Escape" || els.settings.open) return;
  if (!els.shade.hidden) closeDrawers();
  else if (!els.sideText.hidden) showList();
});
for (const mq of Object.values(docked)) mq.addEventListener("change", () => { drawers.left = drawers.right = false; layout(); });
let resizeFrame = 0;
window.addEventListener("resize", () => {
  if (!resizeFrame) resizeFrame = requestAnimationFrame(() => { resizeFrame = 0; layout(); });
});
resizer($("ayir-sol"), "left");
resizer($("ayir-yan"), "right");

// ------------------------------------------------------------ metin penceresi

async function openText(piece, focus) {  // parça; `focus` metindeki atfın kaynağıysa onun cümleleri koyu (S13.6)
  const src = focus || piece.first;
  const cite = piece ? pieceCite(piece) : src.cite_as;
  els.dpath.textContent = cite || "Adresi bulunamadı";
  els.dsource.textContent = src.source_name ? `Kaynak: ${src.source_name}` : "";
  els.dbody.innerHTML = '<p class="small">Yükleniyor…</p>';
  els.sideList.hidden = true;
  els.sideText.hidden = false;
  els.back.hidden = false;
  els.sideTitle.textContent = `[${num(src)}]`;
  els.sideText.scrollTop = 0;
  for (const b of els.sideList.querySelectorAll(".kaynak.secili")) b.classList.remove("secili");
  const item = els.sideList.querySelector(`.kaynak[data-g="${num(src)}"]`);
  if (item) item.classList.add("secili");
  setPanel("right", true);
  const sp = focus ? span(focus) : null;
  const strong = (id) => {               // atfın kendi cümlesi mi (yoksa parçanın öbür cümlesi)
    if (!sp) return true;
    const m = id.match(SENTENCE_ID);
    return !!m && m[1] === sp.node && Number(m[2]) >= sp.start && Number(m[2]) <= sp.end;
  };
  try {
    const data = await api(`metin?id=${encodeURIComponent(piece ? pieceId(piece) : src.id)}`);
    els.dpath.textContent = data.section_ref && piece && piece.node
      ? `${data.section_ref} › ${pieceLabel(piece)}` : data.section_ref || cite || "Adresi bulunamadı";
    const parts = [];
    if (src.unverified) parts.push('<p class="uyari">⚠ Alıntının sözleri bu cümlelerde ve eserlerin başka bir yerinde bulunamadı; cevabın gösterdiği yer bu.</p>');
    for (const s of data.sentences || []) {
      const body = esc(s.text);
      const mark = !s.target ? body : strong(s.id) ? `<mark>${body}</mark>` : `<mark class="acik">${body}</mark>`;
      parts.push(`<p class="cumle" dir="auto">${mark}</p>`);
      for (const a of s.arabic || []) {
        if (a.publisher_translation) {
          parts.push(`<p class="meal">${esc(a.source || "")} · nâşirin meali: ${esc(a.publisher_translation)}</p>`);
        }
      }
      if (s.hasiye && s.hasiye.length) {
        parts.push(`<div class="hasiye" dir="auto">Hâşiye: ${esc(s.hasiye.map((x) => x.text).join(" "))}</div>`);
      }
    }
    if (data.note) parts.push(`<p class="small">${esc(data.note)}</p>`);
    els.dbody.innerHTML = parts.join("") || '<p class="small">Metin yok.</p>';
    const first = els.dbody.querySelector("mark:not(.acik)") || els.dbody.querySelector("mark");
    if (first) first.scrollIntoView({ block: "center" });
  } catch (e) {
    els.dbody.innerHTML = `<p class="hata">${esc(e.message)}</p>`;
  }
}

// ------------------------------------------------------------ soru

function setBusy(on) {
  busy = on;
  els.send.disabled = on;
  els.fresh.disabled = on;
}

async function ask(question) {
  if (busy || !question.trim()) return;
  setBusy(true);
  els.empty.hidden = true;
  const owner = cur;                     // cevap bu konuşmaya yazılır
  const turn = { q: question.trim() };
  const box = renderTurn(turn);
  els.list.append(box);
  const answer = box.querySelector(".cevap");
  const status = el("div", "durum", "Soru gönderiliyor…");
  const steps = [];                      // biten araç adımları
  let current = null;                    // şu anki satır (araç adımıysa biter bitmez listeye geçer)
  let trail = stepList(steps);
  box.insertBefore(trail, answer);
  box.insertBefore(status, answer);
  const showSteps = () => { const fresh = stepList(steps); trail.replaceWith(fresh); trail = fresh; };
  box.scrollIntoView({ block: "start", behavior: "smooth" });

  let draft = "";
  let frame = 0;
  const paint = () => { frame = 0; answer.innerHTML = markdown(draft, null); };
  // saklanan konuşmanın geçmişini sunucu okur; geçici konuşmada tarayıcı gönderir
  const body = owner.id ? { question: turn.q, conversation: owner.id }
    : state.keep ? { question: turn.q } : { question: turn.q, history: owner.turns.map((t) => ({ q: t.q, a: t.a, r: t.r })) };
  let finished = false;

  const handle = (event, data) => {
    if (event === "status") {
      if (current && current.step) { steps.push(current.text); showSteps(); }
      current = data;
      status.textContent = data.text; status.hidden = false;
    }
    else if (event === "delta") {
      draft += data.text;
      status.hidden = true;
      if (!frame) frame = requestAnimationFrame(paint);
    } else if (event === "clear") { draft = ""; answer.innerHTML = ""; }
    else if (event === "restart") {
      draft = ""; answer.innerHTML = "";
      status.textContent = data.text; status.hidden = false;
    } else if (event === "done") {
      finished = true;
      Object.assign(turn, { markdown: data.markdown, sources: data.sources, corrected: data.corrected,
        steps: data.steps || [] });
      if (data.conversation) {
        turn.n = data.n;
        if (!owner.id) {
          owner.id = data.conversation;
          owner.title = owner.title || turn.q.replace(/\s+/g, " ").slice(0, 80);
        }
      } else {
        turn.a = data.raw;               // geçici konuşma: sonraki soruda geçmiş olarak gider
        turn.r = data.reads;             // ve çağrılan araçlar (S13.4 (c))
      }
      owner.turns.push(turn);
      if (typeof data.remaining === "number") { state.remaining = data.remaining; state.questions = data.questions; }
      renderQuota();
      if (owner !== cur) return;          // başka konuşma açıldıysa sayfaya çizilmez (busy iken açılamaz)
      saveLocal();
      numberSources();
      const fresh = renderTurn(turn);
      fresh._index = owner.turns.length - 1;
      box.replaceWith(fresh);
      renderSide();
      if (owner.id) { setHash(owner.id); refreshHistory(); }
      renderTitle();
    } else if (event === "error") {
      finished = true;
      status.remove();
      box.append(el("p", "hata", esc(data.message)));
    }
  };

  try {
    const r = await fetch(`${P}api/sor`, {
      method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (r.status === 401) { location.href = `${P}giris?next=${encodeURIComponent(P)}`; return; }
    if (!r.ok || !r.body) {
      let msg = "Soru gönderilemedi.";
      try { msg = (await r.json()).error || msg; } catch { /* yok */ }
      handle("error", { message: msg });
      return;
    }
    const reader = r.body.getReader();
    const dec = new TextDecoder();
    let buf = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let k;
      while ((k = buf.indexOf("\n\n")) >= 0) {
        const chunk = buf.slice(0, k); buf = buf.slice(k + 2);
        let event = "message", data = "";
        for (const l of chunk.split("\n")) {
          if (l.startsWith("event: ")) event = l.slice(7);
          else if (l.startsWith("data: ")) data += l.slice(6);
        }
        try { handle(event, JSON.parse(data || "{}")); } catch { /* bozuk parça */ }
      }
    }
    if (!finished) handle("error", { message: "Bağlantı kesildi; yeniden sorun." });
  } catch {
    if (!finished) handle("error", { message: "Bağlantı kurulamadı; yeniden deneyin." });
  } finally {
    setBusy(false);
    els.input.focus();
  }
}

els.form.addEventListener("submit", (ev) => {
  ev.preventDefault();
  const q = els.input.value;
  if (!q.trim() || busy) return;
  els.input.value = "";
  grow();
  ask(q);
});
els.input.addEventListener("keydown", (ev) => {
  if (ev.key === "Enter" && !ev.shiftKey && !ev.isComposing) { ev.preventDefault(); els.form.requestSubmit(); }
});
function grow() { els.input.style.height = "auto"; els.input.style.height = els.input.scrollHeight + "px"; }
els.input.addEventListener("input", grow);
$("ornekler").addEventListener("click", (ev) => {
  const b = ev.target.closest(".ornek");
  if (b) ask(b.dataset.q);
});
$("baska-ornek").addEventListener("click", renderExamples);
els.fresh.addEventListener("click", newConversation);

// ------------------------------------------------------------ açılış

async function start() {
  layout();
  renderExamples();
  try {
    const s = await api("durum");
    Object.assign(state, { keep: s.keep, questions: s.questions, remaining: s.remaining });
  } catch { /* varsayılanlarla sürer */ }
  renderQuota();
  await refreshHistory();
  const m = location.hash.match(/^#k\/([\w-]+)$/);
  if (m) { await openConversation(m[1], { push: false }); return; }
  cur = { id: null, title: "", turns: state.keep ? [] : loadLocal() };
  renderAll();
}

start();
