// The project directory: search and filter the latest snapshot; on request, compare it with OWASP's live counts.
'use strict';
(function () {
  const { load, el, safeUrl, day, levelOf, projectPage, snapshotLine, LEVELS } = window.OWASP;
  const $ = (id) => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  let all = [];

  function fillSelect(sel, values, counts, current) {
    for (const v of values) sel.append(el('option', { value: v, text: v + ' (' + (counts.get(v) || 0) + ')', selected: v === current }));
  }
  function card(p) {
    const links = el('p', { class: 'links' });
    const add = (href, text) => { const u = safeUrl(href); if (u) links.append(el('a', { href: u, rel: 'noopener', text })); };
    add(projectPage(p), 'On owasp.org');
    add(p.github_url, 'Source');
    add(p.website_url, 'Website');
    add(p.documentation_url, 'Documentation');
    links.append(el('a', { href: '/graph/?project=' + encodeURIComponent(p.slug || p.id), text: 'Connections' }));
    return el('li', { class: 'project' },
      el('h2', { text: p.title }),
      el('p', { class: 'tags' },
        el('span', { class: 'tag level-' + levelOf(p), text: levelOf(p) }),
        el('span', { class: 'tag', text: p.category || 'no category' }),
        p.is_featured ? el('span', { class: 'tag', text: 'featured' }) : null,
        el('span', { class: 'dim', text: 'updated at source ' + day(p.updated_at) })),
      p.description_text ? el('p', { class: 'desc', text: p.description_text }) : el('p', { class: 'desc dim', text: 'No description in the source record.' }),
      links);
  }
  function render() {
    const q = $('q').value.trim().toLowerCase(), lv = $('level').value, cat = $('category').value, feat = $('featured').checked;
    const hit = all.filter((p) => (!lv || levelOf(p) === lv) && (!cat || p.category === cat) && (!feat || p.is_featured) &&
      (!q || (p.title + ' ' + (p.description_text || '') + ' ' + (p.category || '') + ' ' + (p.slug || '')).toLowerCase().includes(q)));
    $('count').textContent = hit.length + ' of ' + all.length + ' projects';
    $('list').replaceChildren(...hit.map(card));
    const next = new URLSearchParams();
    if (q) next.set('q', q); if (lv) next.set('level', lv); if (cat) next.set('category', cat); if (feat) next.set('featured', '1');
    history.replaceState(null, '', next.toString() ? '?' + next : location.pathname);
  }
  async function live(snap) {
    const out = $('live-out'); const btn = $('live');
    btn.disabled = true; out.textContent = 'Asking owasp.org…';
    try {
      const r = await fetch('https://owasp.org/api/public/projects/counts', { mode: 'cors', credentials: 'omit', cache: 'no-store', referrerPolicy: 'no-referrer' });
      if (!r.ok) throw new Error('owasp.org answered ' + r.status);
      const now = await r.json();
      const then = snap.source_counts;
      const rows = [['Projects', then.total, now.total]].concat(Object.keys({ ...then.levels, ...now.levels }).map((k) => [k, (then.levels || {})[k] ?? 0, (now.levels || {})[k] ?? 0]));
      const table = el('table', {}, el('caption', { text: 'OWASP’s counts: snapshot against now (checked ' + new Date().toLocaleTimeString('en-GB') + ')' }),
        el('thead', {}, el('tr', {}, el('th', { scope: 'col', text: '' }), el('th', { scope: 'col', text: 'Snapshot' }), el('th', { scope: 'col', text: 'Now' }), el('th', { scope: 'col', text: 'Change' }))),
        el('tbody', {}, ...rows.map(([k, a, b]) => el('tr', {}, el('th', { scope: 'row', text: k }), el('td', { text: String(a) }), el('td', { text: String(b) }), el('td', { text: b === a ? 'same' : (b > a ? '+' : '') + (b - a) })))));
      out.replaceChildren(table, el('p', { class: 'dim', text: now.total === then.total ? 'The total matches the snapshot. Individual records may still have changed; the next snapshot will show it.' : 'OWASP’s list has changed since the snapshot. The directory below still shows the snapshot.' }));
    } catch (e) {
      out.textContent = 'Could not read owasp.org from your browser (' + e.message + '). The snapshot below is unchanged.';
    } finally { btn.disabled = false; }
  }
  load(false).then((d) => {
    all = d.projects.projects.slice().sort((a, b) => a.title.localeCompare(b.title, 'en-GB'));
    snapshotLine(d, $('snapshot'));
    const lc = new Map(), cc = new Map();
    for (const p of all) { lc.set(levelOf(p), (lc.get(levelOf(p)) || 0) + 1); if (p.category) cc.set(p.category, (cc.get(p.category) || 0) + 1); }
    fillSelect($('level'), LEVELS.filter((l) => lc.has(l)).concat([...lc.keys()].filter((l) => !LEVELS.includes(l))), lc, params.get('level'));
    fillSelect($('category'), [...cc.keys()].sort((a, b) => cc.get(b) - cc.get(a) || a.localeCompare(b)), cc, params.get('category'));
    $('q').value = params.get('q') || ''; $('featured').checked = params.get('featured') === '1';
    for (const id of ['q', 'level', 'category', 'featured']) $(id).addEventListener('input', render);
    $('live').addEventListener('click', () => live(d.projects));
    $('live').hidden = false;
    const v = d.validation;
    $('validation').textContent = v.level_counts_cover_all_projects ? 'OWASP’s maturity counts cover every project.'
      : 'OWASP’s counts endpoint gives ' + v.source_project_total + ' projects, but its maturity counts add up to ' + v.level_count_total + '. The other ' + (v.source_project_total - v.level_count_total) + ' carry the type “other” in the list and are shown as such; no level is invented for them.';
    render();
  }).catch((e) => { $('snapshot').textContent = 'The snapshot could not be loaded (' + e.message + ').'; });
})();
