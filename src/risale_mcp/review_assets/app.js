"use strict";

// Sayfaya gömülü veri: eserler, gruplar ve bütün eserlerin başlık ağaçları. Bir eserin paragraf
// ve cümleleri `data/<eser>.js` dosyasındadır; o eserden bir başlık açılınca yüklenir.
const DATA = JSON.parse(document.getElementById("data").textContent);
const STORAGE_PREFIX = "risale-review:";   // işaretler eser başına ayrı anahtarda: risale-review:sozler
const ROOT = "";

// ------------------------------------------------------------------ indeksler

const works = new Map(DATA.works.map((w) => [w.slug, w]));
const nodes = new Map();        // id -> outline kaydı (bütün eserler)
const order = [];               // eserler katalog, düğümler kitap sırasıyla
const childrenOf = new Map();   // ebeveyn kimliği -> çocuk kimlikleri
const passagesOf = new Map();   // düğüm kimliği -> ana pasajlar (sıralı); yüklenen eserler
const hasiyeOf = new Map();     // pasaj kimliği -> hâşiyeler
const passageById = new Map();
const sentencesOf = new Map();  // paragraf kimliği -> cümleleri (sıralı)
const sentenceById = new Map();
const sentencesOfWork = new Map();

function pushTo(map, key, value) {
  if (!map.has(key)) map.set(key, []);
  map.get(key).push(value);
}

for (const node of DATA.outline) {
  nodes.set(node.id, node);
  order.push(node.id);
  pushTo(childrenOf, node.parent_id ?? ROOT, node.id);
}

const workOf = (id) => id.split("/")[0];
const children = (id) => childrenOf.get(id) ?? [];
const ownPassages = (id) => passagesOf.get(id) ?? [];

function ancestors(id) {
  const chain = [];
  for (let n = nodes.get(id); n && n.parent_id; n = nodes.get(n.parent_id)) chain.unshift(n.parent_id);
  return chain;
}

/** Paragraf, hâşiye ve cümle kimlikleri düğümün altındadır: sozler/10/p003/h1, sozler/10/c032/h1/c002.
 * Düğüm, eserin metni yüklenmeden de kimlikten bulunur. */
function nodeIdOf(targetId) {
  if (nodes.has(targetId)) return targetId;
  const nodeId = targetId.replace(/\/[pc]\d{3,}(\/.*)?$/, "");
  return nodes.has(nodeId) ? nodeId : null;
}

const targetKind = (id) =>
  nodes.has(id) ? "node" : sentenceById.has(id) ? "sentence" : passageById.has(id) ? "passage" : "missing";
const refOf = (id) => nodes.get(id)?.ref ?? sentenceById.get(id)?.ref ?? passageById.get(id)?.ref ?? null;

/** Arama için: Türkçe küçük harf, şapkasız, kesme işaretsiz. */
function fold(text) {
  return text
    .replace(/I/g, "ı").replace(/İ/g, "i").toLowerCase()
    .normalize("NFD").replace(/̂/g, "").normalize("NFC")
    .replace(/['’]/g, "");
}

// ------------------------------------------------------------------ eser metinlerinin yüklenmesi

const loading = new Map();      // eser -> Promise

const RisaleReview = {
  /** `data/<eser>.js` bunu çağırır. */
  register(view) {
    for (const p of view.passages) {
      passageById.set(p.id, p);
      if (p.kind === "hasiye") pushTo(hasiyeOf, p.parent_id, p);
      else pushTo(passagesOf, p.node_id, p);
    }
    for (const s of view.sentences) {
      sentenceById.set(s.id, s);
      pushTo(sentencesOf, s.p, s);
    }
    sentencesOfWork.set(view.book, view.sentences);
    if (Marks.reanchor(view.book)) onMarksChanged();
  },
};
window.RisaleReview = RisaleReview;

function loadWork(slug) {
  if (!loading.has(slug)) {
    loading.set(slug, new Promise((resolve, reject) => {
      const script = el("script", { src: `data/${slug}.js` });
      script.addEventListener("load", resolve);
      script.addEventListener("error", () => {
        loading.delete(slug);
        reject(new Error(`data/${slug}.js yüklenemedi; \`uv run python -m risale_mcp.review_ui\` çalıştırın.`));
      });
      document.head.append(script);
    }));
  }
  return loading.get(slug);
}

// ------------------------------------------------------------------ işaret deposu

const Marks = {
  byWork: {},     // eser -> {kimlik -> işaret}

  load() {
    for (const slug of works.keys()) {
      try {
        this.byWork[slug] = JSON.parse(localStorage.getItem(STORAGE_PREFIX + slug) ?? "{}");
      } catch {
        this.byWork[slug] = {};
      }
    }
  },

  save(slug) {
    try {
      localStorage.setItem(STORAGE_PREFIX + slug, JSON.stringify(this.byWork[slug]));
    } catch (err) {
      console.warn("İşaretler kaydedilemedi:", err);
    }
  },

  of(slug) {
    return (this.byWork[slug] ??= {});
  },

  *entries() {
    for (const [slug, marks] of Object.entries(this.byWork)) {
      for (const [id, mark] of Object.entries(marks)) yield [id, mark, slug];
    }
  },

  get(id) {
    return this.of(workOf(id))[id] ?? { status: null, note: "" };
  },

  /** `patch` cümle işaretlerinde bağlamı da taşır: {incipit, node}; kimlik kayarsa işaret bundan bulunur. */
  update(id, patch) {
    const slug = workOf(id);
    const marks = this.of(slug);
    const next = { ...this.get(id), ...patch };
    if (!next.status && !next.note) delete marks[id];
    else marks[id] = next;
    this.save(slug);
  },

  /** Eserin metni yüklenince, kimliği artık bulunmayan cümle işaretlerini aynı düğümde (yoksa
   * bütün eserde tek eşleşen) incipit'ten yeniden bağlar. Bölme kuralları değişince numaralar kayabilir. */
  reanchor(slug) {
    const marks = this.of(slug);
    const sentences = sentencesOfWork.get(slug) ?? [];
    let moved = 0;
    for (const [id, mark] of Object.entries(marks)) {
      if (targetKind(id) !== "missing" || !mark.incipit) continue;
      const same = (s) => s.incipit.startsWith(mark.incipit) || mark.incipit.startsWith(s.incipit);
      const inNode = sentences.filter((s) => same(s) && nodeIdOf(s.id) === mark.node);
      const anywhere = sentences.filter(same);
      const match = inNode.length === 1 ? inNode[0] : anywhere.length === 1 ? anywhere[0] : null;
      if (!match || marks[match.id]) continue;
      marks[match.id] = { ...mark, incipit: match.incipit, node: nodeIdOf(match.id) };
      delete marks[id];
      moved++;
    }
    if (moved) this.save(slug);
    return moved;
  },

  counts() {
    const c = { ok: 0, bad: 0, note: 0 };
    for (const [, m] of this.entries()) {
      if (m.status === "ok") c.ok++;
      if (m.status === "bad") c.bad++;
      if (m.note) c.note++;
    }
    return c;
  },
};

// ------------------------------------------------------------------ DOM yardımcıları

function el(tag, attrs = {}, ...kids) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key === "dataset") Object.assign(node.dataset, value);
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value);
  }
  node.append(...kids.filter((k) => k !== null && k !== undefined));
  return node;
}

const nodeLink = (id, text = nodes.get(id)?.title ?? id) => el("a", { href: `#${id}` }, text);

// ------------------------------------------------------------------ ağaç

const treeEl = document.getElementById("tree");
const treeItems = new Map();    // düğüm kimliği -> <li>
const groupItems = new Map();   // grup -> <li>

function treeRow(title, kids, meta) {
  return el("div", { class: "tree-row", title },
    el("span", { class: "caret" }, kids ? "▸" : ""),
    el("span", { class: "tree-title" }, title),
    el("span", { class: "tree-meta" }, meta),
    el("span", { class: "tree-mark" }),
    el("span", { class: "issue-dot", title: "Bu bölümde hatalı işaretli öğe var" }));
}

function buildTreeList(ids) {
  const ul = el("ul");
  for (const id of ids) {
    const node = nodes.get(id);
    const kids = children(id);
    const meta = [kids.length && `${kids.length} alt`, node.p && `¶${node.p}`].filter(Boolean).join(" · ");
    const li = el("li", { dataset: { id } }, treeRow(node.title, kids.length, meta));
    if (kids.length) li.append(buildTreeList(kids));
    treeItems.set(id, li);
    ul.append(li);
  }
  return ul;
}

/** En üstte gruplar (Eski Said dönemi, ana ciltler…), altlarında eserlerin ağaçları. */
function buildTree() {
  const ul = el("ul");
  for (const group of DATA.groups) {
    const roots = DATA.works.filter((w) => w.group === group.id).map((w) => w.slug);
    const li = el("li", { class: "tree-group", dataset: { group: group.id } },
      treeRow(group.title, roots.length, `${roots.length} eser`), buildTreeList(roots));
    groupItems.set(group.id, li);
    ul.append(li);
  }
  return ul;
}

function setOpen(li, open) {
  li.classList.toggle("open", open);
  const caret = li.querySelector(":scope > .tree-row .caret");
  if (caret.textContent) caret.textContent = open ? "▾" : "▸";
}

function onTreeClick(event) {
  const row = event.target.closest(".tree-row");
  if (!row) return;
  const li = row.parentElement;
  if (li.classList.contains("tree-group")) {
    setOpen(li, !li.classList.contains("open"));
    return;
  }
  const id = li.dataset.id;
  const hasKids = children(id).length > 0;

  if (event.target.classList.contains("caret")) {
    if (hasKids) setOpen(li, !li.classList.contains("open"));
    return;
  }
  if (location.hash.slice(1) === id && hasKids) setOpen(li, !li.classList.contains("open"));
  else {
    if (hasKids) setOpen(li, true);
    navigate(id);
  }
}

const groupItemOf = (id) => groupItems.get(works.get(workOf(id))?.group);

function revealInTree(id) {
  const group = groupItemOf(id);
  if (group) setOpen(group, true);
  for (const anc of ancestors(id)) setOpen(treeItems.get(anc), true);
  treeEl.querySelector(".tree-row.selected")?.classList.remove("selected");
  const row = treeItems.get(id)?.querySelector(":scope > .tree-row");
  if (row) {
    row.classList.add("selected");
    row.scrollIntoView({ block: "nearest" });
  }
}

function applySearch(query) {
  const q = fold(query.trim());
  for (const li of [...treeItems.values(), ...groupItems.values()]) {
    li.classList.remove("filtered-out", "force-open", "search-hit");
  }
  if (!q) return;

  const visible = new Set();
  const visibleGroups = new Set();
  for (const id of order) {
    const node = nodes.get(id);
    if (!fold(`${node.title} ${node.subtitle ?? ""}`).includes(q)) continue;
    treeItems.get(id).classList.add("search-hit");
    visible.add(id);
    visibleGroups.add(groupItemOf(id));
    for (const anc of ancestors(id)) {
      visible.add(anc);
      treeItems.get(anc).classList.add("force-open");
    }
  }
  for (const [id, li] of treeItems) if (!visible.has(id)) li.classList.add("filtered-out");
  for (const li of groupItems.values()) li.classList.add(visibleGroups.has(li) ? "force-open" : "filtered-out");
}

/** Ağaçtaki işaret simgelerini ve "altında hata var" noktalarını yeniler. */
function refreshTreeMarks() {
  const ownBad = new Set();
  for (const [id, mark] of Marks.entries()) {
    const nodeId = mark.status === "bad" ? nodeIdOf(id) : null;
    if (nodeId) ownBad.add(nodeId);
  }
  const subtreeBad = new Map();
  for (let i = order.length - 1; i >= 0; i--) {
    const id = order[i];
    subtreeBad.set(id, ownBad.has(id) || children(id).some((c) => subtreeBad.get(c)));
  }
  for (const [id, li] of treeItems) {
    const status = Marks.get(id).status;
    const markEl = li.querySelector(":scope > .tree-row .tree-mark");
    markEl.className = `tree-mark ${status ?? ""}`;
    markEl.textContent = status === "ok" ? "✓" : status === "bad" ? "✗" : "";
    li.querySelector(":scope > .tree-row .issue-dot").classList.toggle("on", Boolean(subtreeBad.get(id)));
  }
  for (const [group, li] of groupItems) {
    const bad = DATA.works.some((w) => w.group === group && subtreeBad.get(w.slug));
    li.querySelector(":scope > .tree-row .issue-dot").classList.toggle("on", bad);
  }
}

function refreshStats() {
  const c = Marks.counts();
  document.getElementById("stats").replaceChildren(
    el("span", { class: "ok" }, `✓ ${c.ok} doğru`), " · ",
    el("span", { class: "bad" }, `✗ ${c.bad} hatalı`), " · ",
    el("span", { class: "note" }, `✎ ${c.note} not`));
}

function onMarksChanged() {
  refreshTreeMarks();
  refreshStats();
}

// ------------------------------------------------------------------ işaret kontrolleri

function markControls(targetId, { container, context = {} } = {}) {
  const box = el("div", { class: "marks" });
  const note = el("textarea", { placeholder: "Not (ör. bu başlık bir üst bölüme ait)…" });
  const okBtn = el("button", { type: "button", title: "Doğru" }, "✓ Doğru");
  const badBtn = el("button", { type: "button", title: "Hatalı" }, "✗ Hatalı");
  const noteBtn = el("button", { type: "button", title: "Not ekle" }, "✎ Not");

  function render() {
    const mark = Marks.get(targetId);
    okBtn.classList.toggle("active-ok", mark.status === "ok");
    badBtn.classList.toggle("active-bad", mark.status === "bad");
    noteBtn.classList.toggle("active-note", Boolean(mark.note));
    box.classList.toggle("has-mark", Boolean(mark.status || mark.note));
    note.hidden = !mark.note && document.activeElement !== note && !box.dataset.noteOpen;
    if (container) {
      container.classList.toggle("status-ok", mark.status === "ok");
      container.classList.toggle("status-bad", mark.status === "bad");
    }
  }

  function setStatus(status) {
    Marks.update(targetId, { ...context, status: Marks.get(targetId).status === status ? null : status });
    render();
    onMarksChanged();
  }

  okBtn.addEventListener("click", () => setStatus("ok"));
  badBtn.addEventListener("click", () => setStatus("bad"));
  noteBtn.addEventListener("click", () => {
    box.dataset.noteOpen = "1";
    note.hidden = false;
    note.focus();
  });
  note.value = Marks.get(targetId).note;
  note.addEventListener("input", () => {
    Marks.update(targetId, { ...context, note: note.value.trim() ? note.value : "" });
    onMarksChanged();
  });
  note.addEventListener("blur", () => {
    delete box.dataset.noteOpen;
    render();
  });

  box.append(okBtn, badBtn, noteBtn, note);
  render();
  return box;
}

// ------------------------------------------------------------------ içerik

const contentEl = document.getElementById("content");

function applyStatus(elem, id) {
  const mark = Marks.get(id);
  elem.classList.toggle("status-ok", mark.status === "ok");
  elem.classList.toggle("status-bad", mark.status === "bad");
  elem.classList.toggle("has-note", Boolean(mark.note));
}

/** Paragrafı cümle cümle çizer (textContent ile, güvenli). Her cümlenin başında numara
 * düğmesi, hâşiye işaretleri de metindeki konumlarında düğme olarak durur. */
function renderSentences(passage, { onRefClick, onSentenceClick }) {
  const frag = document.createDocumentFragment();
  const text = passage.text;
  const sentences = sentencesOf.get(passage.id) ?? [];
  const markersOf = sentences.map(() => []);
  for (const h of hasiyeOf.get(passage.id) ?? []) {
    let i = sentences.findIndex((s) => h.offset <= s.e);      // işaret cümle sonundaki noktadan hemen sonra olabilir
    if (i < 0) i = sentences.length - 1;
    if (i >= 0) markersOf[i].push(h);
  }

  let pos = 0;
  sentences.forEach((s, i) => {
    if (s.s > pos) frag.append(text.slice(pos, s.s));
    const span = el("span", { class: "sentence", dataset: { id: s.id } });
    span.append(el("button", { type: "button", class: "snum", title: s.ref, onclick: () => onSentenceClick(s, span) }, String(s.n)));
    let cur = s.s;
    for (const h of markersOf[i]) {
      const at = Math.min(Math.max(h.offset, s.s), s.e);
      span.append(text.slice(cur, at), " ",
        el("button", { type: "button", class: "ref", onclick: () => onRefClick(h.label) }, `(${h.label})`));
      cur = at;
    }
    span.append(text.slice(cur, s.e));
    applyStatus(span, s.id);
    frag.append(span);
    pos = s.e;
  });
  if (pos < text.length) frag.append(text.slice(pos));
  return frag;
}

/** Seçilen cümlenin atfı, incipit'i, kimliği ve işaret düğmeleri. Aynı cümleye yeniden tıklanınca kapanır. */
function sentencePanel() {
  const panel = el("div", { class: "sentence-panel", hidden: "" });
  let current = null;
  return {
    panel,
    toggle(s, span) {
      current?.classList.remove("selected");
      if (current === span) {
        current = null;
        panel.hidden = true;
        return;
      }
      current = span;
      span.classList.add("selected");
      panel.replaceChildren(
        el("div", { class: "sentence-ref" }, s.ref),
        el("div", { class: "sentence-incipit" }, `“${s.incipit}…”`),
        el("code", {}, s.id),
        markControls(s.id, { container: span, context: { incipit: s.incipit, node: nodeIdOf(s.id) } }));
      panel.hidden = false;
    },
  };
}

const paragraphNumber = (passage) => Number(passage.id.match(/\/p(\d+)$/)[1]);

function renderHasiye(hasiye) {
  const name = hasiye.ref.split(" › ").pop();
  const nested = (hasiyeOf.get(hasiye.id) ?? []).map(renderHasiye);   // hâşiyenin hâşiyesi
  const { panel, toggle } = sentencePanel();
  const box = el("div", { class: "hasiye", dataset: { label: hasiye.label ?? "" } },
    el("div", { class: "hasiye-head" }, el("strong", {}, name)),
    el("div", { class: "ptext" }, renderSentences(hasiye, { onRefClick: (label) => flash(nested, label), onSentenceClick: toggle })),
    panel);
  box.append(markControls(hasiye.id, { container: box }), ...nested);
  return box;
}

function flash(hasiyeler, label) {
  const target = hasiyeler.find((h) => h.dataset.label === label) ?? hasiyeler[0];
  if (!target) return;
  target.scrollIntoView({ block: "nearest", behavior: "smooth" });
  target.classList.add("flash");
  setTimeout(() => target.classList.remove("flash"), 1200);
}

/** Ana cilde eşlenmiş paragraf: metin orada durur, burada yalnızca bağlantısı gösterilir. */
const canonicalLink = (paragraphId) => el("a", { href: `#${nodeIdOf(paragraphId) ?? workOf(paragraphId)}` }, paragraphId);

function renderSourcePassage(passage) {
  const links = passage.source.flatMap((pid, i) => (i ? [", ", canonicalLink(pid)] : [canonicalLink(pid)]));
  return el("article", { class: "passage source", id: passage.id },
    el("div", { class: "pnum" }, `¶${paragraphNumber(passage)}`),
    el("div", { class: "ptext" }, "Metni ana ciltte: ", ...links));
}

function renderPassage(passage) {
  if (passage.source) return renderSourcePassage(passage);
  const article = el("article", { class: `passage kind-${passage.kind}`, id: passage.id });
  const hasiyeler = (hasiyeOf.get(passage.id) ?? []).map(renderHasiye);
  const { panel, toggle } = sentencePanel();

  article.append(
    el("div", { class: "pnum" }, `¶${paragraphNumber(passage)}`),
    el("div", { class: "ptext" }, renderSentences(passage, { onRefClick: (label) => flash(hasiyeler, label), onSentenceClick: toggle })),
    panel,
    markControls(passage.id, { container: article }),
    ...hasiyeler);
  return article;
}

function renderBreadcrumb(id) {
  const group = DATA.groups.find((g) => g.id === works.get(workOf(id)).group);
  const nav = el("nav", { class: "breadcrumb" }, group.title);
  for (const anc of ancestors(id)) nav.append(el("span", { class: "sep" }, "›"), nodeLink(anc));
  nav.append(el("span", { class: "sep" }, "›"), nodes.get(id).title);
  return nav;
}

function renderHeader(id) {
  const node = nodes.get(id);
  const code = el("code", {}, id);
  const copyBtn = el("button", { type: "button" }, "Kimliği kopyala");
  copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(id);
      copyBtn.textContent = "Kopyalandı";
    } catch {
      getSelection().selectAllChildren(code);
      copyBtn.textContent = "Seçildi, Ctrl+C";
    }
    setTimeout(() => (copyBtn.textContent = "Kimliği kopyala"), 1500);
  });

  return el("header", { class: "node-head" },
    el("h2", {}, node.title),
    node.subtitle ? el("p", { class: "subtitle" }, node.subtitle) : null,
    node.sources ? el("p", { class: "node-sources" }, "Ana ciltteki karşılığı: ",
      ...node.sources.flatMap((source, i) => (i ? [", ", nodeLink(source, source)] : [nodeLink(source, source)]))) : null,
    el("div", { class: "node-id" }, code, copyBtn),
    el("div", { class: "node-review" },
      el("span", { class: "label" }, "Bu başlığın yeri ve adı:"),
      markControls(id)),
    ...(hasiyeOf.get(id) ?? []).map(renderHasiye));   // başlıktaki hâşiyeler
}

function renderChildren(id) {
  const kids = children(id);
  if (!kids.length) return null;
  return el("section", { class: "children" },
    el("h3", {}, "Alt bölümler"),
    el("ul", {}, ...kids.map((k) => el("li", {}, nodeLink(k)))));
}

function renderPager(id) {
  const i = order.indexOf(id);
  const prev = order[i - 1];
  const next = order[i + 1];
  return el("nav", { class: "pager" },
    prev ? el("a", { class: "prev", href: `#${prev}` }, `‹ ${nodes.get(prev).title}`) : null,
    next ? el("a", { class: "next", href: `#${next}` }, `${nodes.get(next).title} ›`) : null);
}

function showNode(id) {
  const work = works.get(workOf(id));
  const passages = ownPassages(id);
  const inner = el("div", { class: "content-inner" },
    renderBreadcrumb(id),
    renderHeader(id),
    passages.length
      ? el("section", { class: "passages" }, ...passages.map(renderPassage))
      : el("p", { class: "empty" }, "Bu başlığın kendine ait paragrafı yok; metin alt bölümlerinde."),
    renderChildren(id),
    renderPager(id));
  document.body.classList.toggle("lang-ar", work.language === "ar");
  contentEl.replaceChildren(inner);
  contentEl.scrollTop = 0;
  revealInTree(id);
  document.title = `${nodes.get(id).title} · ${work.title} · ${DATA.title}`;
}

function showMessage(...lines) {
  contentEl.replaceChildren(el("div", { class: "welcome" }, ...lines));
}

function showWelcome() {
  document.body.classList.remove("lang-ar");
  const total = (key) => DATA.works.reduce((sum, w) => sum + w.counts[key], 0);
  showMessage(
    el("h2", {}, DATA.title),
    el("p", {}, "Soldaki ağaçtan bir eser ya da başlık seçin. ← / → tuşlarıyla kitap sırasında gezinebilirsiniz."),
    el("p", {}, `${DATA.works.length} eser · ${total("nodes")} başlık · ${total("passages")} paragraf · ${total("sentences")} cümle`),
    el("p", {}, "Cümlenin başındaki küçük numaraya tıklayınca o cümlenin atfı ve işaret düğmeleri açılır."));
  document.title = DATA.title;
}

// ------------------------------------------------------------------ gezinme

function navigate(id) {
  location.hash = id;
}

async function route() {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!nodes.has(id)) {
    showWelcome();
    return;
  }
  const slug = workOf(id);
  if (!sentencesOfWork.has(slug)) showMessage(el("p", {}, `${works.get(slug).title} yükleniyor…`));
  try {
    await loadWork(slug);
  } catch (err) {
    showMessage(el("p", {}, err.message));
    return;
  }
  if (decodeURIComponent(location.hash.slice(1)) === id) showNode(id);   // bu arada başka başlık seçilmediyse
}

function onKeydown(event) {
  const typing = event.target instanceof Element && event.target.closest("input, textarea");
  if (typing || event.altKey || event.ctrlKey || event.metaKey) return;
  const current = decodeURIComponent(location.hash.slice(1));
  const i = order.indexOf(current);
  if (event.key === "ArrowRight" && i < order.length - 1) navigate(order[i + 1]);
  if (event.key === "ArrowLeft" && i > 0) navigate(order[i - 1]);
}

// ------------------------------------------------------------------ dışa / içe aktarma

/** Bütün eserlerin işaretleri tek dosyada; her kayıt eserini taşır. Atıf ve türün doğru çıkması
 * için işaretli eserlerin metni önce yüklenir. */
async function exportMarks() {
  const marked = [...new Set([...Marks.entries()].map(([, , slug]) => slug))];
  await Promise.allSettled(marked.map(loadWork));
  const items = [...Marks.entries()].map(([id, mark, book]) => ({
    book,
    id,
    target: targetKind(id),
    ref: refOf(id),
    incipit: mark.incipit ?? null,
    status: mark.status,
    note: mark.note,
  }));
  const position = (item) => order.indexOf(nodeIdOf(item.id) ?? item.book);
  items.sort((a, b) => position(a) - position(b));

  const payload = { exported_at: new Date().toISOString(), books: marked, items };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const link = el("a", { href: URL.createObjectURL(blob), download: "risale-kontrol-notlari.json" });
  link.click();
  URL.revokeObjectURL(link.href);
}

/** Bu dosyayı da, eski eser başına dosyaları da ({book, items}) okur. */
async function importMarks(event) {
  const file = event.target.files[0];
  if (!file) return;
  try {
    const payload = JSON.parse(await file.text());
    for (const item of payload.items ?? []) {
      const context = item.incipit ? { incipit: item.incipit, node: nodeIdOf(item.id) ?? undefined } : {};
      Marks.update(item.id, { ...context, status: item.status ?? null, note: item.note ?? "" });
    }
    for (const slug of sentencesOfWork.keys()) Marks.reanchor(slug);
    onMarksChanged();
    route();
  } catch (err) {
    console.error("İçe aktarılamadı:", err);
  }
  event.target.value = "";
}

// ------------------------------------------------------------------ başlat

Marks.load();
treeEl.append(buildTree());
treeEl.addEventListener("click", onTreeClick);
document.getElementById("search").addEventListener("input", (e) => applySearch(e.target.value));
document.getElementById("export").addEventListener("click", exportMarks);
document.getElementById("import").addEventListener("change", importMarks);
window.addEventListener("hashchange", route);
document.addEventListener("keydown", onKeydown);
onMarksChanged();
route();
