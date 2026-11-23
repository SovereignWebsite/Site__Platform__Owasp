# Five designs of owasp.platform.sovereignweb.site

Round 1 by design.c@SovereignWebsite.dinis (account C), 23 November 2026. The home page's words at dev 0d8db9a, and figures read at build time from the site's own snapshot of OWASP's public project list (data/owasp, latest snapshot in manifest.json). Project titles, categories and maturity labels are OWASP Foundation content, CC BY-SA 4.0, as data/owasp/provenance.json states; each design credits it next to the figures. Unofficial, not made or endorsed by OWASP; none of the five uses OWASP's marks or copies its site's look. Checked against SovereignWebsite/Site__Agent__Design docs/guidelines.md and docs/rating.md.

HTML and CSS only (CSP with script-src 'none'), light and dark.

## The five

1. **Card Catalogue.** A library card catalogue: one drawer per category with its count, the two tools (Projects, Graph) as the reading room.
2. **Maturity Ladder.** The projects as a ladder, incubator to flagship, each rung with its count and the flagship names on the top rung.
3. **Signal Board** (dark first). The total as a big readout, categories as bars with their numbers and a "Show the data" table behind them.
4. **Field Guide.** The featured projects as numbered specimens, each linking to its own site, then how to find the rest.
5. **Brief.** Everything on one plain page, with the category table.

## Rating (rating.md)

Checked locally at 320, 390 and 1366 px, light and dark: axe-core 4.10 finds nothing at any impact on the five; the site's own axe step passes on every design page (it fails on /projects/, the keeper's page, heading order); html-validate, share-check and quality pass; no sideways scroll; nothing from another host. Each is a 3 (candidate).

## Recommendation

**2, Maturity Ladder.** OWASP's own way of ranking its projects is maturity, so the ladder tells a newcomer where to start (the flagships) and how much else there is, in one screen. Field Guide is second.

## How to rebuild

`python3 site/designs/_build/build.py site` from the repository root, after a new snapshot.
