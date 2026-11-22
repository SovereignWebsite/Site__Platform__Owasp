"""Index an accessible Markdown conversion of the old OWASP wiki."""
import json
from urllib.parse import quote
from capture import ROOT, fetch, write_json

REPOSITORY = "OWASP-Foundation/OWASP-wiki-md"
commit_body, commit_provenance = fetch("https://api.github.com/repos/" + REPOSITORY + "/commits/master")
commit = json.loads(commit_body)
revision = commit["sha"]
tree_body, tree_provenance = fetch("https://api.github.com/repos/" + REPOSITORY + "/git/trees/" + revision + "?recursive=1")
tree = json.loads(tree_body)
if tree.get("truncated"):
    raise ValueError("Incomplete GitHub tree. Review pagination before indexing.")
documents = [
    {"path": entry["path"], "title": entry["path"].removesuffix(".md").replace("_", " "),
     "source_blob_sha": entry["sha"],
     "raw_url": "https://raw.githubusercontent.com/" + REPOSITORY + "/" + revision + "/" + quote(entry["path"], safe="/")}
    for entry in tree["tree"]
    if entry["type"] == "blob" and entry["path"].endswith(".md")
]
index = {
    "source_system": "Markdown conversion of old OWASP wiki",
    "repository": REPOSITORY, "source_revision": revision,
    "source_committed_at": commit["commit"]["committer"]["date"],
    "captured_at": tree_provenance["fetched_at"],
    "source_provenance": [commit_provenance, tree_provenance],
    "licence_status": "Review conversion repository licence and source page terms before public republication.",
    "coverage": "Catalogue of available Markdown files at this revision. Original wiki revision history and completeness are unverified.",
    "documents": documents
}
write_json(ROOT / "data" / "historical" / "wiki-catalogue.json", index)
sample = next(item for item in documents if item["path"] == "Appendix_A:_Testing_Tools.md")
body, provenance = fetch(sample["raw_url"])
write_json(ROOT / "data" / "historical" / "wiki-testing-tools-sample.json", {
    "source_system": index["source_system"], "source_revision": revision,
    "source_committed_at": index["source_committed_at"],
    "source_url": sample["raw_url"], "source_provenance": provenance,
    "content_format": "markdown", "content": body.decode(),
    "licence_status": index["licence_status"]
})
print(json.dumps({"wiki_documents_indexed": len(documents), "source_revision": revision, "sample_characters": len(body)}))
