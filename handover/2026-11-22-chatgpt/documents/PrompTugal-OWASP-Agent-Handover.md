# PrompTugal-OWASP-Agent-Handover

Text extraction of the accompanying Word document. Preserve its sources and limitations.

PrompTugal source explorer agent handover

OWASP data and history with a Spotify access review

Prepared 22 November 2026 for the implementing agent and PrompTugal data team.

Outcome and access

Use the accompanying research website and source package to implement a reusable service for captured public content, alternative designs, project relationships and historical discovery. The intended ecosystem is data.promptugal.news serving sites listed through hub.sovereignweb.site.

Open the private research website

The website provides a captured project directory, graph exploration, archive title search, two captured historical page bodies, live browser requests and downloadable handover materials. Its layout is an independent research explorer. A precise recreation of the complete OWASP site remains a separate implementation task.

Confirmed requirements

Combine stored JSON snapshots with live requests to permitted upstream sources. Keep dated versions in a repository.

Make project discovery the first use case. Support a directory, an evidence-based graph and historical search.

Show capture time, source update time and last successful check as different values.

Demonstrate PrompTugal workflows and actual RiskMandate Agent Behaviour Policies with traceable decisions and evidence.

Use the stated noncommercial publishing purpose and full source attribution while retaining each source’s applicable licence.

Verified foundation

Item | Evidence
Current project data | 347 project records captured from the OWASP public list endpoint. List and count endpoints returned HTTP 200 and Access-Control-Allow-Origin *. [1]
Graph | 825 nodes and 1,154 edges derived from published categories, maturity labels and resource URLs. Each edge identifies its evidence field and snapshot.
Old wiki catalogue | 7,265 Markdown document paths indexed at a pinned revision of OWASP-Foundation/OWASP-wiki-md. One page was downloaded. [2]
Historical project page | Threat Dragon index retrieved from commit d5472040d2f595b92924823551a05bc4cd31521f, dated 31 December 2020.
Collector | Python standard-library collector, validation output, historical catalogue script, search script and proposed daily GitHub Actions workflow.

The captured source counts identify 347 projects while the returned maturity-level counts sum to 331. Preserve this discrepancy as validation evidence and inspect classification coverage.

Architecture and source access

Serve the latest successful snapshot as the initial experience. Provide a deliberate live refresh where browser CORS permits. Generate graphs and search indexes from stored records. Retain the source response identity, transformations and validation evidence for reproducibility.

OWASP’s homepage response and public data endpoints have different access behaviour. The homepage had no cross-origin read permission and denied iframe embedding. The public project list and counts endpoints returned permissive CORS headers. Treat these as observed website endpoints whose stability and current reuse terms still need confirmation. [1]

OWASP Nest provides another project discovery source and API SDKs. The SDK documentation shows an API key requirement. Its code licence alone does not establish a blanket licence for all upstream data. [3]

Repository and collection

The data package uses the working repository name OWASP.organization. It contains data/manifest.json, immutable data/snapshots directories, historical examples and scripts. The collection workflow is configured for 06:00 UTC daily and manual invocation. It is inactive until connected to the destination GitHub repository.

The implementing agent should run the collector through the intended writer, inspect a successful snapshot, exercise failure handling, and verify persistence before activating unattended publication. A failed fetch should leave the last successfully published version available. Preserve failure and retry evidence.

Time and historical search

Keep observed_at or captured_at for retrieval, source_updated_at where supplied and last_successful_check_at for freshness.

Use stable identities to connect old wiki paths, GitHub repositories and current CMS slugs. Retain the evidence for ambiguous identity mappings.

Index document title, source text, era, revision, URL, snapshot ID and timestamps. Expose the actual indexed coverage in search results.

Support source-version browsing and differences between recovered versions. Original-page appearance needs its assets, styles and templates.

The archive host returned HTTP 403 in this environment. A separate Markdown archive was accessible. Original wiki page revision history and completeness remain unverified. OWASP board minutes discuss preserving a static wiki archive, and the community repository documents a July 2020 history rewrite. [2,4,5]

Graph semantics

Published field relationships are the first graph layer. Inferred topical or integration links should retain their method, evidence and review state. Record when a relationship was observed and which snapshot supports it. A shared category can group projects without asserting that they integrate.

Implementing agent brief

The following instructions are suitable for Claude or another coding agent. An earlier decision to use Claude could not be confirmed in the conversation available here.

Inspect the research package and reproduce the capture locally. Confirm the current upstream response shape and source-specific reuse terms.

Inspect the website source. Preserve working directory filters, graph evidence, archive search, download links and browser fetch error states.

Confirm the destination repository, owning account and publishing permissions. Keep credentials outside source files and distributed archives.

Expand historical full-text ingestion with a coverage register, source revision mapping and explicit missing-content handling.

Add source-version selection and document comparison as additional versions become available. Avoid presenting dates with no recovered content.

Map workflow events to the team’s supplied RiskMandate policy definitions. Verify a normal run, a conflicting record and a retry.

Activate the scheduled collector only after verifying its actual destination writer and readback. Confirm whether 06:00 UTC daily is suitable.

RiskMandate evidence

For each meaningful agent action, capture the policy identifier and version, requested action, decision, supporting evidence, any required approval and resulting action. Link public explanations to the actual workflow and dataset version. Source rules and publication authority require enforcement at the relevant writer.

Remaining decisions and limitations

Current OWASP API stability and public republication terms require confirmation.

The Markdown archive’s coverage, provenance and source-content licences need review before wider republication.

Full-text search currently covers two stored page bodies. The 7,265-document catalogue supports title search and direct on-demand source retrieval.

The site supports one captured project snapshot. A longer timeline requires additional scheduled captures or recovered historical records.

Precise reconstruction of older visual designs requires historical styles, templates and assets.

Policy definitions, enforcement integration and an active unattended collection destination remain to be supplied.

Source package navigation

Run scripts/capture.py to collect projects, scripts/capture.py --include-history for the historical project sample, scripts/index_wiki.py for the archive catalogue, and scripts/search_history.py with a query for local historical search. Read README.md for provenance, rights and known coverage limits.

Spotify browser and connector review

A private browser application can access supported Spotify user data after OAuth authorisation. Spotify recommends Authorization Code with PKCE for browser clients. The application needs a registered client ID, exact redirect URI, appropriate scopes and the user’s consent. [6]

Route | Capability and limits
Browser Web API | Supported account, playlist, library and recent-play data subject to endpoint availability, scopes and quota. A signed-in Spotify tab does not itself grant another site API access. [6,7]
MCP connector | Exposes the functions implemented by that connector. Authentication, permissions, quotas and upstream terms still apply. No Spotify plugin was returned by the plugin search available in this session.
User data export | Spotify provides JSON account export packages. Extended streaming history is documented as covering the account lifetime. Select relevant files and fields for the private use case. [8]

Development mode currently requires a Premium app owner and permits up to five allowlisted users. Since July 2026, development-app quotas are shared across a developer account’s client IDs. Confirm app mode and current quotas before implementation. [9,10]

Spotify policy restricts content analysis, standalone metadata services, reproducing its core experience and ingesting Spotify Content into AI models. Confirm the exact feature and any required permissions before adapting the OWASP graph or archive workflow. Noncommercial operation still requires those terms. [11]

The recently played endpoint is a limited recent-history feed. Use the documented account export route when investigating a longer historical record. No Spotify account connection or authenticated request has been exercised here. [7,8]

Next technical proof

Implement a private browser page that authorises through PKCE and displays a small supported account dataset with minimum scopes. Keep Spotify credentials and personal data out of the public OWASP source repository. Review any planned agent processing of retrieved content against Spotify’s policy. The agent may use the developer documentation to implement the integration. [6,11,12]

Research sources

1  OWASP project directory and public endpoints

2  Old wiki Markdown conversion

3  OWASP Nest Python SDK

4  September 2026 OWASP board minutes

5  OWASP community repository and history note

6  Spotify authorisation

7  Spotify recently played endpoint

8  Spotify account exports

9  Spotify quota modes

10  July 2026 quota changes

11  Spotify Developer Policy

12  Spotify guidance on building with AI

## Linked sources

- https://promptugal-owasp-source-explorer.diniscruz.chatgpt.site
- https://owasp.org/projects
- https://github.com/OWASP-Foundation/OWASP-wiki-md
- https://github.com/OWASP/nest-sdk-python
- https://owasp.org/board/meetings/202609
- https://github.com/OWASP/www-community
- https://developer.spotify.com/documentation/web-api/concepts/authorization
- https://developer.spotify.com/documentation/web-api/reference/get-recently-played
- https://support.spotify.com/us/article/understanding-your-data/
- https://developer.spotify.com/documentation/web-api/concepts/quota-modes
- https://developer.spotify.com/blog/2026-07-23-web-api-quota-updates
- https://developer.spotify.com/policy
- https://developer.spotify.com/documentation/web-api/tutorials/building-with-ai