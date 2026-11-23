// Shared by the directory and the graph: loads the latest snapshot named in /data/owasp/manifest.json.
// No cookies, no storage, no tracking. Everything is drawn with textContent, never innerHTML.
'use strict';
window.OWASP = (function () {
  const LEVELS = ['flagship', 'production', 'lab', 'incubator', 'other'];
  const json = (u) => fetch(u, { cache: 'no-cache' }).then((r) => { if (!r.ok) throw new Error(u + ' answered ' + r.status); return r.json(); });
  async function load(withGraph) {
    const manifest = await json('/data/owasp/manifest.json');
    const id = manifest.latest_snapshot;
    if (!/^[0-9TZ]+-[0-9a-f]+$/.test(id)) throw new Error('unexpected snapshot id');
    const base = '/data/owasp/snapshots/' + id + '/';
    const [projects, validation, graph] = await Promise.all([json(base + 'projects.json'), json(base + 'validation.json'), withGraph ? json(base + 'graph.json') : null]);
    return { manifest, id, base, projects, validation, graph };
  }
  function el(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) { if (v === null || v === undefined || v === false) continue; if (k === 'text') e.textContent = v; else e.setAttribute(k, v === true ? '' : v); }
    for (const k of kids) if (k !== null && k !== undefined) e.append(k);
    return e;
  }
  const safeUrl = (u) => { try { const x = new URL(u); return x.protocol === 'https:' || x.protocol === 'http:' ? x.href : null; } catch { return null; } };
  const when = (iso) => { const d = new Date(iso); return isNaN(d) ? iso : d.toLocaleString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC'; };
  const day = (iso) => { const d = new Date(iso); return isNaN(d) ? iso : d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }); };
  const levelOf = (p) => (p.project_type || 'none');
  const projectPage = (p) => (/^[a-z0-9-]+$/.test(p.slug || '') ? 'https://owasp.org/projects/' + p.slug : null);
  function snapshotLine(d, target) {
    const s = d.projects;
    target.replaceChildren(
      'Snapshot ', el('strong', { text: when(s.observed_at) }), ', from OWASP’s public project list (',
      el('a', { href: 'https://owasp.org/projects', text: 'owasp.org/projects' }), '). ',
      String(s.project_count) + ' projects. Snapshot ', el('code', { text: d.id }), '. ',
      el('a', { href: '/data/owasp/provenance.json', text: 'Provenance and licence' }), '.'
    );
  }
  return { LEVELS, load, el, safeUrl, when, day, levelOf, projectPage, snapshotLine };
})();
