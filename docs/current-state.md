# Servotab Current State

Last reconciled: `2026-08-31`

This is the volatile status surface. It records what has actually crossed each boundary; it does not replace the durable product contract in `README.md` or the repository contract in `AGENTS.md`.

## At a glance

| Surface | Current state | Evidence boundary |
|---|---|---|
| Product identity | `Servotab` adopted | Current source, manifest, assets, site, and docs use the new identity |
| Source candidate | `0.4.0-rc1` on public `main` | Public-release hardening commit `0f7e73d` from PR #14 is present on public `main`; merge-commit Validate run `33359648427` passed all five jobs; no Servotab tag or GitHub Release exists |
| Canonical methods | 12 current methods | `methods/*.md` plus `scripts/skill_catalog.py` |
| Plugin package | Generated candidate | `plugins/servotab/` with one router, 12 leaves, and curated assets |
| Deterministic package gate | Green on integrated 43-file payload | Generation/sync, YAML, manifest, expanded migration selftest, public-tree audit, Python compilation, and the Astro production build passed locally and in CI |
| Repo marketplace | Defined | `.agents/plugins/marketplace.json`; selector `servotab@personal` |
| Live Codex install | Installed, enabled, and cache-exact | `servotab@personal` `0.4.0-rc1` was freshly reinstalled from this checkout; source/cache contain the exact 43-file payload, fresh-process prompt input exposes `servotab:servotab`, and a fresh normal task exercised both implicit router and explicit-leaf behavior |
| Legacy global layer | Retired; both supported roots clear | Thirteen reachable LIFO layers under `~/.codex/skills` were retired one at a time after independent review; no active pointer or `soft-*` entrypoint remains |
| Field Lab | Schema v2 source subject | `fieldlab-pack.json` points to `plugins/servotab/skills`; live model eval not run |
| Website source | Astro static site implemented and polished | Homepage, source-checkout Quickstart and install receipt, task examples, social preview, security route, support, privacy, terms, and lineage are current on public `main` |
| Cloudflare Pages | Production site live from clean merged source | Direct-upload deployment `6a6dc17d-70ac-4905-b6b3-baba93a8ad29` was built and uploaded from clean merge commit `b2bacde`; automatic production and preview deployments remain disabled, while the historical Git connection remains disconnected |
| `servotab.com` | Active; SSL enabled; RUM injection disabled | Proxied apex DNS, Pages custom-domain status, public HTTPS, strict headers, live interaction and responsive checks, same-origin script/network proof, and true 404 all verified |
| Canonical redirects | Active | `www.servotab.com` and `servotab.pages.dev` return 301 to `https://servotab.com` while preserving path suffix and query string |
| GitHub repository | Renamed to `IndelibleVivi/servotab` | New URL is live, the old `/softpowers` URL returns a 301 redirect, and public `main` now contains the Servotab package and website source |
| GitHub governance | Private reporting and protected `main` active | Private Vulnerability Reporting and merged-branch deletion are enabled; active ruleset `Protect main` requires PRs plus five current CI contexts and retains an explicit owner emergency bypass |
| Git publication | Migration, public availability, deployment state, directory-readiness polish, site experience, and public-release hardening merged | The listed milestone PRs are on public `main`; PR #14 merged as `b2bacde` with post-merge Validate run `33359648427`; tag and GitHub Release remain separate |
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

Production deployment `6a6dc17d-70ac-4905-b6b3-baba93a8ad29` was uploaded with Wrangler 4.127.1 from an isolated clean worktree at merged commit `b2bacde481a50a9d617d8088f43d95ec72142639`, with message `Harden public release surfaces`. The deployment-list readback records environment `Production`, branch `main`, and source `b2bacde`; it is live through `https://servotab.com`.

The apex has a proxied CNAME to `servotab.pages.dev`. Pages reports the custom domain as active with SSL enabled. Fresh post-deployment public requests and rendered checks prove the canonical host, strict headers, current visitor-journey copy, 1440-pixel desktop and 390-pixel mobile no-overflow behavior, a 44-pixel mobile-menu target with working navigation, current Docs and Support routes, the 1200 × 630 social image, and zero browser console errors or warnings. Earlier accepted checks continue to cover invoke/return interaction, reduced-motion behavior, and a true 404 with `no-store`.

Cloudflare Configuration Rule `servotab_disable_rum` is active for all incoming requests with action `disable RUM`. A fresh real-browser load exposes only the same-origin `/method-motion.js` script and same-origin page resources, with no Cloudflare Insights script or beacon request and zero console errors or warnings. The edge rule leaves the published `script-src 'self'` CSP, ordinary page caching, and fallback 404 caching contract unchanged.

Cloudflare account configuration now contains the two-entry list `servotab_canonical_hosts` and enabled rule `servotab_canonical_redirects`. A proxied `www` trigger record is present. Fresh edge requests prove both `www.servotab.com` and `servotab.pages.dev` return 301 to the apex while preserving subpaths and query strings; following either redirect reaches a 200 response on `servotab.com`.

The deployed site now points Source and Issues to `IndelibleVivi/servotab`, publishes a first-use source-checkout Quickstart plus installed/enabled and observed `codex-cli 0.147.0` receipts, explains the one-router/twelve-explicit-leaf topology and skills-only trust boundary, links the active private security-reporting route, and serves the deterministic wide social preview. It keeps tag, GitHub Release, OpenAI listing, and OpenAI approval claims explicitly separate. Domain-level redirects and the RUM opt-out remain Cloudflare account configuration, not `site/public/_redirects` or `site/public/_headers` behavior.

## GitHub and publication

The public repository was renamed in place and now resolves at:

```text
https://github.com/IndelibleVivi/servotab
```

The local `origin` uses `git@github-faye:IndelibleVivi/servotab.git`. GitHub returns a 301 from the old `/softpowers` URL, preserving the historical route. Core migration PR #7 merged as `f110fbcd` with post-merge run `33340000993`; public-availability PR #8 merged as `9e5213d` with run `33340162537`; live-state PR #9 merged as `9085f56` with run `33342268739`; directory-readiness PR #10 merged as `e53dcbc` with run `33344979371`; site-experience PR #11 merged as `c656ad7` with run `33349866213`; and public-release-hardening PR #14 merged as `b2bacde` with run `33359648427`. All listed runs completed successfully.

Private Vulnerability Reporting is enabled and the repository security policy points to its active advisory route. Merged pull-request branches are deleted automatically. Repository ruleset `Protect main` (`21900625`) is active on the default branch: updates require a pull request, current strict checks are `public-tree`, `site-build`, both Ubuntu validation jobs, and the macOS validation job, review threads must be resolved, and the repository owner retains an explicit emergency bypass.

The public default branch now contains `.agents/plugins/marketplace.json`, `plugins/servotab/`, the layered licensing files, and the merged README/website availability copy. Source-checkout clone commands and `blob/HEAD` legal links therefore resolve against current Servotab source. No tag or GitHub Release has been created, and no OpenAI submission or listing has occurred.

## Remaining boundaries

1. Retain the inactive legacy manifests, backups, and transitional helper until the documented recovery/operator dependency is deliberately retired; do not manually clean historical receipts.
2. Keep the current Cloudflare production path on clean manual direct deployments while the historical Git binding remains disconnected and stale. Repairing or replacing that binding, recreating the project, or re-enabling automatic deployments is a separate owner decision, not a hidden follow-up to this deployment.
3. Tag and GitHub Release creation remain unperformed and separate from the merged source candidate.
4. Stop before OpenAI directory submission until the owner explicitly opens that gate.

Update this file by replacing superseded facts, not by appending a development diary.
