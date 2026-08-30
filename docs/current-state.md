# Servotab Current State

Last reconciled: `2026-08-31`

This is the volatile status surface. It records what has actually crossed each boundary; it does not replace the durable product contract in `README.md` or the repository contract in `AGENTS.md`.

## At a glance

| Surface | Current state | Evidence boundary |
|---|---|---|
| Product identity | `Servotab` adopted | Current source, manifest, assets, site, and docs use the new identity |
| Source candidate | `0.4.0-rc1` on public `main` | Core migration PR #7 merged as `f110fbcd`; source-checkout/site documentation follow-up is pending, with no tag or GitHub Release claim |
| Canonical methods | 12 current methods | `methods/*.md` plus `scripts/skill_catalog.py` |
| Plugin package | Generated candidate | `plugins/servotab/` with one router, 12 leaves, and curated assets |
| Deterministic package gate | Green on integrated 43-file payload | Generation/sync, YAML, manifest, expanded migration selftest, public-tree audit, and Python compilation passed locally |
| Repo marketplace | Defined | `.agents/plugins/marketplace.json`; selector `servotab@personal` |
| Live Codex install | Installed, enabled, and cache-exact | `servotab@personal` `0.4.0-rc1` was freshly reinstalled from this checkout; source/cache contain the exact 43-file payload, fresh-process prompt input exposes `servotab:servotab`, and a fresh normal task exercised both implicit router and explicit-leaf behavior |
| Legacy global layer | Retired; both supported roots clear | Thirteen reachable LIFO layers under `~/.codex/skills` were retired one at a time after independent review; no active pointer or `soft-*` entrypoint remains |
| Field Lab | Schema v2 source subject | `fieldlab-pack.json` points to `plugins/servotab/skills`; live model eval not run |
| Website source | Astro static site implemented | Source/build routes are separate from edge and custom-domain proof |
| Cloudflare Pages | Production candidate live | Direct-upload deployment `0380fdb1-5782-45af-af1e-b8bc947484ca`; automatic deployments disabled; Dashboard reports the historical Git connection is disconnected |
| `servotab.com` | Active; SSL enabled | Proxied apex DNS, Pages custom-domain status, public HTTPS, strict headers, interaction smoke, and true 404 all verified |
| Canonical redirects | Active | `www.servotab.com` and `servotab.pages.dev` return 301 to `https://servotab.com` while preserving path suffix and query string |
| GitHub repository | Renamed to `IndelibleVivi/servotab` | New URL is live, the old `/softpowers` URL returns a 301 redirect, and public `main` now contains the Servotab package and website source |
| Git publication | Core migration merged | PR #7 merged as `f110fbcd`; post-merge Validate run `33340000993` succeeded, while the public-availability docs PR, tag, and GitHub Release remain separate |
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

Automatic deployments remain disabled, and the Cloudflare Dashboard reports that the historical Git connection is disconnected. The current production candidate was therefore deployed directly from the reviewed local build. Deployment `0380fdb1-5782-45af-af1e-b8bc947484ca` is live through `https://servotab.com`; its Cloudflare source marker remains `73ada46 dirty candidate`, which is deployment provenance rather than a clean commit or release claim.

The apex has a proxied CNAME to `servotab.pages.dev`. Pages reports the custom domain as active with SSL enabled, and fresh public requests prove the canonical host, strict headers, correct content, finite interaction state, narrow-width no-overflow behavior, and a true 404 with `no-store`.

Cloudflare account configuration now contains the two-entry list `servotab_canonical_hosts` and enabled rule `servotab_canonical_redirects`. A proxied `www` trigger record is present. Fresh edge requests prove both `www.servotab.com` and `servotab.pages.dev` return 301 to the apex while preserving subpaths and query strings; following either redirect reaches a 200 response on `servotab.com`.

The deployed site still labels the repository as historical/preceding source because the public-availability copy has not yet been merged and redeployed. Domain-level redirects remain Cloudflare account configuration, not `site/public/_redirects` behavior.

## GitHub and publication

The public repository was renamed in place and now resolves at:

```text
https://github.com/IndelibleVivi/servotab
```

The local `origin` uses `git@github-faye:IndelibleVivi/servotab.git`. GitHub returns a 301 from the old `/softpowers` URL, preserving the historical route. Core migration PR #7 merged to public `main` as `f110fbcd`, and the merge commit's Validate run `33340000993` completed successfully.

The public default branch now contains `.agents/plugins/marketplace.json`, `plugins/servotab/`, and the layered licensing files, so source-checkout clone commands and `blob/HEAD` legal links can resolve against the current Servotab source. The prepared README and website availability copy remains a separate follow-up PR until its own CI and merge are observed. Do not describe that follow-up merge, tag, release, OpenAI submission, or OpenAI listing until the exact action and result are verified.

## Remaining acceptance work

1. Retain the inactive legacy manifests, backups, and transitional helper until the documented recovery/operator dependency is deliberately retired; do not manually clean historical receipts.
2. Close the prepared source-install and website cutover copy through its follow-up PR/CI/merge, then reconnect or deliberately replace the Cloudflare Git integration and deploy a clean merged commit. Keep automatic production deployments disabled unless separately chosen.
3. Stop before OpenAI directory submission until the owner explicitly opens that gate.

Update this file by replacing superseded facts, not by appending a development diary.
