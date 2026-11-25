// S12.3: sohbet sayfası. Konuşma yalnız bu tarayıcıda (localStorage) durur; her soruda önceki sorular ve cevapların
// ham metni (cümle kimliği işaretleriyle) sunucuya yeniden gönderilir. Cevap Server-Sent Events ile akar.
"use strict";

const P = document.body.dataset.prefix;
const KEY = "sohbet:konusma";
const $ = (id) => document.getElementById(id);
const els = { list: $("konusma"), empty: $("bos"), form: $("soru-formu"), input: $("soru"), send: $("gonder"),
  fresh: $("yeni"), dialog: $("metin"), dpath: $("metin-yol"), dbody: $("metin-govde"), dclose: $("metin-kapat") };

let turns = load();
let busy = false;

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}
function save() {
  try { localStorage.setItem(KEY, JSON.stringify(turns)); } catch { /* dolu ya da kapalı: konuşma yalnız sayfada */ }
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
      return `<button type="button" class="ref${bad}" data-n="${n}" title="${esc(src.cite_as || "Adresi bulunamadı")}">[${n}]</button>`;
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

// ------------------------------------------------------------ görünüm

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function renderSources(box, sources) {
  if (!sources || !sources.length) return;
  const wrap = el("div", "kaynaklar");
  wrap.append(el("h4", "", "Kaynaklar"));
  const ol = el("ol");
  for (const s of sources) {
    const li = el("li");
    const b = el("button", "kaynak" + (s.problem ? " kotu" : ""));
    b.type = "button";
    b.dataset.n = s.n;
    b.innerHTML = `<span class="no">[${s.n}]</span><span class="yol-metin">${esc(s.cite_as || "Adresi bulunamadı")}</span>`;
    li.append(b);
    for (const e of s.embedded || []) li.append(el("div", "gomulu", "– " + esc(e.line)));
    if (s.problem) li.append(el("div", "uyari", "⚠ Bu alıntı eserlerin metniyle doğrulanamadı."));
    ol.append(li);
  }
  wrap.append(ol);
  box.append(wrap);
}

function renderTurn(turn) {
  const box = el("section", "tur");
  box.append(el("div", "soru-balon", esc(turn.q)));
  const answer = el("div", "cevap");
  box.append(answer);
  if (turn.markdown) {
    const refs = new Map((turn.sources || []).map((s) => [s.n, s]));
    answer.innerHTML = markdown(turn.markdown, refs);
    renderSources(box, turn.sources);
    if (turn.corrected) box.append(el("p", "alt-bilgi", "Alıntılar denetimde düzeltildi."));
  }
  box._turn = turn;
  return box;
}

function renderAll() {
  els.list.innerHTML = "";
  for (const t of turns) els.list.append(renderTurn(t));
  els.empty.hidden = turns.length > 0;
}

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
  const src = sourceOf(box, target.dataset.n);
  if (src) openText(src);
});

// ------------------------------------------------------------ metin penceresi

async function openText(src) {
  els.dpath.textContent = src.cite_as || "Adresi bulunamadı";
  els.dbody.innerHTML = '<p class="small">Yükleniyor…</p>';
  if (!els.dialog.open) els.dialog.showModal();
  try {
    const r = await fetch(`${P}api/metin?id=${encodeURIComponent(src.id)}`, { credentials: "same-origin" });
    if (!r.ok) throw new Error((await r.json()).error || "Metin açılamadı.");
    const data = await r.json();
    els.dpath.textContent = data.section_ref || src.cite_as || "Adresi bulunamadı";
    const parts = [];
    if (src.unverified) parts.push('<p class="uyari">⚠ Alıntının sözleri bu cümlelerde ve eserlerin başka bir yerinde bulunamadı; cevabın gösterdiği yer bu.</p>');
    for (const s of data.sentences || []) {
      const body = esc(s.text);
      parts.push(`<p class="cumle" dir="auto">${s.target ? `<mark>${body}</mark>` : body}</p>`);
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
    const first = els.dbody.querySelector("mark");
    if (first) first.scrollIntoView({ block: "center" });
  } catch (e) {
    els.dbody.innerHTML = `<p class="hata">${esc(e.message)}</p>`;
  }
}
els.dclose.addEventListener("click", () => els.dialog.close());
els.dialog.addEventListener("click", (ev) => { if (ev.target === els.dialog) els.dialog.close(); });

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
  const turn = { q: question.trim() };
  const box = renderTurn(turn);
  els.list.append(box);
  const answer = box.querySelector(".cevap");
  const status = el("div", "durum", "Soru gönderiliyor…");
  box.insertBefore(status, answer);
  box.scrollIntoView({ block: "start", behavior: "smooth" });

  let draft = "";
  let frame = 0;
  const paint = () => { frame = 0; answer.innerHTML = markdown(draft, null); };
  const history = turns.map((t) => ({ q: t.q, a: t.a }));
  let finished = false;

  const handle = (event, data) => {
    if (event === "status") { status.textContent = data.text; status.hidden = false; }
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
      Object.assign(turn, { a: data.raw, markdown: data.markdown, sources: data.sources, corrected: data.corrected });
      turns.push(turn);
      save();
      const fresh = renderTurn(turn);
      box.replaceWith(fresh);
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
      body: JSON.stringify({ question: turn.q, history }),
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
for (const b of document.querySelectorAll(".ornek")) b.addEventListener("click", () => ask(b.textContent));
els.fresh.addEventListener("click", () => {
  if (busy) return;
  turns = []; save(); renderAll(); els.input.focus();
});

renderAll();
