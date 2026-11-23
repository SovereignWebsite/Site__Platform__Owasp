#!/usr/bin/env python3
"""Five designs of owasp.platform.sovereignweb.site's home page. design.c@SovereignWebsite.dinis, round 1.
Words from the home page; figures read at build time from the site's own snapshot (data/owasp), OWASP Foundation
content under CC BY-SA 4.0 as data/owasp/provenance.json states. HTML and CSS only. Usage: build.py <site dir>"""
import os, sys, json, html, collections

SITE = sys.argv[1]
OUT = os.path.join(SITE, "designs")
HOST = "https://owasp.platform.sovereignweb.site"
e = html.escape
MAN = json.load(open(os.path.join(SITE, "data/owasp/manifest.json")))
SNAP = MAN["latest_snapshot"]
D = json.load(open(os.path.join(SITE, "data/owasp/snapshots", SNAP, "projects.json")))
P = D["projects"]
TOTAL = D["project_count"]
LEVELS = D["source_counts"]["levels"]
CATS = collections.Counter(x.get("category") or "Other" for x in P).most_common()
FEAT = sorted([x for x in P if x.get("is_featured")], key=lambda x: x["title"].lower())
OBS = D["observed_at"][:10]
MARK = "owasp.platform.sovereignweb.site"
H1 = "OWASP"
INTRO = "What OWASP offers and how to use it, from its public material. An unofficial site, not made or endorsed by OWASP."
HERE = [
    '<a href="/projects/">Projects</a>: every OWASP project in a dated snapshot of OWASP’s public list, to search and filter, with a button to compare it with OWASP’s live counts.',
    '<a href="/graph/">Graph</a>: how the projects group by category and maturity level, and what each one links to, with the published field behind every link.',
]
NEXT = ('Coming next: OWASP’s history (the old wiki and past project pages, with the gaps shown) and more live views read in your browser from OWASP’s public sources. '
        'The plan is in the <a href="https://github.com/SovereignWebsite/Site__Platform__Owasp/blob/dev/docs/plan.md">repository</a>.')
OWN = "This site was made by one request to the Sovereign Website pipeline. Its files, its history and its address are in a repository its owner controls, and can move anywhere."
CREDIT = (f'Figures from the site’s snapshot of OWASP’s public project list, observed {OBS} ({TOTAL} projects). Project titles, '
          'categories and maturity labels are OWASP Foundation content, CC BY-SA 4.0, from owasp.org.')
DESIGNS = [
    (1, "Card Catalogue", "A library card catalogue: one drawer per category, its count on the label, the two tools as the reading room."),
    (2, "Maturity Ladder", "The projects as a ladder of maturity, incubator to flagship, each rung its count and its flagship names."),
    (3, "Signal Board", "Dark first: the snapshot as a board of signals, categories as bars with their numbers, the tools as switches."),
    (4, "Field Guide", "A field guide: the featured projects as specimens, then how to find the rest."),
    (5, "Brief", "Everything on one plain page, for reading fast or printing."),
]
FAMILY = [("https://sovereignwebsite.ai/", "Sovereign Website"), ("https://sovereignwebsite.org/", "Principles"),
          ("https://sovereignwebsite.site/", "Hosted"), ("https://hub.sovereignweb.site/", "Hub"),
          ("https://agents.sovereignweb.site/", "Agents"), ("https://vault.sovereignwebsite.site/", "Vault"),
          ("https://agenticcells.ai/", "AgentiCCells"), ("https://riskmandate.ai/", "RiskMandate"),
          ("https://newsroom.sgit.ai/", "Newsroom")]
CSP = "default-src 'self'; script-src 'none'; img-src 'self'; style-src 'self' 'unsafe-inline'; base-uri 'none'; form-action 'none'"
LEVEL_ORDER = ["incubator", "lab", "production", "flagship"]

BASE = """
*{box-sizing:border-box}
html{color-scheme:light dark;-webkit-text-size-adjust:100%}
body{margin:0;font:1.0625rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
a{color:var(--link)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.skip{position:absolute;left:-999px;top:.5rem;z-index:99;background:var(--bg);color:var(--fg);padding:.5rem .9rem;border:2px solid var(--focus)}
.skip:focus{left:1rem}
main *{min-width:0}
.chrome{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;justify-content:flex-end;position:relative;z-index:5;padding-top:.5rem}
.chrome .by{margin:0 auto 0 0;font-size:.9rem;color:var(--muted)}\n.chrome .by a{color:var(--fg)}\n.chrome details{position:relative}
.chrome summary{cursor:pointer;list-style:none;min-height:44px;display:inline-flex;align-items:center;padding:.35rem .8rem;border:1px solid var(--ctl);border-radius:999px;font-size:.9rem;background:var(--bg);color:var(--fg)}
.chrome summary::-webkit-details-marker{display:none}
.chrome summary::after{content:"";width:.45rem;height:.45rem;margin-left:.5rem;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translateY(-2px)}
.chrome details[open] summary::after{transform:rotate(-135deg)}
.chrome ul{position:absolute;right:0;top:calc(100% + .35rem);margin:0;padding:.4rem;list-style:none;min-width:15rem;max-width:calc(100vw - 2rem);background:var(--bg);color:var(--fg);border:1px solid var(--ctl);border-radius:.6rem;box-shadow:0 .6rem 1.6rem rgba(0,0,0,.25)}
.chrome li a{display:block;padding:.55rem .7rem;border-radius:.4rem;color:var(--fg);text-decoration:none;font-size:.95rem}
.chrome li a:hover,.chrome li a:focus-visible{background:var(--hover)}
.chrome li a[aria-current]{font-weight:700;text-decoration:underline}
.chrome .gap{border-top:1px solid var(--ctl);margin-top:.3rem;padding-top:.3rem}
.chrome small{display:block;font-size:.85rem;color:var(--muted);font-weight:400}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.signin{display:grid;grid-template-columns:1fr auto auto;gap:.4rem .6rem;align-items:end;margin:1.25rem 0 .5rem}
.signin label{font-size:.9rem;color:var(--muted);grid-row:1}
.signin label[for=__none]{grid-column:2}
.signin input,.signin select,.signin button{font:inherit;font-size:1rem;padding:.55rem .7rem;border:1px solid var(--ctl);border-radius:6px;background:var(--field);color:var(--fg);min-height:44px}
.signin input{grid-column:1;grid-row:2}.signin select{grid-column:2;grid-row:2}
.signin button{grid-column:3;grid-row:2;background:var(--accent);color:var(--on-accent);border-color:var(--accent);font-weight:700;cursor:pointer}
@media (max-width:30rem){.signin{grid-template-columns:1fr auto}.signin button{grid-column:1/-1;grid-row:3}}
.status{font-weight:700;min-height:1.6em}
.note{font-size:.95rem;color:var(--muted)}
button.small,.out select{font:inherit;font-size:1rem;padding:.4rem .7rem;border:1px solid var(--ctl);border-radius:6px;background:var(--field);color:var(--link);font-weight:700;min-height:44px;cursor:pointer}
.out select{color:var(--fg);font-weight:400}
.out label{color:var(--muted)}
#forget{margin:.3rem 0}
.out h3{font-size:1.1rem;margin:1rem 0 .3rem}
.out table{border-collapse:collapse;width:100%;font-size:.95rem}
.out caption{text-align:left;font-weight:700;padding:.4rem 0}
.out th,.out td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
.out thead th{color:var(--muted);font-size:.9rem}
.scroll{overflow-x:auto;margin:1rem 0}
.out table{border-collapse:collapse;width:100%;font-size:.95rem}
.out caption{text-align:left;font-weight:700;padding:.4rem 0}
.out th,.out td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--line)}
.out thead th{color:var(--muted);font-size:.9rem}
.out th .sub{display:block;font-weight:400;color:var(--muted);font-size:.875rem}
.out tr.group th{background:var(--hover);font-size:.875rem;letter-spacing:.06em;text-transform:uppercase}
.out td.vals{white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}
.out td.ok{color:var(--ok);font-weight:700;white-space:nowrap}
.out td.bad{color:var(--bad);font-weight:700}
.out td.num{text-align:right;font-variant-numeric:tabular-nums}
.sent{font-size:.9rem;color:var(--muted)}
footer{padding:2rem 0 3rem;font-size:.95rem}
footer nav{display:flex;flex-wrap:wrap;gap:.25rem 1.25rem}
footer nav a{min-height:44px;display:inline-flex;align-items:center}
@media print{.chrome,.skip,.signin,#forget{display:none}}
"""


def head(n, css):
    name, idea = (DESIGNS[n - 1][1], DESIGNS[n - 1][2]) if n else ("", "")
    title = f"{name}, design {n} of OWASP" if n else "Five designs, OWASP"
    desc = (f"Design {n} of owasp.platform.sovereignweb.site, {name}: {idea}" if n else
            "Five designs of owasp.platform.sovereignweb.site, the same words in five ideas, side by side.")
    url = f"{HOST}/designs/{n}/" if n else f"{HOST}/designs/"
    img = f"{HOST}/assets/share/card-1200x630.jpg"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OWASP">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="OWASP">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<style>{BASE}{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def chrome(n):
    d = "".join(f'<li><a href="/designs/{i}/"{" aria-current=\"page\"" if i == n else ""}>{i}. {nm}<small>{idea}</small></a></li>' for i, nm, idea in DESIGNS)
    fam = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in FAMILY)
    return f"""<nav class="chrome" aria-label="Designs and the Sovereign Website family">\n<p class="by"><a href="/">OWASP</a>, an unofficial site</p>
<details><summary>Choose a design</summary><ul>{d}<li class="gap"><a href="/designs/">All five, side by side</a></li><li><a href="/">The site as it is now</a></li></ul></details>
<details><summary>Sovereign Website</summary><ul><li><a href="/start/">Start here</a></li><li><a href="/agents/">Use with your AI</a></li><li><a href="/admin/">How this site was made</a></li><li class="gap"><a href="/policy/">How this site is governed</a></li>{fam}</ul></details>
</nav>"""


def own(cls="own"):
    return f'<nav class="{cls}" aria-label="This site"><a href="/projects/">Projects</a><a href="/graph/">Graph</a><a href="/start/">Start here</a><a href="/agents/">Use with your AI</a></nav>'


def ul(items, cls="plain"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def footer():
    return f"""<footer>
<nav aria-label="About this site"><a href="/start/">Start here</a> <a href="/agents/">Use with your AI</a> <a href="/admin/">How this site was made</a> <a href="/policy/">How this site is governed</a></nav>
<p>A sovereign website, made with the <a href="https://sovereignwebsite.org/">open pattern</a>. Source: <a href="https://github.com/SovereignWebsite/Site__Platform__Owasp">github.com/SovereignWebsite/Site__Platform__Owasp</a>.</p>
</footer>
</body>
</html>
"""



def here(cls="plain"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in HERE) + "</ul>"


def cat_table(cap="Projects by category"):
    rows = "".join(f'<tr><th scope="row">{e(c)}</th><td>{n}</td></tr>' for c, n in CATS)
    return f'<div class="tbox" tabindex="0" role="region" aria-label="{cap}"><table><caption>{cap}</caption><thead><tr><th scope="col">Category</th><th scope="col">Projects</th></tr></thead><tbody>{rows}</tbody></table></div>'


def feat_list(cls="feat"):
    return f'<ul class="{cls}">' + "".join(f'<li><a href="{e(x.get("website_url") or x.get("github_url") or "https://owasp.org/")}">{e(x["title"])}</a> <span>{e(x.get("category") or "")}</span></li>' for x in FEAT) + "</ul>"


COMMON = """
.plain{padding-left:1.2rem}.plain li{margin:.5rem 0}
.credit{font-size:.95rem;color:var(--muted)}
.tbox{overflow-x:auto}
table{border-collapse:collapse;width:100%}
caption{text-align:left;font-weight:700;padding:.3rem 0}
th,td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid var(--line)}
td{font-variant-numeric:tabular-nums}
.feat{list-style:none;padding:0;margin:0}
.feat li{padding:.35rem 0;border-bottom:1px solid var(--line)}
.feat span{color:var(--muted);font-size:.95rem}
"""

# 1. Card Catalogue
CSS1 = COMMON + """
:root{--bg:#f4efe4;--fg:#211c14;--muted:#574e40;--link:#7b2d12;--focus:#7b2d12;--ctl:#82786a;--hover:#e9e1cf;--field:#fff;--accent:#7b2d12;--on-accent:#fff;--line:#d5c9b3;--ok:#1d6b45;--bad:#a13a2a;--wood:#6b4423;--card:#fffdf7}
@media (prefers-color-scheme:dark){:root{--bg:#16130e;--fg:#efe8da;--muted:#c3b9a5;--link:#ffab8a;--focus:#ffab8a;--ctl:#8e8471;--hover:#24201a;--field:#1d1a15;--accent:#ffab8a;--on-accent:#1a0d06;--line:#3b352b;--ok:#86ddb3;--bad:#ff9b8a;--wood:#a8774a;--card:#1d1a15}}
.wrap{max-width:70rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font:700 1.3rem Georgia,"Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
h1,h2{font-family:Georgia,"Times New Roman",serif}
.k{font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:1.5rem 0 .3rem}
h1{font-size:clamp(2.6rem,9vw,5rem);line-height:1;margin:0 0 1rem}
.lede{font-size:1.15rem;max-width:42rem}
.cabinet{background:var(--wood);padding:1rem;border-radius:.4rem;margin:2rem 0}
.drawers{list-style:none;margin:0;padding:0;display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,12rem),1fr))}
.drawers li{background:var(--card);border-radius:.25rem;padding:.9rem;text-align:center;box-shadow:inset 0 -6px 0 var(--hover)}
.drawers b{display:block;font:700 2rem Georgia,serif}
.drawers span{display:block;font:600 .95rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase}
.room{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));margin:2rem 0}
.room h2{font-size:1.5rem;margin:0 0 .4rem}
footer{border-top:1px solid var(--line)}
"""


def d1():
    drawers = "".join(f"<li><b>{n}</b><span>{e(c)}</span></li>" for c, n in CATS)
    return head(1, CSS1) + f"""<div class="wrap">{chrome(1)}
<header class="mast"><a class="brand" href="/">OWASP</a>{own()}</header>
<main id="main"><p class="k">{MARK}</p><h1>{H1}</h1><p class="lede">{INTRO}</p>
<section class="cabinet" aria-labelledby="h-cab"><h2 id="h-cab" class="vh">The catalogue, by category</h2><ul class="drawers">{drawers}</ul></section>
<p class="credit">{CREDIT}</p>
<div class="room"><section aria-labelledby="h-here"><h2 id="h-here">What is here</h2>{here()}</section>
<section aria-labelledby="h-next"><h2 id="h-next">Coming next</h2><p>{NEXT}</p><p>{OWN}</p></section></div>
</main>
""" + footer().replace("</body>", "</div></body>")


# 2. Maturity Ladder
CSS2 = COMMON + """
:root{--bg:#f2f5f8;--fg:#101a24;--muted:#45515d;--link:#0b5394;--focus:#0b5394;--ctl:#6b7684;--hover:#e1e7ee;--field:#fff;--accent:#0b5394;--on-accent:#fff;--line:#cdd6e0;--ok:#1d6b45;--bad:#a13a2a;--rung:#ffffff}
@media (prefers-color-scheme:dark){:root{--bg:#0d131a;--fg:#e8eef4;--muted:#adb9c5;--link:#8cc4ff;--focus:#8cc4ff;--ctl:#7a8693;--hover:#18212c;--field:#121a23;--accent:#8cc4ff;--on-accent:#06121c;--line:#26323e;--ok:#86ddb3;--bad:#ff9b8a;--rung:#121a23}}
.wrap{max-width:70rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font-weight:800;font-size:1.25rem;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.k{font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:1.5rem 0 .3rem}
h1{font-size:clamp(2.4rem,8vw,4.4rem);line-height:1;margin:0 0 1rem;letter-spacing:-.02em}
h2{font-size:clamp(1.4rem,3.2vw,1.9rem);margin:0 0 .5rem}
.ladder{list-style:none;margin:1.5rem 0;padding:0;display:flex;flex-direction:column-reverse;gap:.6rem}
.ladder li{background:var(--rung);border:1px solid var(--line);border-left:8px solid var(--accent);border-radius:.4rem;padding:.8rem 1rem;display:grid;grid-template-columns:7rem 5rem 1fr;gap:1rem;align-items:baseline}
.ladder li:nth-child(1){margin-right:0}.ladder li:nth-child(2){margin-right:8%}.ladder li:nth-child(3){margin-right:16%}.ladder li:nth-child(4){margin-right:24%}
@media (max-width:40rem){.ladder li{grid-template-columns:1fr;gap:.2rem;margin-right:0!important}}
.ladder b{font-size:1.1rem;text-transform:capitalize}
.ladder .n{font-size:1.6rem;font-weight:800;font-variant-numeric:tabular-nums}
.ladder small{color:var(--muted);font-size:.95rem}
.two{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));margin:2rem 0}
footer{border-top:1px solid var(--line)}
"""


def d2():
    names = {"flagship": ", ".join(sorted((x["title"] for x in P if x.get("project_type") == "flagship"), key=str.lower))}
    rungs = "".join(f'<li><b>{lv}</b><span class="n">{LEVELS.get(lv, 0)}</span><small>{e(names.get(lv, ""))}</small></li>' for lv in LEVEL_ORDER)
    return head(2, CSS2) + f"""<div class="wrap">{chrome(2)}
<header class="mast"><a class="brand" href="/">OWASP</a>{own()}</header>
<main id="main"><p class="k">{MARK}</p><h1>{H1}</h1><p>{INTRO}</p>
<section aria-labelledby="h-lad"><h2 id="h-lad">{TOTAL} projects, by maturity level</h2><ol class="ladder">{rungs}</ol><p class="credit">{CREDIT}</p></section>
<div class="two"><section aria-labelledby="h-here"><h2 id="h-here">What is here</h2>{here()}</section>
<section aria-labelledby="h-next"><h2 id="h-next">Coming next</h2><p>{NEXT}</p><p>{OWN}</p></section></div>
</main>
""" + footer().replace("</body>", "</div></body>")


# 3. Signal Board (dark first)
CSS3 = COMMON + """
:root{--bg:#0a0c10;--fg:#eef1f5;--muted:#b3bac4;--link:#7fe0c4;--focus:#7fe0c4;--ctl:#7d8592;--hover:#161a21;--field:#11141a;--accent:#7fe0c4;--on-accent:#04140f;--line:#262b34;--ok:#7fe0c4;--bad:#ff9b8a;--panel:#11141a;--bar:#7fe0c4}
@media (prefers-color-scheme:light){:root{--bg:#eef1f4;--fg:#0b0e12;--muted:#47505b;--link:#0f6b52;--focus:#0f6b52;--ctl:#6c7581;--hover:#dfe4ea;--field:#fff;--accent:#0f6b52;--on-accent:#fff;--line:#c9d0d9;--ok:#0f6b52;--bad:#a13a2a;--panel:#ffffff;--bar:#0f6b52}}
.wrap{max-width:80rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font:800 1.15rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.2em;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.top{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));padding:1.5rem 0;align-items:end}
.k{font:700 .85rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0}
h1{font:800 clamp(3rem,12vw,7rem)/.95 ui-monospace,Menlo,Consolas,monospace;margin:.3rem 0 1rem;letter-spacing:-.02em}
h2{font:800 1rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;margin:0 0 .75rem;color:var(--accent)}
.big{font:800 clamp(3rem,10vw,6rem)/1 ui-monospace,Menlo,Consolas,monospace;color:var(--accent);margin:0}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:.6rem;padding:1.1rem 1.2rem;margin:1rem 0}
.bars{list-style:none;margin:0;padding:0;display:grid;gap:.45rem}
.bars li{display:grid;grid-template-columns:9rem 1fr 3rem;gap:.75rem;align-items:center;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.95rem}
.bars .t{height:.9rem;background:var(--hover);border-radius:.2rem;overflow:hidden}
.bars .t i{display:block;height:100%;background:var(--bar)}
.bars b{text-align:right}
@media (max-width:30rem){.bars li{grid-template-columns:1fr 3rem}.bars .t{grid-column:1/-1;grid-row:2}}
.switches{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr))}
details.data{margin-top:.75rem}details.data summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:700}
footer{border-top:1px solid var(--line)}
"""


def d3():
    mx = CATS[0][1]
    bars = "".join(f'<li><span>{e(c)}</span><span class="t" aria-hidden="true"><i style="width:{round(100*n/mx)}%"></i></span><b>{n}</b></li>' for c, n in CATS)
    return head(3, CSS3) + f"""<div class="wrap">{chrome(3)}
<header class="mast"><a class="brand" href="/">OWASP</a>{own()}</header>
<main id="main"><div class="top"><div><p class="k">{MARK}</p><h1>{H1}</h1><p>{INTRO}</p></div>
<div><p class="big">{TOTAL}</p><p>projects in the snapshot observed {OBS}</p></div></div>
<section class="panel" aria-labelledby="h-cat"><h2 id="h-cat">By category</h2><ul class="bars">{bars}</ul>
<details class="data"><summary>Show the data</summary>{cat_table()}</details><p class="credit">{CREDIT}</p></section>
<div class="switches"><section class="panel" aria-labelledby="h-here"><h2 id="h-here">What is here</h2>{here()}</section>
<section class="panel" aria-labelledby="h-next"><h2 id="h-next">Coming next</h2><p>{NEXT}</p><p>{OWN}</p></section></div>
</main>
""" + footer().replace("</body>", "</div></body>")


# 4. Field Guide
CSS4 = COMMON + """
:root{--bg:#f3f4ec;--fg:#1a1d14;--muted:#50553f;--link:#3d5a12;--focus:#3d5a12;--ctl:#787e69;--hover:#e6e8db;--field:#fff;--accent:#3d5a12;--on-accent:#fff;--line:#d3d6c4;--ok:#1d6b45;--bad:#a13a2a;--plate:#fffef8}
@media (prefers-color-scheme:dark){:root{--bg:#12140e;--fg:#ecefe2;--muted:#bec3ab;--link:#b7d98a;--focus:#b7d98a;--ctl:#868b77;--hover:#20231a;--field:#191c14;--accent:#b7d98a;--on-accent:#111806;--line:#343829;--ok:#86ddb3;--bad:#ff9b8a;--plate:#191c14}}
.wrap{max-width:72rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0;border-bottom:1px solid var(--fg)}
.brand{font:italic 700 1.3rem Georgia,"Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
h1,h2{font-family:Georgia,"Times New Roman",serif}
.k{font:italic 1rem Georgia,serif;color:var(--muted);margin:1.5rem 0 .3rem}
h1{font-size:clamp(2.4rem,8vw,4.4rem);line-height:1;margin:0 0 1rem}
h2{font-size:clamp(1.4rem,3.2vw,1.9rem);margin:0 0 .5rem}
.specimens{list-style:none;margin:1.25rem 0;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));counter-reset:sp}
.specimens li{counter-increment:sp;background:var(--plate);border:1px solid var(--line);padding:1rem;position:relative}
.specimens li::before{content:"No. " counter(sp);display:block;font:italic .95rem Georgia,serif;color:var(--muted)}
.specimens a{font:700 1.1rem Georgia,serif}
.specimens span{display:block;color:var(--muted);font-size:.95rem;margin-top:.25rem}
.two{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));margin:2rem 0}
footer{border-top:1px solid var(--fg)}
"""


def d4():
    spec = "".join(f'<li><a href="{e(x.get("website_url") or x.get("github_url") or "https://owasp.org/")}">{e(x["title"])}</a><span>{e(x.get("category") or "")}, {e(x.get("project_type") or "")}</span></li>' for x in FEAT)
    return head(4, CSS4) + f"""<div class="wrap">{chrome(4)}
<header class="mast"><a class="brand" href="/">OWASP</a>{own()}</header>
<main id="main"><p class="k">A field guide · {MARK}</p><h1>{H1}</h1><p>{INTRO}</p>
<section aria-labelledby="h-sp"><h2 id="h-sp">The {len(FEAT)} featured projects</h2><ol class="specimens">{spec}</ol><p class="credit">{CREDIT}</p></section>
<div class="two"><section aria-labelledby="h-here"><h2 id="h-here">Find the other {TOTAL - len(FEAT)}</h2>{here()}</section>
<section aria-labelledby="h-next"><h2 id="h-next">Coming next</h2><p>{NEXT}</p><p>{OWN}</p></section></div>
</main>
""" + footer().replace("</body>", "</div></body>")


# 5. Brief
CSS5 = COMMON + """
:root{--bg:#ffffff;--fg:#111111;--muted:#4a4a4a;--link:#0b4f8a;--focus:#0b4f8a;--ctl:#767676;--hover:#f0f0f0;--field:#ffffff;--accent:#0b4f8a;--on-accent:#ffffff;--line:#d6d6d6;--ok:#1d6b45;--bad:#a13a2a}
@media (prefers-color-scheme:dark){:root{--bg:#121212;--fg:#f1f1f1;--muted:#bdbdbd;--link:#8cc4ff;--focus:#8cc4ff;--ctl:#8a8a8a;--hover:#222;--field:#1a1a1a;--accent:#8cc4ff;--on-accent:#0b0b0b;--line:#333;--ok:#86ddb3;--bad:#ff9b8a}}
.wrap{max-width:42rem;margin:0 auto;padding:0 1rem}
.brand{font:700 1.1rem Georgia,"Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:0 1rem;font-size:.95rem}.own a{min-height:44px;display:inline-flex;align-items:center}
h1{font:700 clamp(2rem,6vw,2.6rem)/1.15 Georgia,serif;margin:1.25rem 0 .75rem}
h2{font:700 1.45rem Georgia,serif;margin:2rem 0 .4rem;padding-top:1rem;border-top:1px solid var(--line)}
footer{border-top:1px solid var(--line);margin-top:2rem}
"""


def d5():
    return head(5, CSS5) + f"""<div class="wrap">{chrome(5)}
<header><a class="brand" href="/">OWASP</a>{own()}</header>
<main id="main"><p>{MARK}</p><h1>{H1}</h1><p>{INTRO}</p>
<h2>What is here</h2>{here()}<p>{NEXT}</p><p>{OWN}</p>
<h2>The snapshot in figures</h2>{cat_table()}<p class="credit">{CREDIT}</p></main>
""" + footer().replace("</body>", "</div></body>")


CSSI = """
:root{--bg:#f6f5f2;--fg:#151515;--muted:#4f4c47;--link:#7b2d12;--focus:#7b2d12;--ctl:#77736c;--hover:#e9e6df;--card:#fff;--line:#dcd8cf;--field:#fff;--accent:#7b2d12;--on-accent:#fff;--ok:#1d6b45;--bad:#a13a2a}
@media (prefers-color-scheme:dark){:root{--bg:#121212;--fg:#efede8;--muted:#bdb9b1;--link:#ffab8a;--focus:#ffab8a;--ctl:#85817a;--hover:#222;--card:#1c1c1c;--line:#333;--field:#1a1a1a;--accent:#ffab8a;--on-accent:#1a0d06;--ok:#86ddb3;--bad:#ff9b8a}}
.wrap{max-width:76rem;margin:0 auto;padding:0 1rem}
.brand{font-weight:800;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
h1{font:700 clamp(2rem,5.5vw,3rem)/1.1 Georgia,serif;margin:1rem 0 .75rem}
.cards{list-style:none;margin:1.5rem 0 3rem;padding:0;display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-radius:.6rem;overflow:hidden}
.cards img{display:block;max-width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;object-position:top;width:100%;border-bottom:1px solid var(--line)}
.cards .b{padding:1rem}.cards h2{font-size:1.2rem;margin:0 0 .3rem}.cards p{margin:.3rem 0}
footer{border-top:1px solid var(--line)}
"""


def index(rec):
    cards = "".join(f'<li><img src="/designs/{i}/shot-1366.webp" alt="Design {i}, {nm}, at desktop width" width="1366" height="854" loading="lazy"><div class="b"><h2><a href="/designs/{i}/">{i}. {nm}</a></h2><p>{idea}</p>{"<p><strong>Recommended by the designer.</strong></p>" if i == rec else ""}</div></li>' for i, nm, idea in DESIGNS)
    return head(0, CSSI) + f"""<div class="wrap">{chrome(0)}
<header><a class="brand" href="/">OWASP</a></header>
<main id="main"><h1>Five designs of this site</h1>
<p>The same words, and figures from the site's own snapshot, in five ideas. The owner picks one; the keeper makes it the site.</p>
<ul class="cards">{cards}</ul></main>
""" + footer().replace("</body>", "</div></body>")


if __name__ == "__main__":
    for i, f in {1: d1, 2: d2, 3: d3, 4: d4, 5: d5}.items():
        os.makedirs(f"{OUT}/{i}", exist_ok=True)
        open(f"{OUT}/{i}/index.html", "w").write(f())
    open(f"{OUT}/index.html", "w").write(index(int(os.environ.get("RECOMMEND", "2"))))
    print("built", OUT, TOTAL, CATS[:3])
