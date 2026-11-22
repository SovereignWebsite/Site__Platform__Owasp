"""Capture public OWASP project metadata and an independently dated historical sample."""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://owasp.org"
LIST_URL = BASE + "/api/public/projects/list?limit=1000"
COUNTS_URL = BASE + "/api/public/projects/counts"
HISTORY_URL = "https://api.github.com/repos/OWASP/www-project-threat-dragon/commits?per_page=1&until=2020-12-31T23:59:59Z"
AGENT = "PrompTugal-OWASP-Research/0.1 (public project metadata research)"

class TextReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)

def plain_text(value):
    reader = TextReader()
    reader.feed(value or "")
    return " ".join(" ".join(reader.parts).split())

def fetch(url):
    request = Request(url, headers={"User-Agent": AGENT, "Origin": "https://data.promptugal.news"})
    with urlopen(request, timeout=40) as response:
        body = response.read()
        return body, {
            "requested_url": url,
            "final_url": response.url,
            "http_status": response.status,
            "content_type": response.headers.get("Content-Type"),
            "access_control_allow_origin": response.headers.get("Access-Control-Allow-Origin"),
            "etag": response.headers.get("ETag"),
            "body_sha256": hashlib.sha256(body).hexdigest(),
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.replace(temporary, path)

def graph(projects, snapshot_id):
    nodes = {}
    edges = []
    for project in projects:
        project_id = "project:" + project["id"]
        nodes[project_id] = {"id": project_id, "kind": "project", "label": project["title"]}
        relations = [
            ("category", project.get("category")),
            ("level", project.get("project_type")),
            ("repository", project.get("github_url")),
            ("website", project.get("website_url")),
            ("documentation", project.get("documentation_url"))
        ]
        for kind, value in relations:
            if not value:
                continue
            if kind in {"repository", "website", "documentation"} and urlparse(value).scheme not in {"http", "https"}:
                continue
            target = kind + ":" + value
            nodes[target] = {"id": target, "kind": kind, "label": value}
            edges.append({
                "source": project_id, "target": target, "relation": "has_" + kind,
                "evidence_field": {"level": "project_type", "repository": "github_url"}.get(kind, kind + "_url" if kind in {"website", "documentation"} else kind),
                "snapshot_id": snapshot_id
            })
    return {"snapshot_id": snapshot_id, "nodes": list(nodes.values()), "edges": edges}

def capture(include_history=False):
    list_body, list_provenance = fetch(LIST_URL)
    counts_body, counts_provenance = fetch(COUNTS_URL)
    listing = json.loads(list_body)
    counts = json.loads(counts_body)
    records = listing["projects"]
    if not records or not all(isinstance(p.get("id"), str) and isinstance(p.get("title"), str) for p in records):
        raise ValueError("Unexpected project list schema")
    if len({p["id"] for p in records}) != len(records):
        raise ValueError("Duplicate project identifiers")
    if counts["total"] != len(records):
        raise ValueError("Project list differs from total count. Inspect pagination or concurrent source changes before publishing.")
    fields = ("id", "created_at", "updated_at", "slug", "title", "category", "status", "is_featured", "project_type", "github_url", "website_url", "documentation_url")
    projects = []
    for record in records:
        item = {key: record.get(key) for key in fields}
        item["description_text"] = plain_text(record.get("description"))
        item["source_url"] = LIST_URL
        projects.append(item)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    content_hash = hashlib.sha256(json.dumps(projects, sort_keys=True).encode()).hexdigest()
    snapshot_id = stamp + "-" + content_hash[:10]
    source = {
        "schema_version": 1, "snapshot_id": snapshot_id,
        "observed_at": list_provenance["fetched_at"],
        "publication_status": "research_snapshot",
        "licence_status": "Current API data reuse terms require confirmation before public republication.",
        "source_provenance": [list_provenance, counts_provenance],
        "normalization": "Selected public fields and plain description text. Media links omitted.",
        "project_count": len(projects), "source_counts": counts, "projects": projects
    }
    graph_value = graph(projects, snapshot_id)
    directory = ROOT / "data" / "snapshots" / snapshot_id
    write_json(directory / "projects.json", source)
    write_json(directory / "graph.json", graph_value)
    validation = {
        "snapshot_id": snapshot_id,
        "project_count_matches_source": True,
        "level_count_total": sum(counts.get("levels", {}).values()),
        "source_project_total": counts["total"],
        "level_counts_cover_all_projects": sum(counts.get("levels", {}).values()) == counts["total"],
        "note": "Differences in level counts are recorded without inventing missing classifications."
    }
    write_json(directory / "validation.json", validation)
    manifest_path = ROOT / "data" / "manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"snapshots": []}
    snapshots = previous["snapshots"] + [{"snapshot_id": snapshot_id, "observed_at": source["observed_at"], "project_count": len(projects)}]
    if include_history:
        commit_body, commit_provenance = fetch(HISTORY_URL)
        commit = json.loads(commit_body)[0]
        commit_id = commit["sha"]
        commit_time = commit["commit"]["committer"]["date"]
        legacy_url = "https://raw.githubusercontent.com/OWASP/www-project-threat-dragon/" + commit_id + "/index.md"
        legacy_body, legacy_provenance = fetch(legacy_url)
        write_json(ROOT / "data" / "historical" / "threat-dragon-2020.json", {
            "source_system": "GitHub project website source",
            "repository": "OWASP/www-project-threat-dragon",
            "commit_sha": commit_id, "source_committed_at": commit_time,
            "captured_at": legacy_provenance["fetched_at"], "source_url": legacy_url,
            "source_provenance": [commit_provenance, legacy_provenance],
            "content_format": "jekyll_markdown", "content": legacy_body.decode(),
            "coverage": "One historical project index. This does not establish full historical site coverage.",
            "licence_status": "Confirm licence at this repository revision before public republication."
        })
    write_json(manifest_path, {"schema_version": 1, "latest_snapshot": snapshot_id, "last_successful_capture_at": source["observed_at"], "snapshots": snapshots})
    print(json.dumps({"snapshot_id": snapshot_id, "projects": len(projects), "nodes": len(graph_value["nodes"]), "edges": len(graph_value["edges"]), "historical_sample_requested": include_history}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-history", action="store_true")
    capture(parser.parse_args().include_history)
