# OWASP organisation research foundation

Prepared for PrompTugal on 22 November 2026.

This repository captures a working example of public OWASP project metadata, a graph derived from explicit fields, and historical website source samples. The intended product combines an OWASP-style directory, graph exploration and dated historical search.

## Verified access

- https://owasp.org/api/public/projects/counts
- https://owasp.org/api/public/projects/list?limit=1000

Both returned HTTP 200 and Access-Control-Allow-Origin * when requested with Origin https://data.promptugal.news. These are endpoints used by the current public website, without a documented stability commitment established in this research. The homepage HTML has different cross-origin and iframe restrictions.

The first capture contains 347 project records. The graph contains 825 nodes and 1,154 explicit-field edges. A shared category groups projects. It does not establish that those projects integrate with one another.

The historical example retrieves the Threat Dragon project index from commit d5472040d2f595b92924823551a05bc4cd31521f, committed on 31 December 2020. Its retrieval date is recorded separately from the commit date.

## Capture and update

Run Python 3 with the standard library.

    python scripts/capture.py
    python scripts/capture.py --include-history
    python scripts/index_wiki.py
    python scripts/search_history.py "testing"

A successful capture checks project identifiers and reconciles the returned list with the count endpoint. It writes a new dated snapshot and updates the manifest. Failed captures should leave the last successful published version available. Source changes to pagination or schema require review.

The supplied GitHub Actions workflow proposes a daily capture at 06:00 UTC and supports manual runs. It becomes active when installed in a repository with Actions and write permission enabled. This local package has no remote configured and no active unattended schedule.

## Repository contents

- data/manifest.json records available snapshots and the latest successful capture.
- data/snapshots/<id>/projects.json stores selected source fields, descriptions and provenance.
- data/snapshots/<id>/graph.json stores explicit project relationships.
- data/snapshots/<id>/validation.json records validation evidence.
- data/historical/threat-dragon-2020.json contains one historical source file.
- data/historical/wiki-catalogue.json indexes 7,265 old wiki Markdown document paths at a pinned archive revision.
- data/historical/wiki-testing-tools-sample.json preserves one recovered wiki page.
- scripts/capture.py provides the collector.
- scripts/index_wiki.py refreshes the archive catalogue and sample.
- scripts/search_history.py searches catalogue titles and the two captured page bodies.
- .github/workflows/capture.yml provides the proposed update job.

Media URLs are omitted because some public records contain expiring signed links. The selected fields and plain descriptions support indexing and graph construction. A complete visual reconstruction needs separate source HTML, assets, styles and applicable permission checks.

## Hybrid product design

Serve a stored snapshot first. Fetch live public metadata on request where CORS permits and show the result alongside the dated snapshot. Compare a live response before replacing stored data. Preserve existing snapshots.

Show captured_at or observed_at for collection, source_updated_at where the source supplies it, and last_successful_check_at for freshness. A recent retrieval of an old document does not establish a recent content change.

Give projects stable identities that span old wiki paths, GitHub website repositories and current CMS slugs. Retain mappings with evidence and review ambiguous matches.

Index every stored document version with title, plain text, era, source URL, source revision, snapshot ID and timestamps. Search can then target the current snapshot, a selected date or every indexed version. Store explicit graph relations separately from inferred semantic connections, with evidence and inference method on each edge.

## Historical sources and limits

The current CMS, old GitHub/Jekyll repositories and older MediaWiki site are separate source systems. The wiki returned HTTP 403 during this research. OWASP's September 2026 board minutes discuss retiring it and preserving a static archive.

Git history is useful where commits remain available. OWASP/www-community documents a July 2020 history rewrite, so completeness must be checked. Threat Dragon's current FAQ says old project website repositories were scheduled for deletion by the end of 2026. Preserve permitted material while accessible.

Archive replay and re-rendering recovered content are different deliverables. Label the available coverage, source date and any missing assets. An accessible Markdown conversion at OWASP-Foundation/OWASP-wiki-md was indexed at commit e46e3386c68cd4e3d0a3ccf4d8725c40e24e2345. It contains 7,265 Markdown paths. One Testing Tools page was downloaded successfully. This is an archive candidate with source terms to review. Its completeness and original page-by-page wiki revision history have not been established. The search script covers all catalogue titles and only the two locally captured full-text samples.

## Rights and policy

The project's stated publishing purpose is noncommercial with full attribution. Confirm applicable reuse terms for each source, including the current public API and each historical revision. The old main site repository declares CC BY-SA 4.0. That declaration alone does not establish a blanket licence for all current CMS data and media.

Treat this package as a research snapshot pending source-specific public republication review. Graph generation does not change the underlying content rights.

Map source access, allowed transformations, conflict handling, publication and evidence retention to the team's actual RiskMandate Agent Behaviour Policies. Store policy version, action, decision and evidence with workflow runs. Client-side rules can guide the reader. Shared publishing permissions require enforcement by the writer.

## Sources

- https://owasp.org/projects
- https://owasp.org/projects/threat-dragon?tab=faqs
- https://owasp.org/board/meetings/202609
- https://github.com/OWASP/owasp.github.io
- https://github.com/OWASP/www-community
- https://github.com/OWASP/Nest
- https://github.com/OWASP/nest-sdk-python

- https://github.com/OWASP-Foundation/OWASP-wiki-md
