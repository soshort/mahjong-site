// Живая витрина сайта: мини-маджонг с полкой (как дуэль с Мажобэ в игре),
// глаза Мажобэ (следят за курсором, пальцем и тапами), падающие тайлы на
// первом экране и появление блоков при прокрутке. Без библиотек; при
// «меньше движения» в системе — без падающих тайлов и плавных появлений.
(() => {
  "use strict";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const tileUrl = (n) => `/img/tile/${n}.webp`;
  const rand = (a, b) => a + Math.random() * (b - a);
  const heads = [];

  // --- Глаза Мажобэ -----------------------------------------------------------
  // Голова — картинка watch_head; белки — доли её размера [cx, cy, rx, ry]
  // (манифест игры watch.json); зрачки — круги, бегут к точке взгляда.
  const PUPIL_SHARE = 0.62;
  function makeHead(el, eyes) {
    const pupils = eyes.map(() => {
      const p = document.createElement("i");
      p.className = "pupil";
      el.appendChild(p);
      return p;
    });
    const head = { el, eyes, pupils, look: null };
    head.layout = () => {
      const w = el.clientWidth, h = el.clientHeight;
      eyes.forEach(([cx, cy, rx, ry], i) => {
        const r = Math.min(rx * w, ry * h) * PUPIL_SHARE;
        const s = pupils[i].style;
        s.width = s.height = `${2 * r}px`;
        s.left = `${cx * w - r}px`;
        s.top = `${cy * h - r}px`;
      });
      if (head.look) lookAt(head, head.look[0], head.look[1]);
    };
    heads.push(head);
    head.layout();
    return head;
  }
  function lookAt(head, x, y) {
    head.look = [x, y];
    const box = head.el.getBoundingClientRect();
    const w = box.width, h = box.height;
    head.eyes.forEach(([cx, cy, rx, ry], i) => {
      const r = Math.min(rx * w, ry * h) * PUPIL_SHARE;
      const mx = rx * w - r * 0.92, my = ry * h - r * 0.92;
      let dx = x - (box.left + cx * w), dy = y - (box.top + cy * h);
      const len = Math.hypot(dx / mx, dy / my);
      const k = len > 1 ? 1 / len : 1;
      // Далёкая точка — до края белка; близкая — пропорционально.
      const near = Math.min(1, Math.hypot(dx, dy) / (w * 0.6));
      dx *= k * near; dy *= k * near;
      head.pupils[i].style.transform = `translate(${dx}px, ${dy}px)`;
    });
  }
  const lookAll = (x, y) => heads.forEach((h) => lookAt(h, x, y));
  addEventListener("pointermove", (e) => lookAll(e.clientX, e.clientY), { passive: true });
  addEventListener("pointerdown", (e) => lookAll(e.clientX, e.clientY), { passive: true });
  addEventListener("resize", () => heads.forEach((h) => h.layout()));
  // Без мыши (телефон) — глаза бегают сами, пока нет касаний.
  let lastMove = 0;
  addEventListener("pointermove", () => { lastMove = performance.now(); }, { passive: true });
  setInterval(() => {
    if (performance.now() - lastMove < 2500) return;
    heads.forEach((h) => {
      const b = h.el.getBoundingClientRect();
      lookAt(h, b.left + rand(-0.3, 1.3) * b.width, b.top + rand(0.6, 2.4) * b.height);
    });
  }, 1600);
  // Кнопки Google Play: Мажобэ смотрит на кнопку и оживляется.
  document.querySelectorAll("a.play").forEach((a) => {
    a.addEventListener("pointerenter", () => heads.forEach((h) => h.el.classList.add("perk")));
    a.addEventListener("pointerleave", () => heads.forEach((h) => h.el.classList.remove("perk")));
  });
  document.querySelectorAll(".mz-head").forEach((el) => makeHead(el, JSON.parse(el.dataset.eyes)));

  // --- Мини-маджонг -----------------------------------------------------------
  // 12 тайлов в два слоя: 4×2 снизу, ещё два снизу во втором ряду и два
  // сверху, каждый закрывает по четыре. Свободен тайл, который никто не
  // накрывает. Тап — тайл на полку (4 места), две одинаковые — пара
  // исчезает; четыре разных — проигрыш; поле пусто — чёрная дыра и победа.
  const root = document.getElementById("demo");
  if (root) demo(root, JSON.parse(root.dataset.demo));

  function demo(el, cfg) {
    // Раскладка: [колонка, ряд, слой, номер иконки в cfg.icons].
    const LAYOUT = [
      [0.5, 0.5, 1, 0], [2.5, 0.5, 1, 1],
      [1, 2, 0, 2], [2, 2, 0, 0],
      [0, 0, 0, 1], [1, 0, 0, 3], [0, 1, 0, 4], [1, 1, 0, 2],
      [2, 0, 0, 3], [3, 0, 0, 5], [2, 1, 0, 4], [3, 1, 0, 5],
    ];
    const SLOTS = 4;
    el.innerHTML = `
      <div class="d-top"><img class="d-shop" src="/img/watch_shop.webp" alt="">
        <div class="d-head mz-head"><img src="/img/watch_head.webp" alt=""></div></div>
      <div class="d-pole">${[1, 2, 3, 4].map((n) => `<b>${n}</b>`).join("")}</div>
      <div class="d-field"></div>
      <div class="d-hint">${cfg.hint}</div>
      <div class="d-msg" hidden><h3></h3><p></p>
        <a class="play small" href="${document.querySelector("a.play").href}">${document.querySelector("a.play").innerHTML}</a>
        <button type="button" class="again">${cfg.again}</button></div>`;
    const head = makeHead(el.querySelector(".d-head"), cfg.eyes);
    const field = el.querySelector(".d-field");
    const pole = el.querySelector(".d-pole");
    const msg = el.querySelector(".d-msg");
    const hint = el.querySelector(".d-hint");
    msg.querySelector(".again").addEventListener("click", start);
    let tiles = [], shelf = [], busy = 0, over = false;

    function geom() {
      const W = el.clientWidth;
      const tw = W / 5.6, th = tw * 1.24;
      const fieldTop = pole.offsetTop + pole.offsetHeight;
      const ox = (W - 4 * tw) / 2 + tw * 0.04, oy = fieldTop + tw * 0.42;
      const sw = W / SLOTS * 0.66, sh = sw * 1.24;
      return { W, tw, th, ox, oy, sw, sh, lift: tw * 0.09, shelfY: pole.offsetTop - sh * 0.86 };
    }
    function fieldRect(t, g) {
      return { x: g.ox + t.c * g.tw - t.l * g.lift, y: g.oy + t.r * g.th - t.l * g.lift, w: g.tw, h: g.th };
    }
    function slotRect(i, g) {
      const step = g.W / SLOTS;
      return { x: step * i + (step - g.sw) / 2, y: g.shelfY, w: g.sw, h: g.sh };
    }
    function place(t, r) {
      const s = t.el.style;
      s.left = `${r.x}px`; s.top = `${r.y}px`; s.width = `${r.w}px`; s.height = `${r.h}px`;
    }
    function covered(t) {
      return tiles.some((o) => o.on === "field" && o.l > t.l && Math.abs(o.c - t.c) < 1 && Math.abs(o.r - t.r) < 1);
    }
    function refresh() {
      const g = geom();
      tiles.forEach((t) => {
        if (t.on === "field") { place(t, fieldRect(t, g)); t.el.classList.toggle("blocked", covered(t)); }
      });
      shelf.forEach((t, i) => place(t, slotRect(i, g)));
    }
    function start() {
      field.querySelectorAll(".tile").forEach((n) => n.remove());
      el.querySelectorAll(".tile, .shard, .hole").forEach((n) => n.remove());
      msg.hidden = true; over = false; busy = 0; shelf = [];
      el.classList.remove("won", "lost");
      head.el.classList.remove("laugh");
      // Иконки — свои на каждый заход (пары те же по раскладке).
      const icons = [...cfg.icons].sort(() => Math.random() - 0.5);
      tiles = LAYOUT.map(([c, r, l, k], i) => {
        const t = { c, r, l, icon: icons[k], on: "field", el: document.createElement("button") };
        t.el.type = "button";
        t.el.className = "tile";
        // Слой — главнее порядка: верхний тайл всегда рисуется поверх
        // нижних (иначе последний нижний вставал вровень с верхним).
        t.el.style.zIndex = 10 + l * 50 + i;
        t.el.dataset.layer = l;
        t.el.innerHTML = `<img src="${tileUrl(t.icon)}" alt="" draggable="false">`;
        t.el.addEventListener("click", () => tap(t));
        el.appendChild(t.el);
        return t;
      });
      refresh();
      if (!reduce) tiles.forEach((t, i) => {
        t.el.animate([{ transform: "translateY(-40px) scale(.7)", opacity: 0 }, { transform: "none", opacity: 1 }],
          { duration: 380, delay: 40 * i, easing: "cubic-bezier(.2,.9,.3,1.2)", fill: "backwards" });
      });
    }
    function tap(t) {
      if (over || t.on !== "field" || covered(t) || shelf.length >= SLOTS) return;
      hint.classList.add("gone");
      const b = t.el.getBoundingClientRect();
      lookAt(head, b.left + b.width / 2, b.top + b.height / 2);
      t.on = "shelf";
      shelf.push(t);
      t.el.classList.remove("blocked");
      t.el.classList.add("flying");
      t.el.style.zIndex = 200 + shelf.length;
      busy++;
      refresh();
      setTimeout(() => { t.el.classList.remove("flying"); busy--; land(t); }, reduce ? 0 : 330);
    }
    function land(t) {
      const twin = shelf.find((o) => o !== t && o.icon === t.icon);
      if (twin) {
        const left = tiles.filter((o) => o.on === "field").length;
        shelf = shelf.filter((o) => o !== t && o !== twin);
        t.on = twin.on = "gone";
        if (left === 0 && shelf.length === 0) return finale([twin, t]);
        burst([twin, t]);
        setTimeout(refresh, 160);
        return;
      }
      if (shelf.length >= SLOTS && busy === 0) lose();
    }
    function burst(pair) {
      head.el.classList.remove("nod"); void head.el.offsetWidth; head.el.classList.add("nod");
      pair.forEach((t) => {
        t.el.classList.add("pop");
        shards(t.el.getBoundingClientRect(), 9);
        setTimeout(() => t.el.remove(), 320);
      });
    }
    function shards(r, n) {
      if (reduce) return;
      const box = el.getBoundingClientRect();
      for (let i = 0; i < n; i++) {
        const s = document.createElement("i");
        s.className = "shard";
        s.style.left = `${r.left - box.left + r.width / 2}px`;
        s.style.top = `${r.top - box.top + r.height / 2}px`;
        el.appendChild(s);
        const a = rand(0, Math.PI * 2), d = rand(30, 90);
        s.animate([{ transform: "translate(-50%,-50%) rotate(0)", opacity: 1 },
          { transform: `translate(${Math.cos(a) * d - 5}px, ${Math.sin(a) * d - 5 + 30}px) rotate(${rand(-300, 300)}deg)`, opacity: 0 }],
          { duration: rand(450, 700), easing: "cubic-bezier(.2,.7,.4,1)" }).onfinish = () => s.remove();
      }
    }
    // Последняя пара — чёрная дыра посреди поля: тайлы закручивает в неё.
    function finale(pair) {
      over = true;
      const g = geom();
      const hole = document.createElement("i");
      hole.className = "hole";
      hole.style.left = `${g.W / 2}px`;
      hole.style.top = `${g.oy + g.th * 1.4}px`;
      el.appendChild(hole);
      const hb = { x: g.W / 2, y: g.oy + g.th * 1.4 };
      pair.forEach((t, i) => {
        const x = parseFloat(t.el.style.left) + parseFloat(t.el.style.width) / 2;
        const y = parseFloat(t.el.style.top) + parseFloat(t.el.style.height) / 2;
        t.el.animate([{ transform: "none" },
          { transform: `translate(${(hb.x - x) * 0.55}px, ${(hb.y - y) * 0.5 - 30}px) rotate(${i ? 200 : -200}deg) scale(.8)`, offset: 0.55 },
          { transform: `translate(${hb.x - x}px, ${hb.y - y}px) rotate(${i ? 540 : -540}deg) scale(0)` }],
          { duration: reduce ? 10 : 1100, easing: "cubic-bezier(.5,0,.75,0)", fill: "forwards" });
      });
      setTimeout(() => {
        hole.classList.add("close");
        pair.forEach((t) => t.el.remove());
        el.classList.add("won");
        show(cfg.win, cfg.win_text, true);
      }, reduce ? 50 : 1300);
    }
    function lose() {
      over = true;
      el.classList.add("lost");
      head.el.classList.add("laugh");
      setTimeout(() => show(cfg.lose, cfg.lose_text, false), 500);
    }
    function show(title, text, won) {
      msg.querySelector("h3").textContent = title;
      msg.querySelector("p").textContent = text;
      msg.querySelector(".play").hidden = !won;
      msg.hidden = false;
    }
    // Ширина блока меняется не только с окном (шрифты, сетка первого
    // экрана) — раскладка и глаза следят за самим блоком.
    new ResizeObserver(() => { refresh(); head.layout(); }).observe(el);
    start();
  }

  // --- Падающие тайлы ---------------------------------------------------------
  const rain = document.querySelector(".rain");
  if (rain && !reduce) {
    const icons = JSON.parse(rain.dataset.icons);
    const count = innerWidth < 700 ? 7 : 12;
    for (let i = 0; i < count; i++) {
      const d = document.createElement("i");
      d.className = "drop";
      const size = rand(34, 64);
      d.style.width = `${size}px`; d.style.height = `${size * 1.24}px`;
      d.style.left = `${rand(0, 100)}%`;
      d.style.opacity = rand(0.10, 0.22).toFixed(2);
      d.innerHTML = `<img src="${tileUrl(icons[i % icons.length])}" alt="">`;
      d.style.animationDuration = `${rand(14, 26).toFixed(1)}s`;
      d.style.animationDelay = `${-rand(0, 26).toFixed(1)}s`;
      d.style.setProperty("--spin", `${rand(-200, 200).toFixed(0)}deg`);
      rain.appendChild(d);
    }
  }

  // --- Выбор языка ----------------------------------------------------------------
  // Список языков (<details>) закрывается кликом мимо него и клавишей Esc.
  const closeLangs = (except) => document.querySelectorAll("details.langs[open]").forEach((d) => {
    if (d !== except) d.removeAttribute("open");
  });
  document.addEventListener("click", (e) => closeLangs(e.target.closest("details.langs")));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeLangs(null); });

  // --- Появление при прокрутке ------------------------------------------------
  const blocks = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    blocks.forEach((b) => b.classList.add("in"));
  } else {
    const io = new IntersectionObserver((list) => list.forEach((x) => {
      if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    blocks.forEach((b, i) => { b.style.transitionDelay = `${(i % 3) * 90}ms`; io.observe(b); });
  }
})();
