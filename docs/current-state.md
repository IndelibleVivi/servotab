# Servotab Current State

Last reconciled: `2026-08-31`

This is the volatile status surface. It records what has actually crossed each boundary; it does not replace the durable product contract in `README.md` or the repository contract in `AGENTS.md`.

## At a glance

| Surface | Current state | Evidence boundary |
|---|---|---|
| Product identity | `Servotab` adopted | Current source, manifest, assets, site, and docs use the new identity |
| Source candidate | `0.4.0-rc1` on public `main` | Core migration PR #7 merged as `f110fbcd`; public-availability PR #8 merged as `9e5213d`; no tag or GitHub Release exists |
| Canonical methods | 12 current methods | `methods/*.md` plus `scripts/skill_catalog.py` |
| Plugin package | Generated candidate | `plugins/servotab/` with one router, 12 leaves, and curated assets |
| Deterministic package gate | Green on integrated 43-file payload | Generation/sync, YAML, manifest, expanded migration selftest, public-tree audit, and Python compilation passed locally |
| Repo marketplace | Defined | `.agents/plugins/marketplace.json`; selector `servotab@personal` |
| Live Codex install | Installed, enabled, and cache-exact | `servotab@personal` `0.4.0-rc1` was freshly reinstalled from this checkout; source/cache contain the exact 43-file payload, fresh-process prompt input exposes `servotab:servotab`, and a fresh normal task exercised both implicit router and explicit-leaf behavior |
| Legacy global layer | Retired; both supported roots clear | Thirteen reachable LIFO layers under `~/.codex/skills` were retired one at a time after independent review; no active pointer or `soft-*` entrypoint remains |
| Field Lab | Schema v2 source subject | `fieldlab-pack.json` points to `plugins/servotab/skills`; live model eval not run |
| Website source | Astro static site implemented | Source/build routes are separate from edge and custom-domain proof |
| Cloudflare Pages | Production site live from clean merged source | Direct-upload deployment `fa58ada7-191a-4fe1-a1dc-7071d548654e` records source `9e5213d` with a clean workspace marker; automatic production and preview deployments are disabled, while the historical Git connection remains disconnected |
| `servotab.com` | Active; SSL enabled | Proxied apex DNS, Pages custom-domain status, public HTTPS, strict headers, interaction smoke, and true 404 all verified |
| Canonical redirects | Active | `www.servotab.com` and `servotab.pages.dev` return 301 to `https://servotab.com` while preserving path suffix and query string |
| GitHub repository | Renamed to `IndelibleVivi/servotab` | New URL is live, the old `/softpowers` URL returns a 301 redirect, and public `main` now contains the Servotab package and website source |
| Git publication | Core migration and public availability merged | PR #7 merged as `f110fbcd` with post-merge Validate run `33340000993`; PR #8 merged as `9e5213d` with post-merge run `33340162537`; tag and GitHub Release remain separate |
| OpenAI directory | Not submitted | Submission and publication remain owner-gated |

## Source and package

The current architecture is plugin-native:

```text
methods/*.md + scripts/skill_catalog.py
        → scripts/build_skills.py
        → plugins/servotab/skills/**
        → PACK_MANIFEST.json

.agents/plugins/marketplace.json
        → servotab@personal
        → plugins/servotab
```

Current method ids are `design`, `spec-chain`, `plan`, `execute`, `debug`, `tdd`, `review`, `review-feedback`, `verify`, `worktree`, `delegate`, and `finish`. The only implicit-eligible skill is `servotab`.

The old root `skills/` projection and transaction installer are retired from current source. The local marketplace `personal` has been added from this checkout, and `servotab@personal` `0.4.0-rc1` is installed and enabled. A final remove/add refresh produced an exact 43-file source/cache match with two curated assets and plugin-local rights files.

The integrated 43-file package passes source/generated sync, exact skill validation, manifest freshness, expanded packaging/migration selftests, public-tree audit, Python compilation, and Field Lab v2 `validate` / `selftest` / `list` with zero target-agent invocations.

Independent review closed with no actionable P0–P2 findings in the repaired retirement helper. The verified 13-layer live chain was then retired against the exact root `~/.codex/skills`, one LIFO layer per invocation with a fresh read-only preflight before each layer. Both supported roots now report `CLEAR`; the active pointer and all top-level `softpowers` / `soft-*` entrypoints are absent. Nineteen historical manifest receipts remain with status `uninstalled`, and no modified-skill snapshot was needed.

A fresh-process `codex debug prompt-input` probe now includes the implicit router as `servotab:servotab` and includes no legacy Softpowers skill. The 12 leaves remain explicit-only by `agents/openai.yaml` policy, like first-party router/specialist plugins; they are intentionally omitted from the baseline implicit catalog.

A normal newly opened Codex worktree task then received an ordinary-language, read-only regression-test question with no named skill invocation. It loaded `servotab:servotab`, kept the task narrow, and routed the evidence question through the debug and TDD references without editing the checkout. A follow-up explicit `$review` invocation entered the review leaf and returned one verified P2 contract finding against the prior recommendation. This is a named local behavior receipt, not a claim about other machines or general longitudinal quality.

## Website and Cloudflare

The website source under `site/` contains the canonical static routes:

```text
/
/docs
/methods
/lineage
/support
/privacy
/terms
/404
```

Automatic production and preview deployments are disabled: `production_deployments_enabled` is `false`, `preview_deployment_setting` is `none`, and the deprecated aggregate deployment switch is also `false`. The Cloudflare Dashboard reports that the historical Git connection is disconnected, and the stored Git source label still references `IndelibleVivi/softpowers`. The existing Pages project was not disconnected, recreated, or switched to a different topology.

Production deployment `fa58ada7-191a-4fe1-a1dc-7071d548654e` was uploaded with Wrangler 4.127.1 from an isolated clean worktree at merged commit `9e5213d80bae1339438efd7d0dd19c9810ad3a7d`, with `commit-dirty=false`. Cloudflare records source `9e5213d` and message `Deploy merged Servotab site from PR #8`; the deployment is live through `https://servotab.com`.

The apex has a proxied CNAME to `servotab.pages.dev`. Pages reports the custom domain as active with SSL enabled. Fresh post-deployment public requests and rendered checks prove the canonical host, strict headers, current repository/install copy, desktop and 390-pixel no-overflow behavior, mobile-menu open/close behavior, and a true 404 with `no-store`. The PR #8 website change was limited to copy and repository configuration; motion and invoke-interaction code were unchanged from the preceding accepted receipt.

Cloudflare account configuration now contains the two-entry list `servotab_canonical_hosts` and enabled rule `servotab_canonical_redirects`. A proxied `www` trigger record is present. Fresh edge requests prove both `www.servotab.com` and `servotab.pages.dev` return 301 to the apex while preserving subpaths and query strings; following either redirect reaches a 200 response on `servotab.com`.

The deployed site now points Source and Issues to `IndelibleVivi/servotab`, publishes the current source-checkout installation route, and keeps tag, GitHub Release, OpenAI listing, and OpenAI approval claims explicitly separate. Domain-level redirects remain Cloudflare account configuration, not `site/public/_redirects` behavior.

## GitHub and publication

The public repository was renamed in place and now resolves at:

```text
https://github.com/IndelibleVivi/servotab
```

The local `origin` uses `git@github-faye:IndelibleVivi/servotab.git`. GitHub returns a 301 from the old `/softpowers` URL, preserving the historical route. Core migration PR #7 merged to public `main` as `f110fbcd`, and its post-merge Validate run `33340000993` completed successfully. Public-availability PR #8 then merged as `9e5213d`, and post-merge Validate run `33340162537` also completed successfully.

The public default branch now contains `.agents/plugins/marketplace.json`, `plugins/servotab/`, the layered licensing files, and the merged README/website availability copy. Source-checkout clone commands and `blob/HEAD` legal links therefore resolve against current Servotab source. No tag or GitHub Release has been created, and no OpenAI submission or listing has occurred.

## Remaining boundaries

1. Retain the inactive legacy manifests, backups, and transitional helper until the documented recovery/operator dependency is deliberately retired; do not manually clean historical receipts.
2. Keep the current Cloudflare production path on clean manual direct deployments while the historical Git binding remains disconnected and stale. Repairing or replacing that binding, recreating the project, or re-enabling automatic deployments is a separate owner decision, not a hidden follow-up to this deployment.
3. Tag and GitHub Release creation remain unperformed and separate from the merged source candidate.
4. Stop before OpenAI directory submission until the owner explicitly opens that gate.

Update this file by replacing superseded facts, not by appending a development diary.
