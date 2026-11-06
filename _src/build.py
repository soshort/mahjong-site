#!/usr/bin/env python3
"""Сборка сайта игры: главная и «Как играть» на всех языках игры, sitemap.xml
и картинки из репозитория игры. GitHub Pages папки с «_» не публикует —
этот файл на сайт не попадает.

    python3 _src/build.py            — страницы и sitemap
    python3 _src/build.py --assets   — ещё и картинки из игры (img/)

Тексты — _src/i18n/<код>.json (en, ru — оригинал; остальные — переводы,
названия режимов и кнопок — из строк игры и её страницы в Play). Пути:
en — «/», остальные — «/<код>/». Политика и удаление данных — только en и
ru (privacy.html, delete.html, ru/…), правятся руками; остальные языки
ссылаются на английские. Скриншоты — кадры без подписи из
mobile/store/screenshots/raw (tools/store_shots.gd … raw), en и ru.
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

SITE = "https://mahjong.stepanz.dev"
PLAY = "https://play.google.com/store/apps/details?id=dev.stepanz.mahjong"
YT = "HvKxJ-6F2d4"
ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT.parent / "mahjong"
HOWTO_FILE = "how-to-play.html"
DATE = "2026-11-06"
# Иконки мини-игры (пары) и падающих тайлов — номера в атласе игры
# (shared/tiles/icons.png, tiles.json).
DEMO_ICONS = [63, 79, 77, 68, 50, 49]
RAIN_ICONS = [11, 12, 8, 18, 64, 84, 59, 41, 23, 21, 30, 93]
SHOTS = ["finisher", "duel", "mazhobe", "play", "mechanics", "daily"]
PLAY_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" '
             'd="M4 3.5v17a1 1 0 0 0 1.5.86l14-8.5a1 1 0 0 0 0-1.72l-14-8.5A1 1 0 0 0 4 3.5z"/></svg>')
e = html.escape


def load() -> dict:
    """Языки: en и ru первыми, остальные — по коду."""
    files = {p.stem: json.loads(p.read_text()) for p in (ROOT / "_src/i18n").glob("*.json")}
    order = ["en", "ru"] + sorted(k for k in files if k not in ("en", "ru"))
    return {k: files[k] for k in order}


L = load()


def path(lang: str, file: str = "") -> str:
    return ("/" if lang == "en" else f"/{lang}/") + file


def doc_path(lang: str, file: str) -> str:
    """Политика и удаление — есть только en и ru."""
    return path("ru" if lang == "ru" else "en", file)


def play_url(lang: str) -> str:
    return f"{PLAY}&hl={L[lang]['play_hl']}"


def ver(name: str) -> str:
    """Метка версии файла в ссылке (?v=…): GitHub Pages разрешает кешировать
    10 минут, и браузер держал старый style.css при новой странице."""
    return hashlib.sha1((ROOT / name).read_bytes()).hexdigest()[:8]


def alternates(file: str) -> str:
    links = [f'<link rel="alternate" hreflang="{d["hreflang"]}" href="{SITE}{path(k, file)}">' for k, d in L.items()]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{path("en", file)}">')
    return "\n".join(links)


def lang_menu(lang: str, file: str) -> str:
    """Выбор языка: свёрнутый список без скриптов."""
    items = "".join(f'<a href="{path(k, file)}" hreflang="{d["hreflang"]}" lang="{d["hreflang"]}"'
                    f'{" aria-current=\"page\"" if k == lang else ""}>{e(d["native"])}</a>' for k, d in L.items())
    return (f'<details class="langs"><summary>{e(L[lang]["native"])}</summary>'
            f'<div class="langs-list">{items}</div></details>')


def head(lang: str, file: str, title: str, desc: str, og_type: str, extra: str) -> str:
    """Общая «голова» страницы.
    Параметры: язык и файл — адрес, заголовок и описание — сниппет, тип OG и
    разметка — что за страница."""
    url = SITE + path(lang, file)
    return f'''<!doctype html>
<html lang="{L[lang]['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{alternates(file)}
<link rel="icon" href="/icon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#17120d">
<link rel="preload" href="/fonts/philosopher.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/feature.jpg">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="500">
<meta property="og:locale" content="{L[lang]['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css?v={ver('style.css')}">
<script>document.documentElement.classList.add("js")</script>
{extra}
</head>
<body>
<header class="top">
  <a class="brand" href="{path(lang)}"><img src="/icon.png" alt="" width="36" height="36">Mazhobe</a>
  {lang_menu(lang, file)}
</header>'''


def ld(data: dict) -> str:
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def footer(lang: str) -> str:
    m, u = L[lang]["main"], L[lang]["ui"]
    return f'''<footer class="wrap">
  <a href="{path(lang, HOWTO_FILE)}">{e(u['howto_link'])}</a> · <a href="{doc_path(lang, 'privacy.html')}">{e(m['privacy'])}</a> · <a href="{doc_path(lang, 'delete.html')}">{e(m['delete'])}</a> · <span class="contact">{e(m['contact'])}: <a href="mailto:stepanz.dev@gmail.com">stepanz.dev@gmail.com</a></span>
</footer>'''


def play_button(lang: str) -> str:
    return f'<a class="play" href="{play_url(lang)}">{PLAY_ICON}{e(L[lang]["main"]["cta"])}</a>'


def page(lang: str) -> str:
    d = L[lang]
    m, shots = d["main"], d["shots"]
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": m["h1"],
           "alternateName": "Mazhobe Mahjong", "operatingSystem": "Android", "applicationCategory": "GameApplication",
           "description": m["desc"], "url": SITE + path(lang), "image": SITE + "/img/feature.jpg",
           "inLanguage": d["hreflang"], "installUrl": play_url(lang),
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "sameAs": [PLAY, "https://youtu.be/" + YT], "author": {"@type": "Person", "name": "Stepan Z"},
           "screenshot": [f"{SITE}/img/{shots}-{k}.webp" for k in SHOTS]}
    video = {"@context": "https://schema.org", "@type": "VideoObject", "name": m["video_name"],
             "description": m["desc"], "thumbnailUrl": SITE + "/img/trailer.jpg", "uploadDate": "2026-11-05",
             "duration": "PT36S", "embedUrl": f"https://www.youtube.com/embed/{YT}",
             "contentUrl": f"https://www.youtube.com/watch?v={YT}"}
    faq = d["faq"]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq["items"]]}
    faq_html = "\n".join(f"      <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq["items"])
    eyes = (ROOT / "_src/eyes.json").read_text()
    demo = json.dumps({**m["demo"], "icons": DEMO_ICONS, "eyes": json.loads(eyes)}, ensure_ascii=False)
    feats = "\n".join(f'''    <article class="feature reveal">
      <img src="/img/{shots}-{k}.webp" width="540" height="960" loading="lazy" alt="{e(m['alt_shot'] + h)}">
      <div class="text"><h3>{e(h)}</h3><p>{e(p)}</p></div>
    </article>''' for k, h, p in m["features"])
    how = "\n".join(f"      <li>{e(x)}</li>" for x in m["how"])
    iframe = (f'&lt;iframe src=&quot;https://www.youtube-nocookie.com/embed/{YT}?autoplay=1&quot; '
              f'title=&quot;{e(m["trailer_h"])}&quot; allow=&quot;autoplay; encrypted-media; picture-in-picture&quot; '
              f'allowfullscreen&gt;&lt;/iframe&gt;')
    return head(lang, "", m["title"], m["desc"], "website", "\n".join([ld(app), ld(video), ld(faq_ld)])) + f'''
<main>
  <div class="hero-wrap">
    <div class="rain" data-icons='{json.dumps(RAIN_ICONS)}' aria-hidden="true"></div>
    <div class="wrap hero">
      <div class="hero-text">
        <h1>{e(m['h1'])}</h1>
        <p class="lead">{e(m['lead'])}</p>
        {play_button(lang)}
        <span class="free">{e(m['free'])}</span>
        <p class="try">{e(m['try'])}</p>
      </div>
      <div class="demo" id="demo" data-demo='{e(demo)}'></div>
    </div>
  </div>
  <section class="wrap reveal">
    <h2>{e(m['trailer_h'])}</h2>
    <div class="trailer">
      <button type="button" aria-label="{e(m['trailer_btn'])}" onclick="this.outerHTML='{iframe}'"><img src="/img/trailer.jpg" width="1280" height="720" loading="lazy" alt="{e(m['trailer_btn'])}"></button>
    </div>
  </section>
  <section class="wrap">
    <h2 class="reveal">{e(m['feat_h'])}</h2>
    <div class="features">
{feats}
    </div>
  </section>
  <section class="wrap faq reveal">
    <h2>{e(faq['h'])}</h2>
{faq_html}
    <p class="center"><a class="more" href="{path(lang, HOWTO_FILE)}">{e(d['ui']['howto_link'])}<span aria-hidden="true">→</span></a></p>
  </section>
  <section class="wrap how reveal">
    <h2>{e(m['how_h'])}</h2>
    <ul>
{how}
    </ul>
    <div class="peek">
      <div class="peek-head mz-head" data-eyes='{eyes}'><img src="/img/watch_head.webp" width="800" height="294" alt=""></div>
      <div class="peek-pole"></div>
    </div>
    <p class="center">{play_button(lang)}</p>
  </section>
</main>
{footer(lang)}
<script src="/site.js?v={ver('site.js')}" defer></script>
</body>
</html>
'''


def howto(lang: str) -> str:
    """Страница «Как играть»: правила полки, механики, режимы на двоих."""
    d = L[lang]
    h, u, m = d["howto"], d["ui"], d["main"]
    url = SITE + path(lang, HOWTO_FILE)
    body = []
    for i, (title, paras) in enumerate(h["sections"]):
        body.append(f"<h2>{e(title)}</h2>")
        if len(paras) > 2:
            body.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in paras) + "</ul>")
        else:
            body.extend(f"<p>{e(x)}</p>" for x in paras)
        if i == 4:
            body.append(f'<img class="doc-shot" src="/img/{d["shots"]}-mechanics.webp" width="540" height="960" '
                        f'loading="lazy" alt="{e(h["image_alt"])}">')
    steps = [{"@type": "HowToSection", "name": title, "itemListElement": [
        {"@type": "HowToStep", "text": x} for x in paras]} for title, paras in h["sections"]]
    howto_ld = {"@context": "https://schema.org", "@type": "HowTo", "name": h["title"], "description": h["desc"],
                "inLanguage": d["hreflang"], "step": steps}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": m["h1"], "item": SITE + path(lang)},
        {"@type": "ListItem", "position": 2, "name": h["h1"], "item": url}]}
    newline = "\n"
    return head(lang, HOWTO_FILE, h["title"], h["desc"], "article", ld(howto_ld) + "\n" + ld(crumbs)) + f'''
<main class="wrap doc">
<p class="crumbs"><a href="{path(lang)}">{e(u['home'])}</a> › {e(h['h1'])}</p>
<h1>{e(h['h1'])}</h1>
<p class="lead">{e(h['intro'])}</p>
{newline.join(body)}
<h2>{e(u['back_cta'])}</h2>
<p>{play_button(lang)}</p>
</main>
{footer(lang)}
<script src="/site.js?v={ver('site.js')}" defer></script>
</body>
</html>
'''


def stamp_docs() -> None:
    """Ручные страницы (политика, удаление) — та же метка версии стилей."""
    for doc in ("privacy.html", "delete.html", "ru/privacy.html", "ru/delete.html"):
        f = ROOT / doc
        text, n = re.subn(r'href="/style\.css(\?v=[0-9a-f]+)?"', f'href="/style.css?v={ver("style.css")}"',
                          f.read_text())
        assert n == 1, doc
        f.write_text(text)


def sitemap() -> str:
    def group(files: list[str]) -> str:
        out = ""
        for k in files:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{L[x]["hreflang"]}" href="{SITE}{path(x, k)}"/>'
                           for x in L)
            for lang in L:
                out += f"  <url>\n    <loc>{SITE}{path(lang, k)}</loc>\n    <lastmod>{DATE}</lastmod>{alts}\n  </url>\n"
        return out
    docs = ""
    for k in ("privacy.html", "delete.html"):
        alts = (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/{k}"/>'
                f'\n    <xhtml:link rel="alternate" hreflang="ru" href="{SITE}/ru/{k}"/>')
        for p in (f"/{k}", f"/ru/{k}"):
            docs += f"  <url>\n    <loc>{SITE}{p}</loc>{alts}\n  </url>\n"
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{group(["", HOWTO_FILE])}{docs}</urlset>\n')


def assets() -> None:
    """Картинки из игры → img/ (WebP)."""
    from PIL import Image
    img = ROOT / "img"
    (img / "tile").mkdir(parents=True, exist_ok=True)
    tiles = json.loads((GAME / "shared/tiles/tiles.json").read_text())
    atlas = Image.open(GAME / "shared/tiles/icons.png")
    cell, cols = tiles["icon_cell"], tiles["icon_cols"]
    for n in sorted(set(DEMO_ICONS + RAIN_ICONS)):
        x, y = (n % cols) * cell, (n // cols) * cell
        atlas.crop((x, y, x + cell, y + cell)).save(img / "tile" / f"{n}.webp", "WEBP", quality=86, method=6)
    m = GAME / "mobile/assets/mazhobe"
    Image.open(m / "watch_shop.png").convert("RGB").resize((800, 300), Image.LANCZOS).save(
        img / "watch_shop.webp", "WEBP", quality=80, method=6)
    Image.open(m / "watch_head.png").resize((800, 294), Image.LANCZOS).save(
        img / "watch_head.webp", "WEBP", quality=86, method=6)
    Image.open(GAME / "shared/ui/pole.png").save(img / "pole.webp", "WEBP", quality=86, method=6)
    bg = Image.open(GAME / "shared/backgrounds/autumn.jpg").convert("RGB")
    bg.resize((720, round(bg.height * 720 / bg.width)), Image.LANCZOS).save(img / "field.webp", "WEBP", quality=72,
                                                                             method=6)
    raw = GAME / "mobile/store/screenshots/raw"
    for lang in ("en", "ru"):
        for shot in SHOTS:
            src = sorted(raw.glob(f"{lang}/phone/0*_{shot}.png"))[0]
            Image.open(src).convert("RGB").resize((540, 960), Image.LANCZOS).save(
                img / f"{lang}-{shot}.webp", "WEBP", quality=80, method=6)
    eyes = json.loads((m / "watch.json").read_text())["eyes"]
    (ROOT / "_src/eyes.json").write_text(json.dumps(eyes))
    print("картинки обновлены")


def main() -> None:
    if "--assets" in sys.argv:
        assets()
    for lang in L:
        out = ROOT / path(lang).lstrip("/")
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page(lang))
        (out / HOWTO_FILE).write_text(howto(lang))
    (ROOT / "sitemap.xml").write_text(sitemap())
    stamp_docs()
    print("страницы собраны:", ", ".join(L))


if __name__ == "__main__":
    main()
