// Ana sayfa: talimat kutusu (metni ayrı dosyadan okur, kopyalar) ve iki cevabın yazılıyormuş gibi karşılaştırması.
// Betik çalışmazsa sayfa yine okunur: talimatın bağlantısı durur, karşılaştırmada cevaplar baştan görünür.

// Görünüm: tarayıcının ayarına uyar; düğme öbürünü seçer ve hatırlanır (sayfa başındaki satır, çizimden önce uygular).
for (const button of document.querySelectorAll("[data-theme-toggle]")) {
  button.addEventListener("click", () => {
    const root = document.documentElement;
    const current = root.dataset.theme || (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    const next = current === "light" ? "dark" : "light";
    root.dataset.theme = next;
    try {
      localStorage.setItem("theme", next);
    } catch {}
  });
}

// Talimat: <div class="copybox" data-src="/talimat.md"> içine metni yükler, düğme panoya kopyalar.
for (const box of document.querySelectorAll(".copybox[data-src]")) {
  const pre = box.querySelector("pre");
  const button = box.querySelector("button");
  fetch(box.dataset.src)
    .then((r) => (r.ok ? r.text() : Promise.reject(r.status)))
    .then((text) => {
      pre.textContent = text.trim();
      button.hidden = false;
    })
    .catch(() => {});
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(pre.textContent);
    } catch {
      const range = document.createRange();
      range.selectNodeContents(pre);
      getSelection().removeAllRanges();
      getSelection().addRange(range);
      document.execCommand("copy");
    }
    const label = button.textContent;
    button.textContent = button.dataset.done;
    setTimeout(() => (button.textContent = label), 1800);
  });
}

// Kısa değerler: <button data-copy="…"> değeri panoya kopyalar (ChatGPT'de ad ve adres elle yazılır).
for (const button of document.querySelectorAll("button[data-copy]")) {
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
    } catch {
      return;
    }
    const label = button.textContent;
    button.textContent = button.dataset.done;
    setTimeout(() => (button.textContent = label), 1800);
  });
}

// Karşılaştırma: iki cevap aynı anda yazılır; sağda önce araç adımları sırayla tamamlanır.
const WORDS_PER_SECOND = 40;
const STEP_MS = 650;
const BLOCKS = "p, li, ul, ol, blockquote, h3, h4, pre, table, hr";

const cmp = document.querySelector("[data-cmp]");
if (cmp) setupCompare(cmp);

function setupCompare(root) {
  const panels = [...root.querySelectorAll(".cmp-panel")];
  const tabs = [...root.querySelectorAll(".cmp-tabs button")];
  let userPicked = false;

  function show(side) {
    for (const p of panels) p.classList.toggle("active", p.dataset.side === side);
    for (const t of tabs) t.setAttribute("aria-selected", t.dataset.side === side);
  }
  for (const t of tabs)
    t.addEventListener("click", () => {
      userPicked = true;
      show(t.dataset.side);
    });
  show("off");

  if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
    root.classList.add("done");
    return;
  }

  // Her kelime bir <span class="w">; blok, ilk kelimesi görünene kadar yer kaplamaz.
  const tracks = panels.map((panel) => {
    const answer = panel.querySelector(".answer");
    const words = [];
    const walker = document.createTreeWalker(answer, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      if (!node.textContent.trim()) continue;
      const frag = document.createDocumentFragment();
      for (const part of node.textContent.split(/(\s+)/)) {
        if (!part) continue;
        if (/^\s+$/.test(part)) frag.append(part);
        else {
          const span = document.createElement("span");
          span.className = "w";
          span.textContent = part;
          frag.append(span);
          words.push(span);
        }
      }
      node.replaceWith(frag);
    }
    return {
      panel,
      body: panel.querySelector(".cmp-body"),
      answer,
      words,
      steps: [...panel.querySelectorAll(".tool-steps li")],
    };
  });

  let frame = 0;
  let timers = [];

  function reset() {
    cancelAnimationFrame(frame);
    timers.forEach(clearTimeout);
    timers = [];
    root.classList.remove("done");
    root.classList.add("playing");
    for (const t of tracks) {
      t.body.scrollTop = 0;
      for (const el of t.answer.querySelectorAll(BLOCKS)) el.classList.add("pending");
      t.answer.classList.add("pending");
      for (const w of t.words) w.classList.remove("on");
      for (const s of t.steps) {
        s.classList.add("pending");
        s.classList.remove("run");
      }
    }
  }

  function play() {
    reset();
    const starts = tracks.map((t) => {
      // Araç adımları sırayla dönüp tamamlanır; cevap en son adımdan sonra başlar.
      t.steps.forEach((s, i) => {
        timers.push(setTimeout(() => s.classList.remove("pending"), 400 + i * STEP_MS));
        timers.push(setTimeout(() => s.classList.add("run"), 400 + i * STEP_MS));
        timers.push(setTimeout(() => s.classList.remove("run"), 400 + (i + 1) * STEP_MS));
      });
      return 700 + t.steps.length * STEP_MS;
    });
    const t0 = performance.now();
    const shown = tracks.map(() => 0);
    const finished = tracks.map(() => false);

    function tick(now) {
      tracks.forEach((t, i) => {
        if (finished[i]) return;
        const elapsed = now - t0 - starts[i];
        if (elapsed < 0) return;
        t.answer.classList.remove("pending");
        const target = Math.min(t.words.length, Math.floor((elapsed / 1000) * WORDS_PER_SECOND));
        for (; shown[i] < target; shown[i]++) {
          const w = t.words[shown[i]];
          w.classList.add("on");
          for (let el = w.parentElement; el && el !== t.answer; el = el.parentElement) el.classList.remove("pending");
        }
        t.body.scrollTop = t.body.scrollHeight;
        if (shown[i] >= t.words.length) {
          finished[i] = true;
          // Bağlayıcısız cevap önce biter: kullanıcı sekme seçmediyse telefonda öbür cevaba geçilir.
          if (t.panel.dataset.side === "off" && !userPicked) show("on");
        }
      });
      if (finished.every(Boolean)) {
        root.classList.remove("playing");
        root.classList.add("done");
        for (const t of tracks) t.body.scrollTop = 0;
      } else frame = requestAnimationFrame(tick);
    }
    frame = requestAnimationFrame(tick);
  }

  root.querySelector("[data-replay]").addEventListener("click", () => {
    userPicked = false;
    show("off");
    play();
  });

  // Bölüm ekrana girince bir kez başlar; o zamana kadar cevaplar gizli bekler.
  reset();
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        observer.disconnect();
        play();
      }
    },
    { threshold: 0.3 },
  );
  observer.observe(root);
}
