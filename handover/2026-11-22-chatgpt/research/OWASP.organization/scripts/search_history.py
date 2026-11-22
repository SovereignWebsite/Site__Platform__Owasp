"""Search archived document titles and the locally captured historical page bodies."""
import argparse
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("query")
parser.add_argument("--limit", type=int, default=15)
args = parser.parse_args()
query = args.query.casefold()
catalogue = json.loads((root / "data/historical/wiki-catalogue.json").read_text())
matches = [
    {"match_type": "archived_title", "title": item["title"], "source_url": item["raw_url"],
     "source_revision": catalogue["source_revision"]}
    for item in catalogue["documents"] if query in item["title"].casefold()
]
for path in (root / "data/historical").glob("*.json"):
    item = json.loads(path.read_text())
    content = item.get("content", "")
    position = content.casefold().find(query)
    if position >= 0:
        matches.append({"match_type": "captured_full_text", "title": path.stem,
                        "source_url": item["source_url"],
                        "excerpt": content[max(0, position - 70):position + 180]})
print(json.dumps({"query": args.query, "total_matches": len(matches),
                  "coverage": "All archived catalogue titles and two locally captured page bodies.",
                  "results": matches[:max(0, args.limit)]}, indent=2))
