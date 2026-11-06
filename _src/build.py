#!/usr/bin/env python3
"""Сборка сайта игры: главные страницы (/ и /ru/), sitemap.xml и картинки
из репозитория игры. GitHub Pages папки с «_» не публикует — этот файл
на сайт не попадает.

    python3 _src/build.py            — страницы и sitemap
    python3 _src/build.py --assets   — ещё и картинки из игры (img/)

Политика и удаление данных (privacy.html, delete.html, ru/…) — обычные
файлы, правятся руками. Скриншоты для карточек — кадры без подписи из
mobile/store/screenshots/raw (tools/store_shots.gd … raw).
"""
import html
import json
import sys
from pathlib import Path

from content import FAQ, HOWTO, UI

SITE = "https://mahjong.stepanz.dev"
PLAY = "https://play.google.com/store/apps/details?id=dev.stepanz.mahjong"
YT = "HvKxJ-6F2d4"
ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT.parent / "mahjong"
# Иконки мини-игры (пары) и падающих тайлов — номера в атласе игры
# (shared/tiles/icons.png, tiles.json).
DEMO_ICONS = [63, 79, 77, 68, 50, 49]
RAIN_ICONS = [11, 12, 8, 18, 64, 84, 59, 41, 23, 21, 30, 93]
SHOTS = ["finisher", "duel", "mazhobe", "play", "mechanics", "daily"]
PLAY_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" '
             'd="M4 3.5v17a1 1 0 0 0 1.5.86l14-8.5a1 1 0 0 0 0-1.72l-14-8.5A1 1 0 0 0 4 3.5z"/></svg>')

T = {
    "en": {
        "path": "/", "play": PLAY + "&hl=en",
        "title": "Mazhobe: Mahjong for Two — online mahjong duels for Android",
        "desc": "Free mahjong for two on Android: duel friends online on one board, beat Mazhobe the toad, "
                "or team up in Duet. 3000 levels, a 4-tile shelf and a new daily level.",
        "h1": "Mazhobe: Mahjong for Two",
        "lead": "Mahjong duels online — with a friend, a random player or Mazhobe, the grumpy toad. "
                "Want some quiet? 3000 solo levels are waiting.",
        "cta": "Get it on Google Play", "free": "Free · Android",
        "try": "Try it right here: tap free tiles, match pairs on the shelf. Mazhobe is watching.",
        "demo": {"win": "Clean win!", "win_text": "That was a warm-up. The game has 3000 levels and online duels.",
                 "lose": "The shelf is full!", "lose_text": "Four different tiles — Mazhobe is very pleased with himself.",
                 "again": "Play again", "hint": "Tap a free tile"},
        "trailer_h": "Trailer", "trailer_btn": "Play the trailer",
        "video_name": "Mazhobe: Mahjong for Two — trailer",
        "feat_h": "What's inside",
        "features": [
            ("duel", "Online duels", "One board for two: whoever collects more pairs wins. Invite friends from the "
             "leaderboard or let the game find an opponent."),
            ("mazhobe", "Duel Mazhobe", "No opponent around, or no connection? Play Mazhobe himself — Sleepy, Sly or "
             "Reckless. The more reckless he is, the more acorns you win."),
            ("play", "A 4-tile shelf", "Tiles don't vanish on the board — they go to a shelf with four slots. Two alike "
             "make a pair, four different and you lose. Think one move ahead."),
            ("finisher", "Spectacular finishers", "14 finishers for the last pair: lightning, a black hole, ink, sakura "
             "and more — Mazhobe sells them all for acorns."),
            ("mechanics", "Ice, locks and mysteries", "Frozen tiles, bronze, silver and gold locks, and a mystery tile "
             "that blows the whole board apart."),
            ("daily", "Daily level", "One level for everyone each day. The ghost of the day's best player plays right "
             "beside you — overtake it for a bonus."),
        ],
        "how_h": "Also in the game",
        "how": ["Duet: clear one board together with a shared shelf", "3000 levels, 627 layouts from 22 to 258 tiles",
                "Leaderboards, friends, likes and titles from Mazhobe",
                "Google Play Games achievements; progress moves to a new phone",
                "22 languages; levels and duels with Mazhobe work offline"],
        "privacy": "Privacy Policy", "delete": "Data deletion", "contact": "Contact",
        "alt_shot": "Screenshot: ",
    },
    "ru": {
        "path": "/ru/", "play": PLAY + "&hl=ru",
        "title": "Мажобэ: Маджонг на двоих — дуэли в маджонг онлайн для Android",
        "desc": "Бесплатный маджонг на двоих для Android: дуэли с друзьями онлайн на одном поле, дуэль с жабой "
                "Мажобэ и «Дуэт». 3000 уровней, полка на 4 тайла и уровень дня.",
        "h1": "Мажобэ: Маджонг на двоих",
        "lead": "Дуэли в маджонг онлайн — с другом, случайным игроком или ворчливой жабой Мажобэ. "
                "А когда хочется тишины — 3000 уровней в одиночку.",
        "cta": "Скачать в Google Play", "free": "Бесплатно · Android",
        "try": "Попробуй прямо здесь: тапай свободные тайлы, собирай пары на полке. Мажобэ следит.",
        "demo": {"win": "Чистая победа!", "win_text": "Это была разминка. В игре — 3000 уровней и дуэли онлайн.",
                 "lose": "Полка забита!", "lose_text": "Четыре разных тайла — Мажобэ очень доволен собой.",
                 "again": "Ещё раз", "hint": "Тапни свободный тайл"},
        "trailer_h": "Ролик", "trailer_btn": "Смотреть ролик",
        "video_name": "Мажобэ: Маджонг на двоих — ролик",
        "feat_h": "Что внутри",
        "features": [
            ("duel", "Дуэль онлайн", "Одно поле на двоих: кто собрал больше пар — тот и победил. Зови друзей из "
             "таблицы лидеров или жми «Найти соперника»."),
            ("mazhobe", "Дуэль с Мажобэ", "Нет соперника или нет сети — играй с самим Мажобэ: Сонным, Хитрым или "
             "Азартным. Чем азартнее, тем больше жёлудей за победу."),
            ("play", "Полка на 4 тайла", "Тайлы не исчезают с поля, а ложатся на полку на четыре места. Две "
             "одинаковые — пара, четыре разных — проигрыш. Думай на ход вперёд."),
            ("finisher", "Зрелищные добивания", "14 добиваний для последней пары: молния, чёрная дыра, тушь, сакура "
             "и другие — Мажобэ продаёт их за жёлуди."),
            ("mechanics", "Лёд, замки и загадки", "Вмёрзшие тайлы, бронзовые, серебряные и золотые замки и "
             "тайл-загадка, от которого разлетается всё поле."),
            ("daily", "Уровень дня", "Один уровень на всех в сутки. Рядом играет призрак лучшего игрока дня — обгони "
             "его и получи бонус."),
        ],
        "how_h": "А ещё",
        "how": ["«Дуэт»: разбирайте одно поле вместе, полка общая", "3000 уровней, 627 форм раскладов от 22 до 258 тайлов",
                "Таблицы лидеров, друзья, лайки и титулы от Мажобэ",
                "Достижения Google Play Игр; прогресс переезжает на новый телефон",
                "22 языка; уровни и дуэль с Мажобэ работают без сети"],
        "privacy": "Политика конфиденциальности", "delete": "Удаление данных", "contact": "Связь",
        "alt_shot": "Скриншот: ",
    },
}


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
    bg.resize((720, round(bg.height * 720 / bg.width)), Image.LANCZOS).save(img / "field.webp", "WEBP", quality=72, method=6)
    raw = GAME / "mobile/store/screenshots/raw"
    for lang in ("en", "ru"):
        for i, shot in enumerate(SHOTS):
            src = sorted(raw.glob(f"{lang}/phone/0*_{shot}.png"))[0]
            Image.open(src).convert("RGB").resize((540, 960), Image.LANCZOS).save(
                img / f"{lang}-{shot}.webp", "WEBP", quality=80, method=6)
    eyes = json.loads((m / "watch.json").read_text())["eyes"]
    (ROOT / "_src/eyes.json").write_text(json.dumps(eyes))
    print("картинки обновлены")


def page(lang: str) -> str:
    t = T[lang]
    e = html.escape
    url = SITE + t["path"]
    ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": t["h1"],
          "alternateName": "Mazhobe Mahjong", "operatingSystem": "Android", "applicationCategory": "GameApplication",
          "description": t["desc"], "url": url, "image": SITE + "/img/feature.jpg", "inLanguage": lang,
          "installUrl": t["play"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "sameAs": [PLAY, "https://youtu.be/" + YT],
          "author": {"@type": "Person", "name": "Stepan Z"},
          "screenshot": [f"{SITE}/img/{lang}-{k}.webp" for k in SHOTS]}
    video = {"@context": "https://schema.org", "@type": "VideoObject", "name": t["video_name"],
             "description": t["desc"], "thumbnailUrl": SITE + "/img/trailer.jpg", "uploadDate": "2026-11-05",
             "duration": "PT36S", "embedUrl": f"https://www.youtube.com/embed/{YT}",
             "contentUrl": f"https://www.youtube.com/watch?v={YT}"}
    faq_h, faq = FAQ[lang]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    faq_html = "\n".join(f"      <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    eyes = (ROOT / "_src/eyes.json").read_text()
    demo = json.dumps({**t["demo"], "icons": DEMO_ICONS, "eyes": json.loads(eyes)}, ensure_ascii=False)
    rain = json.dumps(RAIN_ICONS)
    feats = "\n".join(f'''    <article class="feature reveal">
      <img src="/img/{lang}-{k}.webp" width="540" height="960" loading="lazy" alt="{e(t['alt_shot'] + h)}">
      <div class="text"><h3>{e(h)}</h3><p>{e(p)}</p></div>
    </article>''' for k, h, p in t["features"])
    how = "\n".join(f"      <li>{e(x)}</li>" for x in t["how"])
    nav = "".join(f'<a href="{T[l]["path"]}" hreflang="{l}"{" aria-current=\"page\"" if l == lang else ""}>'
                  f'{l.upper()}</a>' for l in ("en", "ru"))
    play_btn = f'<a class="play" href="{t["play"]}">{PLAY_ICON}{e(t["cta"])}</a>'
    iframe = (f'&lt;iframe src=&quot;https://www.youtube-nocookie.com/embed/{YT}?autoplay=1&quot; '
              f'title=&quot;{e(t["trailer_h"])}&quot; allow=&quot;autoplay; encrypted-media; picture-in-picture&quot; '
              f'allowfullscreen&gt;&lt;/iframe&gt;')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/">
<link rel="alternate" hreflang="ru" href="{SITE}/ru/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<link rel="icon" href="/icon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#17120d">
<link rel="preload" href="/fonts/philosopher.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t['h1'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/feature.jpg">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="500">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'ru_RU'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(video, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top">
  <a class="brand" href="{t['path']}"><img src="/icon.png" alt="" width="36" height="36">Mazhobe</a>
  <nav class="lang">{nav}</nav>
</header>
<main>
  <div class="hero-wrap">
    <div class="rain" data-icons='{rain}' aria-hidden="true"></div>
    <div class="wrap hero">
      <div class="hero-text">
        <h1>{e(t['h1'])}</h1>
        <p class="lead">{e(t['lead'])}</p>
        {play_btn}
        <span class="free">{e(t['free'])}</span>
        <p class="try">{e(t['try'])}</p>
      </div>
      <div class="demo" id="demo" data-demo='{e(demo)}'></div>
    </div>
  </div>
  <section class="wrap reveal">
    <h2>{e(t['trailer_h'])}</h2>
    <div class="trailer">
      <button type="button" aria-label="{e(t['trailer_btn'])}" onclick="this.outerHTML='{iframe}'"><img src="/img/trailer.jpg" width="1280" height="720" loading="lazy" alt="{e(t['trailer_btn'])}"></button>
    </div>
  </section>
  <section class="wrap">
    <h2 class="reveal">{e(t['feat_h'])}</h2>
    <div class="features">
{feats}
    </div>
  </section>
  <section class="wrap faq reveal">
    <h2>{e(faq_h)}</h2>
{faq_html}
    <p class="center"><a href="{t['path']}{HOWTO[lang]['file']}">{e(UI[lang]['howto_link'])} →</a></p>
  </section>
  <section class="wrap how reveal">
    <h2>{e(t['how_h'])}</h2>
    <ul>
{how}
    </ul>
    <div class="peek">
      <div class="peek-head mz-head" data-eyes='{eyes}'><img src="/img/watch_head.webp" width="800" height="294" alt=""></div>
      <div class="peek-pole"></div>
    </div>
    <p class="center">{play_btn}</p>
  </section>
</main>
{footer(lang)}
<script src="/site.js" defer></script>
</body>
</html>
'''


def footer(lang: str) -> str:
    t, e = T[lang], html.escape
    return f'''<footer class="wrap">
  <a href="{t['path']}{HOWTO[lang]['file']}">{e(UI[lang]['howto_link'])}</a> · <a href="{t['path']}privacy.html">{e(t['privacy'])}</a> · <a href="{t['path']}delete.html">{e(t['delete'])}</a> · {e(t['contact'])}: <a href="mailto:stepanz.dev@gmail.com">stepanz.dev@gmail.com</a>
</footer>'''


def howto(lang: str) -> str:
    """Страница «Как играть»: правила полки, механики, режимы на двоих."""
    t, h, e = T[lang], HOWTO[lang], html.escape
    path = t["path"] + h["file"]
    url = SITE + path
    nav = "".join(f'<a href="{T[l]["path"]}{h["file"]}" hreflang="{l}"{" aria-current=\"page\"" if l == lang else ""}>'
                  f'{l.upper()}</a>' for l in ("en", "ru"))
    shot, alt = h["image"]
    body = []
    for i, (title, paras) in enumerate(h["sections"]):
        body.append(f"<h2>{e(title)}</h2>")
        if len(paras) > 2:
            body.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in paras) + "</ul>")
        else:
            body.extend(f"<p>{e(x)}</p>" for x in paras)
        if i == 4:
            body.append(f'<img class="doc-shot" src="/img/{lang}-{shot}.webp" width="540" height="960" '
                        f'loading="lazy" alt="{e(alt)}">')
    steps = [{"@type": "HowToSection", "name": title, "itemListElement": [
        {"@type": "HowToStep", "text": x} for x in paras]} for title, paras in h["sections"]]
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": h["title"], "description": h["desc"],
          "inLanguage": lang, "step": steps}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["h1"], "item": SITE + t["path"]},
        {"@type": "ListItem", "position": 2, "name": h["h1"], "item": url}]}
    newline = "\n"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(h['title'])}</title>
<meta name="description" content="{e(h['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/{h['file']}">
<link rel="alternate" hreflang="ru" href="{SITE}/ru/{h['file']}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{h['file']}">
<link rel="icon" href="/icon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#17120d">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(h['title'])}">
<meta property="og:description" content="{e(h['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/feature.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>
</head>
<body>
<header class="top">
  <a class="brand" href="{t['path']}"><img src="/icon.png" alt="" width="36" height="36">Mazhobe</a>
  <nav class="lang">{nav}</nav>
</header>
<main class="wrap doc">
<p class="crumbs"><a href="{t['path']}">{e(UI[lang]['home'])}</a> › {e(h['h1'])}</p>
<h1>{e(h['h1'])}</h1>
<p class="lead">{e(h['intro'])}</p>
{newline.join(body)}
<h2>{e(UI[lang]['back_cta'])}</h2>
<p><a class="play" href="{t['play']}">{PLAY_ICON}{e(t['cta'])}</a></p>
</main>
{footer(lang)}
</body>
</html>
'''


def sitemap() -> str:
    def entry(en: str, ru: str, loc: str) -> str:
        return f'''  <url>
    <loc>{SITE}{loc}</loc>
    <lastmod>2026-11-06</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>
    <xhtml:link rel="alternate" hreflang="ru" href="{SITE}{ru}"/>
  </url>
'''
    pairs = [("/", "/ru/"), ("/how-to-play.html", "/ru/how-to-play.html"), ("/privacy.html", "/ru/privacy.html"),
             ("/delete.html", "/ru/delete.html")]
    urls = "".join(entry(en, ru, en) + entry(en, ru, ru) for en, ru in pairs)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')


def main() -> None:
    if "--assets" in sys.argv:
        assets()
    (ROOT / "index.html").write_text(page("en"))
    (ROOT / "ru/index.html").write_text(page("ru"))
    for lang in ("en", "ru"):
        (ROOT / (T[lang]["path"].lstrip("/") + HOWTO[lang]["file"])).write_text(howto(lang))
    (ROOT / "sitemap.xml").write_text(sitemap())
    print("страницы собраны")


if __name__ == "__main__":
    main()
