// The project graph: every edge comes from a field OWASP publishes, and names that field and the snapshot.
'use strict';
(function () {
  const { load, el, safeUrl, levelOf, projectPage, snapshotLine, LEVELS } = window.OWASP;
  const $ = (id) => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  const SVG = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, text) => { const e = document.createElementNS(SVG, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); if (text) e.textContent = text; return e; };
  const KIND = { category: 'Category', level: 'Maturity level', repository: 'Source repository', website: 'Website', documentation: 'Documentation' };

  load(true).then((d) => {
    const g = d.graph, nodes = new Map(g.nodes.map((n) => [n.id, n]));
    const bySource = new Map(), byTarget = new Map();
    for (const e of g.edges) {
      (bySource.get(e.source) || bySource.set(e.source, []).get(e.source)).push(e);
      (byTarget.get(e.target) || byTarget.set(e.target, []).get(e.target)).push(e);
    }
    const projects = d.projects.projects.slice().sort((a, b) => a.title.localeCompare(b.title, 'en-GB'));
    const bySlug = new Map(projects.map((p) => [p.slug || p.id, p]));
    snapshotLine(d, $('snapshot'));

    // Size of the graph, by kind of node and kind of edge.
    const nk = new Map(), ek = new Map();
    for (const n of g.nodes) nk.set(n.kind, (nk.get(n.kind) || 0) + 1);
    for (const e of g.edges) ek.set(e.relation, (ek.get(e.relation) || 0) + 1);
    $('stats').replaceChildren(
      el('li', {}, el('strong', { text: String(g.nodes.length) }), ' nodes: ' + [...nk].map(([k, n]) => n + ' ' + k).join(', ')),
      el('li', {}, el('strong', { text: String(g.edges.length) }), ' edges: ' + [...ek].map(([k, n]) => n + ' ' + k.replace('has_', '')).join(', ')));

    // Category by maturity level: how the two published groupings overlap. Each cell opens the directory, filtered.
    const levels = LEVELS.filter((l) => projects.some((p) => levelOf(p) === l));
    const cats = [...new Set(projects.map((p) => p.category || 'no category'))];
    const cell = (c, l) => projects.filter((p) => (p.category || 'no category') === c && (!l || levelOf(p) === l)).length;
    cats.sort((a, b) => cell(b) - cell(a) || a.localeCompare(b));
    const q = (c, l) => '/projects/?' + new URLSearchParams(Object.assign(c === 'no category' ? {} : { category: c }, l ? { level: l } : {}));
    $('matrix').replaceChildren(
      el('caption', { text: 'Projects by category (rows) and maturity level (columns). Select a number to see those projects.' }),
      el('thead', {}, el('tr', {}, el('th', { scope: 'col', text: 'Category' }), ...levels.map((l) => el('th', { scope: 'col', text: l })), el('th', { scope: 'col', text: 'All' }))),
      el('tbody', {}, ...cats.map((c) => el('tr', {}, el('th', { scope: 'row', text: c }),
        ...levels.concat([null]).map((l) => { const n = cell(c, l); return el('td', { class: n ? 'n' : 'n zero' }, n ? el('a', { href: q(c, l), text: String(n) }) : '0'); })))));

    // One project and its edges, drawn as a star and listed with the evidence for each edge.
    const pick = $('project');
    for (const p of projects) pick.append(el('option', { value: p.slug || p.id, text: p.title }));
    function showProject(key) {
      const p = bySlug.get(key) || projects[0];
      pick.value = p.slug || p.id;
      const edges = bySource.get('project:' + p.id) || [];
      const W = 640, H = 360, cx = W / 2, cy = H / 2, R = 135;
      const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-labelledby': 'star-title' });
      s.append(svg('title', { id: 'star-title' }, p.title + ' and its ' + edges.length + ' published connections'));
      edges.forEach((e, i) => {
        const a = -Math.PI / 2 + (2 * Math.PI * i) / Math.max(edges.length, 1), x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
        const n = nodes.get(e.target) || { kind: '?', label: e.target };
        s.append(svg('line', { x1: cx, y1: cy, x2: x, y2: y, class: 'edge' }));
        s.append(svg('circle', { cx: x, cy: y, r: 7, class: 'node k-' + n.kind }));
        const right = Math.cos(a) >= -0.01, label = n.kind === 'category' || n.kind === 'level' ? n.label : n.label.replace(/^https?:\/\//, '').replace(/\/$/, '');
        const t = svg('text', { x: x + (right ? 12 : -12), y: y + 4, 'text-anchor': right ? 'start' : 'end', class: 'lbl' });
        t.append(svg('tspan', { class: 'kind' }, (KIND[n.kind] || n.kind) + ': '), svg('tspan', {}, label.length > 34 ? label.slice(0, 33) + '…' : label));
        s.append(t);
      });
      s.append(svg('circle', { cx, cy, r: 11, class: 'node k-project' }));
      s.append(svg('text', { x: cx, y: cy - 18, 'text-anchor': 'middle', class: 'lbl title' }, p.title));
      $('star').replaceChildren(s);
      const page = projectPage(p);
      $('project-out').replaceChildren(
        el('p', {}, el('strong', { text: p.title }), ' ', page ? el('a', { href: page, rel: 'noopener', text: 'on owasp.org' }) : null),
        el('table', {}, el('caption', { text: 'Each edge, the field it comes from, and how many projects share its other end' }),
          el('thead', {}, el('tr', {}, ...['Relation', 'Connects to', 'Evidence field', 'Projects sharing it'].map((h) => el('th', { scope: 'col', text: h })))),
          el('tbody', {}, ...edges.map((e) => {
            const n = nodes.get(e.target) || { kind: '?', label: e.target }, u = safeUrl(n.label), shared = (byTarget.get(e.target) || []).length;
            return el('tr', {}, el('td', { text: e.relation.replace('has_', '') }),
              el('td', {}, u && n.kind !== 'category' && n.kind !== 'level' ? el('a', { href: u, rel: 'noopener', text: n.label }) : n.label),
              el('td', {}, el('code', { text: e.evidence_field })),
              el('td', {}, n.kind === 'category' ? el('a', { href: q(n.label), text: String(shared) }) : n.kind === 'level' ? el('a', { href: '/projects/?level=' + encodeURIComponent(n.label), text: String(shared) }) : String(shared)));
          }))));
      const next = new URLSearchParams({ project: p.slug || p.id });
      history.replaceState(null, '', '?' + next);
    }
    pick.addEventListener('input', () => showProject(pick.value));
    showProject(params.get('project') || 'cyclonedx');

    // Resources that more than one project points to: the only places the graph joins projects beyond grouping.
    const shared = [...byTarget].filter(([t, es]) => !/^(category|level):/.test(t) && es.length > 1);
    $('shared').replaceChildren(...(shared.length ? shared.map(([t, es]) => {
      const n = nodes.get(t), u = safeUrl(n.label);
      return el('li', {}, (KIND[n.kind] || n.kind) + ': ', u ? el('a', { href: u, rel: 'noopener', text: n.label }) : n.label, ' is named by ',
        ...es.flatMap((e, i) => { const p = projects.find((x) => 'project:' + x.id === e.source); return [i ? ' and ' : '', el('a', { href: '?project=' + encodeURIComponent(p.slug || p.id), text: p.title })]; }), '.');
    }) : [el('li', { text: 'None in this snapshot.' })]));
  }).catch((e) => { $('snapshot').textContent = 'The snapshot could not be loaded (' + e.message + ').'; });
})();
