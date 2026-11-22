"use strict";

const state = {
  snapshot: null,
  projects: [],
  graph: null,
  catalogue: null,
  historicalSamples: [],
  projectPage: 1,
  archivePage: 1,
  projectPageSize: 12,
  archivePageSize: 20,
  graphHitAreas: []
};

const byId = id => document.getElementById(id);

const sourceLists = {
  "owasp-sources": [
    ["Current OWASP projects", "https://owasp.org/projects"],
    ["OWASP public project counts", "https://owasp.org/api/public/projects/counts"],
    ["OWASP public project list", "https://owasp.org/api/public/projects/list?limit=1000"],
    ["OWASP Nest", "https://github.com/OWASP/Nest"],
    ["Old main website repository", "https://github.com/OWASP/owasp.github.io"],
    ["Old wiki Markdown conversion", "https://github.com/OWASP-Foundation/OWASP-wiki-md"],
    ["Threat Dragon migration notes", "https://owasp.org/projects/threat-dragon?tab=faqs"],
    ["September 2026 board minutes", "https://owasp.org/board/meetings/202609"]
  ],
  "spotify-sources": [
    ["OAuth authorisation and PKCE", "https://developer.spotify.com/documentation/web-api/concepts/authorization"],
    ["Display profile data in a browser app", "https://developer.spotify.com/documentation/web-api/howtos/web-app-profile"],
    ["Scopes and endpoint permissions", "https://developer.spotify.com/documentation/web-api/concepts/scopes"],
    ["Development and extended quota modes", "https://developer.spotify.com/documentation/web-api/concepts/quota-modes"],
    ["July 2026 quota changes", "https://developer.spotify.com/blog/2026-07-23-web-api-quota-updates"],
    ["Spotify Developer Policy", "https://developer.spotify.com/policy"],
    ["Spotify account exports", "https://support.spotify.com/us/article/understanding-your-data/"]
  ]
};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function safeLink(label, address) {
  const link = element("a", "", label);
  try {
    const url = new URL(address);
    if (url.protocol === "https:" || url.protocol === "http:") {
      link.href = url.href;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  } catch {
    link.removeAttribute("href");
  }
  return link;
}

function dateLabel(value) {
  return new Intl.DateTimeFormat("en-GB", {
    day: "2-digit", month: "short", year: "numeric",
    hour: "2-digit", minute: "2-digit", timeZone: "Europe/London"
  }).format(new Date(value)) + " London time";
}

async function readJSON(url) {
  const response = await fetch(url, { credentials: new URL(url, location.href).origin === location.origin ? "same-origin" : "omit", signal: AbortSignal.timeout(30000) });
  if (!response.ok) throw new Error("Request returned HTTP " + response.status);
  return response.json();
}

function populateSelect(select, values, placeholder) {
  const previous = select.value;
  select.replaceChildren();
  const all = element("option", "", placeholder);
  all.value = "";
  select.append(all);
  for (const value of [...new Set(values.filter(Boolean))].sort()) {
    const option = element("option", "", value);
    option.value = value;
    select.append(option);
  }
  if ([...select.options].some(option => option.value === previous)) select.value = previous;
}

function updateFilters() {
  populateSelect(byId("level-filter"), state.projects.map(p => p.project_type), "All maturity levels");
  populateSelect(byId("category-filter"), state.projects.map(p => p.category), "All categories");
}

function filteredProjects() {
  const query = byId("project-search").value.trim().toLowerCase();
  const level = byId("level-filter").value;
  const category = byId("category-filter").value;
  return state.projects.filter(project => {
    const text = [project.title, project.description_text, project.category].join(" ").toLowerCase();
    return (!query || text.includes(query)) &&
      (!level || project.project_type === level) &&
      (!category || project.category === category);
  });
}

function showProject(project) {
  byId("detail-context").textContent = "Project record · " + project.id;
  const body = byId("detail-body");
  body.replaceChildren(element("h2", "", project.title));
  body.append(element("p", "", project.description_text || "Description is unavailable in this source record."));
  body.append(element("p", "footnote",
    "Maturity · " + (project.project_type || "Unclassified") +
    "   Category · " + (project.category || "Unclassified")));
  const links = element("div", "detail-links");
  links.append(safeLink("OWASP project page", "https://owasp.org/projects/" + encodeURIComponent(project.slug)));
  for (const [field, title] of [
    ["github_url", "Repository"], ["website_url", "Website"], ["documentation_url", "Documentation"]
  ]) {
    if (project[field]) links.append(safeLink(title, project[field]));
  }
  body.append(links);
  if (project.updated_at) body.append(element("p", "footnote", "Source updated at " + dateLabel(project.updated_at)));
  body.append(element("p", "footnote", "Captured snapshot " + state.snapshot.snapshot_id));
  const graphButton = element("button", "button", "Explore captured relationships");
  graphButton.addEventListener("click", () => {
    byId("detail").close();
    byId("graph-project").value = project.id;
    location.hash = "graph";
    drawGraph();
  });
  body.append(graphButton);
  byId("detail").showModal();
}

function renderProjects() {
  const projects = filteredProjects();
  const pages = Math.max(1, Math.ceil(projects.length / state.projectPageSize));
  state.projectPage = Math.min(state.projectPage, pages);
  const grid = byId("project-grid");
  grid.replaceChildren();
  const start = (state.projectPage - 1) * state.projectPageSize;
  for (const project of projects.slice(start, start + state.projectPageSize)) {
    const card = element("article", "project-card");
    const top = element("div", "card-top");
    top.append(element("span", "level " + (project.project_type || ""), project.project_type || "Unclassified"));
    top.append(element("span", "category", project.category || ""));
    const title = element("button", "card-title", project.title);
    title.addEventListener("click", () => showProject(project));
    const bottom = element("div", "card-bottom");
    bottom.append(safeLink("OWASP project page", "https://owasp.org/projects/" + encodeURIComponent(project.slug)));
    const details = element("button", "", "View record");
    details.addEventListener("click", () => showProject(project));
    bottom.append(details);
    card.append(top, title,
      element("p", "card-description", project.description_text || "No description supplied."),
      bottom);
    grid.append(card);
  }
  if (!projects.length) grid.append(element("p", "empty", "No projects match these filters."));
  byId("project-count").textContent = projects.length + " projects";
  byId("project-page").textContent = "Page " + state.projectPage + " of " + pages;
  byId("project-prev").disabled = state.projectPage === 1;
  byId("project-next").disabled = state.projectPage === pages;
  const metrics = byId("metrics");
  metrics.replaceChildren();
  for (const [label, count] of [
    ["Projects", state.projects.length],
    ...["flagship", "production", "lab", "incubator"].map(level => [
      level.charAt(0).toUpperCase() + level.slice(1),
      state.projects.filter(p => p.project_type === level).length
    ])
  ]) {
    const metric = element("div", "metric");
    metric.append(element("strong", "", String(count)), element("span", "", label));
    metrics.append(metric);
  }
}

async function refreshLive() {
  const button = byId("refresh");
  button.disabled = true;
  const status = byId("live-state");
  status.className = "";
  status.textContent = "Requesting live data directly from OWASP…";
  try {
    const data = await readJSON("https://owasp.org/api/public/projects/list?limit=1000");
    if (!Array.isArray(data.projects) || !data.projects.length ||
      !data.projects.every(p => typeof p.id === "string" && typeof p.title === "string")) {
      throw new Error("The source response schema changed.");
    }
    state.projects = data.projects.map(project => {
      const documentValue = new DOMParser().parseFromString(project.description || "", "text/html");
      return { ...project, description_text: documentValue.body.textContent || "" };
    });
    updateFilters();
    state.projectPage = 1;
    renderProjects();
    status.className = "live-success";
    status.textContent = "Live data loaded " + dateLabel(new Date().toISOString());
  } catch (error) {
    status.className = "error";
    status.textContent = "Live fetch failed. " + error.message + " Captured data remains available.";
  } finally {
    button.disabled = false;
  }
}

async function loadGraph() {
  if (!state.graph) state.graph = await readJSON("data/graph.json");
  drawGraph();
}

function selectedGraphRelations() {
  const projectId = "project:" + byId("graph-project").value;
  const projectNode = state.graph.nodes.find(node => node.id === projectId);
  const edges = state.graph.edges.filter(edge => edge.source === projectId);
  return {
    projectNode,
    edges,
    targets: edges.map(edge => state.graph.nodes.find(node => node.id === edge.target))
  };
}

function showEvidence(node, edge) {
  const panel = byId("graph-evidence");
  panel.replaceChildren(element("h3", "", node.label));
  panel.append(element("div", "evidence-key", "NODE TYPE"), element("p", "", node.kind));
  if (edge) {
    panel.append(element("div", "evidence-key", "PUBLISHED RELATION"),
      element("p", "", edge.relation.replaceAll("_", " ")),
      element("div", "evidence-key", "SOURCE FIELD"),
      element("p", "", edge.evidence_field));
  }
  if (node.kind === "repository" || node.kind === "website" || node.kind === "documentation") {
    panel.append(safeLink("Open source resource", node.label));
  }
  panel.append(element("div", "evidence-key", "CAPTURED SNAPSHOT"),
    element("p", "footnote", state.snapshot.snapshot_id));
}

function drawGraph() {
  if (!state.graph || byId("graph").hidden) return;
  const { projectNode, edges, targets } = selectedGraphRelations();
  if (!projectNode) return;
  const canvas = byId("graph-canvas");
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const pixelRatio = window.devicePixelRatio || 1;
  canvas.width = width * pixelRatio;
  canvas.height = height * pixelRatio;
  const context = canvas.getContext("2d");
  context.scale(pixelRatio, pixelRatio);
  context.clearRect(0, 0, width, height);
  const centre = { x: width / 2, y: height / 2 - 5 };
  const radius = Math.min(width * .31, height * .34, 165);
  const locations = targets.map((node, index) => ({
    node, edge: edges[index],
    x: centre.x + Math.cos(-Math.PI / 2 + 2 * Math.PI * index / targets.length) * radius,
    y: centre.y + Math.sin(-Math.PI / 2 + 2 * Math.PI * index / targets.length) * radius
  }));
  context.strokeStyle = "#a9c8dd";
  context.lineWidth = 1.7;
  for (const point of locations) {
    context.beginPath();
    context.moveTo(centre.x, centre.y);
    context.lineTo(point.x, point.y);
    context.stroke();
  }
  state.graphHitAreas = [];
  const nodes = [{ ...centre, node: projectNode, radius: 29 }, ...locations.map(point => ({ ...point, radius: 17 }))];
  for (const point of nodes) {
    context.beginPath();
    context.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
    context.fillStyle = point.node.kind === "project" ? "#0c6eae" : "#e5f0f7";
    context.fill();
    context.strokeStyle = "#4b97c6";
    context.stroke();
    context.textAlign = "center";
    context.font = "500 12px Arial";
    context.fillStyle = "#254963";
    const label = point.node.label.replace(/^https?:\/\//, "").replace(/\/$/, "");
    const cropped = label.length > 31 ? label.slice(0, 28) + "…" : label;
    context.fillText(cropped, point.x, point.y + point.radius + 20, Math.min(200, width * .45));
    state.graphHitAreas.push(point);
  }
  const relations = byId("graph-relations");
  relations.replaceChildren();
  for (const point of locations) {
    const button = element("button", "", point.node.kind + " · " + point.node.label);
    button.addEventListener("click", () => showEvidence(point.node, point.edge));
    relations.append(button);
  }
  showEvidence(projectNode);
}

async function loadArchive() {
  if (!state.catalogue) state.catalogue = await readJSON("data/wiki-catalogue.json");
  if (!state.historicalSamples.length) {
    state.historicalSamples = await Promise.all([
      readJSON("data/wiki-testing-tools-sample.json"),
      readJSON("data/threat-dragon-2020.json")
    ]);
  }
  renderArchive();
}

async function openArchiveDocument(item) {
  byId("detail-context").textContent = "Historical document · Pinned source";
  const body = byId("detail-body");
  body.replaceChildren(element("h2", "", item.title || "Captured historical page"));
  body.append(element("p", "", "Loading document…"));
  byId("detail").showModal();
  try {
    let content = item.content;
    const address = item.raw_url || item.source_url;
    if (!content) {
      const response = await fetch(address, { credentials: "omit", signal: AbortSignal.timeout(30000) });
      if (!response.ok) throw new Error("HTTP " + response.status);
      content = await response.text();
    }
    body.replaceChildren(element("h2", "", item.title || "Captured historical page"));
    body.append(safeLink("Open pinned source", address));
    body.append(element("p", "footnote", "Source revision " +
      (item.source_revision || item.commit_sha || state.catalogue.source_revision)));
    body.append(element("pre", "archive-content", content));
  } catch (error) {
    body.replaceChildren(element("h2", "", item.title || "Historical document"));
    body.append(element("p", "error", "The source could not be loaded. " + error.message));
    body.append(safeLink("Open source independently", item.raw_url || item.source_url));
  }
}

function renderArchive() {
  if (!state.catalogue) return;
  const query = byId("archive-search").value.trim().toLowerCase();
  const mode = byId("archive-mode").value;
  const records = mode === "titles" ? state.catalogue.documents :
    state.historicalSamples.map((item, index) => ({
      ...item,
      title: index === 0 ? "Old wiki · Appendix A Testing Tools" : "Threat Dragon · December 2020"
    }));
  const matches = records.filter(item =>
    (mode === "titles" ? item.title : item.title + " " + item.content).toLowerCase().includes(query));
  const pages = Math.max(1, Math.ceil(matches.length / state.archivePageSize));
  state.archivePage = Math.min(state.archivePage, pages);
  byId("archive-status").textContent = matches.length + " matches · " +
    (mode === "titles" ? "Title catalogue at revision " + state.catalogue.source_revision.slice(0, 10) : "Two captured full-text samples");
  const list = byId("archive-results");
  list.replaceChildren();
  const start = (state.archivePage - 1) * state.archivePageSize;
  for (const item of matches.slice(start, start + state.archivePageSize)) {
    const row = element("article", "archive-row");
    const info = element("div");
    info.append(element("h3", "", item.title), element("p", "", mode === "titles" ?
      "Archived Markdown · Source file available on request" :
      "Captured full text · Source date and retrieval time preserved"));
    const button = element("button", "secondary", "Read source");
    button.addEventListener("click", () => openArchiveDocument(item));
    row.append(info, button);
    list.append(row);
  }
  if (!matches.length) list.append(element("p", "empty", "No archived documents match this search."));
  byId("archive-page").textContent = "Page " + state.archivePage + " of " + pages;
  byId("archive-prev").disabled = state.archivePage === 1;
  byId("archive-next").disabled = state.archivePage === pages;
}

async function activateView() {
  const requested = location.hash.slice(1) || "directory";
  const viewId = ["directory", "graph", "archive", "handover", "spotify"].includes(requested) ? requested : "directory";
  for (const section of document.querySelectorAll(".view")) section.hidden = section.id !== viewId;
  for (const link of document.querySelectorAll("[data-view]")) {
    const active = link.dataset.view === viewId;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
  try {
    if (viewId === "graph") await loadGraph();
    if (viewId === "archive") await loadArchive();
  } catch (error) {
    const section = byId(viewId);
    let status = section.querySelector(".view-error");
    if (!status) {
      status = element("p", "view-error error");
      section.append(status);
    }
    status.textContent = "This view could not load. " + error.message;
  }
  window.scrollTo({ top: 0, behavior: "instant" });
}

async function initialize() {
  for (const [id, sources] of Object.entries(sourceLists)) {
    for (const [label, url] of sources) {
      const item = element("li");
      item.append(safeLink(label, url));
      byId(id).append(item);
    }
  }
  byId("close-detail").addEventListener("click", () => byId("detail").close());
  byId("refresh").addEventListener("click", refreshLive);
  byId("copy-brief").addEventListener("click", async () => {
    const status = byId("copy-status");
    try {
      const response = await fetch("downloads/AGENT-HANDOVER.md");
      if (!response.ok) throw new Error("Brief unavailable");
      await navigator.clipboard.writeText(await response.text());
      status.textContent = "Agent brief copied.";
    } catch {
      status.replaceChildren(element("span", "", "Clipboard unavailable. "));
      const link = element("a", "", "Open the agent brief");
      link.href = "downloads/AGENT-HANDOVER.md";
      status.append(link);
    }
  });
  for (const id of ["project-search", "level-filter", "category-filter"]) {
    byId(id).addEventListener("input", () => { state.projectPage = 1; renderProjects(); });
  }
  byId("project-prev").addEventListener("click", () => { state.projectPage--; renderProjects(); });
  byId("project-next").addEventListener("click", () => { state.projectPage++; renderProjects(); });
  byId("archive-prev").addEventListener("click", () => { state.archivePage--; renderArchive(); });
  byId("archive-next").addEventListener("click", () => { state.archivePage++; renderArchive(); });
  for (const id of ["archive-search", "archive-mode"]) {
    byId(id).addEventListener("input", () => { state.archivePage = 1; renderArchive(); });
  }
  byId("graph-project").addEventListener("change", drawGraph);
  byId("graph-canvas").addEventListener("click", event => {
    const rect = event.currentTarget.getBoundingClientRect();
    const hit = state.graphHitAreas.find(point =>
      Math.hypot(event.clientX - rect.left - point.x, event.clientY - rect.top - point.y) < point.radius + 15);
    if (hit) showEvidence(hit.node, hit.edge);
  });
  window.addEventListener("resize", drawGraph);
  state.snapshot = await readJSON("data/projects.json");
  state.projects = state.snapshot.projects;
  byId("snapshot-date").textContent = "Snapshot captured " + dateLabel(state.snapshot.observed_at);
  const picker = byId("graph-project");
  for (const project of [...state.projects].sort((a, b) => a.title.localeCompare(b.title))) {
    const option = element("option", "", project.title);
    option.value = project.id;
    picker.append(option);
  }
  updateFilters();
  renderProjects();
  window.addEventListener("hashchange", activateView);
  await activateView();
}

initialize().catch(error => {
  byId("snapshot-date").className = "error";
  byId("snapshot-date").textContent = "The captured directory could not load. " + error.message;
});
