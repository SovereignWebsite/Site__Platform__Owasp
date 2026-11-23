# Plan: owasp.platform.sovereignweb.site

owasp.c@SovereignWebsite.dinis, 22 November 2026. The idea is Dinis's: "a mix of real-time and static, and also past history data". ChatGPT's handover (branch inbox/chatgpt-owasp-handover-2026-11-22) is the starting material.

## The three parts

| Part | What the visitor gets | Data it reads | Where the data lives |
|---|---|---|---|
| Static (shipped first) | The project directory: search and filter every project; the graph: categories by maturity, each project's connections with the field behind each edge | A dated snapshot of OWASP's public project list | /data/owasp/snapshots/<id>/, listed in /data/owasp/manifest.json |
| Now | On request, the visitor's own browser reads OWASP's public endpoints and compares them with the snapshot. Never automatic, never through this site | owasp.org/api/public/projects/counts (and list), which answer with CORS `*` | Nothing stored; the snapshot stays as it is |
| History | The old wiki (title catalogue of 7,265 Markdown paths, pages read on demand from the pinned archive) and past project pages, with every gap shown as a gap | OWASP-Foundation/OWASP-wiki-md at e46e338; OWASP/www-project-* git history; past snapshots of the list | /data/owasp/history/ (next slice) |

## Provenance and licence, on every piece

- OWASP's site says: "Unless otherwise specified, all content on the site is Creative Commons Attribution-ShareAlike v4.0". Project data is republished under CC BY-SA 4.0 with attribution, and the derived files keep that licence. /data/owasp/provenance.json says this, with the source URLs, the source body hashes, the chain of custody and the changes made.
- Each page shows the snapshot time, the source, and a link to the provenance. Capture time, the record's own update time and the last check are three different values and are shown apart.
- OWASP is a trademark; the site says it is unofficial on every page.
- Open: the list endpoint is OWASP's website's own, with no reuse statement of its own. If OWASP says the site-wide licence does not cover it, the files come down and the site links instead.
- The wiki archive: OWASP's old wiki was CC BY-SA; the Markdown conversion's own terms and completeness are to be checked before any page body is republished. Until then: titles, and links to the source, not copies.
- People: only project leaders OWASP itself publishes, if ever. The current snapshot holds no names.

## What ChatGPT's work gives

- A working collector (Python standard library) with provenance per request: URL, status, CORS header, body SHA-256, time.
- One snapshot (20261122T162429Z: 347 projects, 825 nodes, 1,154 edges) and its validation, which found the 347 against 331 gap. That gap is the 16 projects whose type is "other"; the site says so and invents no level.
- The wiki title catalogue (7,265 paths at a pinned commit), one wiki page and one 2020 project page.
- A static explorer, used here as a reference, not copied: this site has its own pages in the seed's design, no innerHTML from data, and no downloads of OWASP material.

## What is missing

- More than one snapshot: the history of the list itself needs captures over time. Each needs a person's or an agent's run from a commit; ChatGPT's daily workflow stays inactive (no timer, Dinis 19 November).
- Full-text history: only two page bodies are captured. A coverage register (what was looked for, found, missing) comes before any bulk copying.
- Identity mapping between wiki paths, www-project-* repositories and current slugs, with evidence for each match.
- Live list compare (record by record, not only counts), and OWASP Nest as a second source (its API needs a key, so browser-only use is out).
- The owner's own share card (the seed's neutral card is still in place).
- RiskMandate policy evidence: the site's real policy is /policy/abp.json; no other policy claims are made.

## Slices

1. Directory and graph from the snapshot, with snapshot time, source and licence on the page. **Built** (branch owasp-c/first-slice; on dev once the claim is confirmed and the key published).
2. Live: record-level compare of the list in the browser, with what changed.
3. History: the wiki catalogue as a searchable index with links to source; coverage register; past project pages for the flagship projects.
4. Captures over time: a manual, signed capture run per snapshot, appended to the manifest.
