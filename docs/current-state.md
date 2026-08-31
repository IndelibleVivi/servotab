# Servotab Current State

Last reconciled: `2026-08-31`

This is the volatile status surface. It records what has actually crossed each boundary; it does not replace the durable product contract in `README.md` or the repository contract in `AGENTS.md`.

## At a glance

| Surface | Current state | Evidence boundary |
|---|---|---|
| Product identity | `Servotab` adopted | Current source, manifest, assets, site, and docs use the new identity |
| Source candidate | `0.5.0` on local branch `feat/v0.5-skill-icons` | Per-skill icon integration and publication-status reconciliation are source-complete locally; no Servotab tag or GitHub Release exists, and Git/CI integration remains pending |
| Canonical methods and icons | 12 current methods plus 13 skill icon pairs | `methods/*.md`, `scripts/skill_catalog.py`, `assets/servotab-mark-ink*`, and `assets/skill-icons/*`; paper-backed leaf fallbacks remain source-only |
| Plugin package | Generated 69-file candidate | `plugins/servotab/` contains one router, 12 leaves, two local icon assets per skill, two top-level plugin assets, and package-local rights files |
| Deterministic package gate | Green locally on the 69-file `0.5.0` payload | Generation/sync, exact YAML/topology/icon validation, manifest freshness, expanded packaging/migration selftest, public-tree audit, Python compilation, all 13 standalone `skill-validate` checks, and a clean website production build have passed locally; CI remains to be refreshed after Git integration |
| Repo marketplace | Defined | `.agents/plugins/marketplace.json`; selector `servotab@personal` |
| Live Codex install | Published and personal `0.4.0-rc1` payloads remain installed; `0.5.0` not installed | The official `openai-curated-remote/servotab/0.4.0-rc1` cache and the exact 43-file `servotab@personal` receipt remain observable; they do not prove activation or icon rendering for the new 69-file candidate |
| Legacy global layer | Retired; both supported roots clear | Thirteen reachable LIFO layers under `~/.codex/skills` were retired one at a time after independent review; no active pointer or `soft-*` entrypoint remains |
| Field Lab | Schema v2 source subject; no-model checks green | `validate`, `selftest`, and `list` pass against `plugins/servotab/skills` with zero target-agent invocations; live model eval not run |
| Submission materials | New `0.5.0` update ZIP pending an immutable package-source commit | The new archive will be generated only from committed `plugins/servotab/` bytes and checked against the 69-file manifest; both `0.4.0-rc1` archives are historical and forbidden for the `0.5.0` update |
| Website source | `0.5.0` publication-status and method-icon update source-complete and browser-checked locally | Homepage, Docs, Terms, Footer, and Methods catalog now link the live listing, separate the newer source candidate, and render the 12 canonical leaf glyphs; desktop/mobile browser QA is green, while Git integration and deployment remain pending |
| Cloudflare Pages | Production site live from exact merged source | Direct-upload deployment `f262501e-cd23-4f19-b779-3e42cb0703d6` was built and uploaded from merge commit `1356c1e`; deployment readback reports Production, branch `main`, and source `1356c1e`; automatic deployments remain disabled and the historical Git connection remains disconnected |
| `servotab.com` | Active; SSL enabled; RUM injection disabled | Proxied apex DNS, Pages custom-domain status, public HTTPS, strict headers, live interaction and responsive checks, same-origin script/network proof, and true 404 all verified |
| Canonical redirects | Active | `www.servotab.com` and `servotab.pages.dev` return 301 to `https://servotab.com` while preserving path suffix and query string |
| GitHub repository | Renamed to `IndelibleVivi/servotab` | New URL is live, the old `/softpowers` URL returns a 301 redirect, and public `main` now contains the Servotab package and website source |
| GitHub governance | Private reporting and protected `main` active | Private Vulnerability Reporting and merged-branch deletion are enabled; active ruleset `Protect main` requires PRs plus five current CI contexts and retains an explicit owner emergency bypass |
| Git publication | Last integrated `main` remains `82be13e`; `0.5.0` branch is local | The new changes have not yet been committed, pushed, reviewed by required CI, or merged; tag and GitHub Release remain separate and unperformed |
| OpenAI directory | Public listing live | Owner publication report, listing route `plugins_6a952d7c729c819196646fda7ec9ad94`, and the official local curated cache establish the published `0.4.0-rc1` state; upload and publication of the `0.5.0` update remain owner-controlled |

## Source and package

The current architecture is plugin-native:

```text
methods/*.md + scripts/skill_catalog.py + assets/{servotab-mark-ink*,skill-icons/*}
        → scripts/build_skills.py
        → plugins/servotab/skills/**
        → PACK_MANIFEST.json

.agents/plugins/marketplace.json
        → servotab@personal
        → plugins/servotab
```

Current method ids are `design`, `spec-chain`, `plan`, `execute`, `debug`, `tdd`, `review`, `review-feedback`, `verify`, `worktree`, `delegate`, and `finish`. The only implicit-eligible skill is `servotab`.

The OpenAI package publisher fields remain deliberately separate from public
creator credit: `.codex-plugin/plugin.json` uses `Yifei Fang` for both
`author.name` and `interface.developerName`, while the repository, README
editions, and website continue to credit `Faye & Cove`. The brand, product
narrative and creator credit did not change. The source candidate version is now
`0.5.0`; this is a candidate/update boundary, not a rename or authorship change.

The old root `skills/` projection and transaction installer remain retired. The local marketplace `personal` still exposes the earlier `0.4.0-rc1` installed/enabled receipt, and the official curated cache separately exposes the published `0.4.0-rc1` package. Both preserve `Yifei Fang` for `author.name` and `interface.developerName`. The new `0.5.0` candidate has not replaced either installed payload, so current icon rendering in ChatGPT/Codex remains unverified until Faye submits the update and a refreshed host surface is available.

The generated `0.5.0` package contains 69 exact manifest-owned files. The local gate currently passes source/generated sync, exact 13-skill and 12-reference topology, 26 icon-file and interface-path checks, manifest freshness, expanded packaging/migration selftests including icon metadata/missing-file/digest tamper controls, public-tree audit, Python compilation, all 13 standalone `skill-validate` checks, and the Astro production build. Field Lab `validate`, `selftest`, and `list` also pass with zero target-agent invocations. The v0.5 change does not alter method bodies. The older fixed-ref text-comparison receipt at package commit `fe2ec57` remains a bounded historical receipt for the then-current 41 text files; it is not relabelled as byte or provenance proof for the new package.

The new `0.5.0` update artifact is intentionally not named yet: it will be generated from an immutable package-source commit after the full source gate passes. The earlier `servotab-0.4.0-rc1-openai-submission-0e715e7.zip` (`149db94281c7bbc673e10fc2dac9cd7d5cfc8dc680cd73c86f8e5b95cc8afde7`) and `servotab-0.4.0-rc1-openai-submission-1356c1e.zip` (`cf0d3323b5a06f1a4a099308f75c0084660ae24b81bf2cc80ff8064069efca23`) are retained only as historical publication-era artifacts. Neither may be used for the `0.5.0` update.

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

Production deployment `f262501e-cd23-4f19-b779-3e42cb0703d6` was uploaded with Wrangler 4.127.1 from an exact `git archive` of merged commit `1356c1e109425345119b6838025edca2b00408e9`, with message `Harden submission provenance and privacy`. The deployment-list readback records environment `Production`, branch `main`, and source `1356c1e`; it is live through `https://servotab.com`.

The apex has a proxied CNAME to `servotab.pages.dev`. Pages reports the custom domain as active with SSL enabled. Fresh post-deployment public requests and rendered checks prove the canonical host, strict headers, current visitor-journey copy, 1440-pixel desktop and 390-pixel mobile no-overflow behavior, a 44-pixel mobile-menu target with working navigation, current Docs and Support routes, the 1200 × 630 social image, and zero browser console errors or warnings. Earlier accepted checks continue to cover invoke/return interaction, reduced-motion behavior, and a true 404 with `no-store`.

Cloudflare Configuration Rule `servotab_disable_rum` is active for all incoming requests with action `disable RUM`. A fresh real-browser load exposes only the same-origin `/method-motion.js` script and same-origin page resources, with no Cloudflare Insights script or beacon request and zero console errors or warnings. The edge rule leaves the published `script-src 'self'` CSP, ordinary page caching, and fallback 404 caching contract unchanged.

Cloudflare account configuration now contains the two-entry list `servotab_canonical_hosts` and enabled rule `servotab_canonical_redirects`. A proxied `www` trigger record is present. Fresh edge requests prove both `www.servotab.com` and `servotab.pages.dev` return 301 to the apex while preserving subpaths and query strings; following either redirect reaches a 200 response on `servotab.com`.

The deployed site now points Source and Issues to `IndelibleVivi/servotab`, publishes a first-use source-checkout Quickstart plus installed/enabled and observed `codex-cli 0.147.0` receipts, explains the one-router/twelve-explicit-leaf topology and skills-only trust boundary, links the active private security-reporting route, and serves the deterministic wide social preview. The live privacy route explicitly states publisher collection, purpose, recipient, retention, and user controls; a fresh request followed the canonical slash redirect to a 200 response containing each disclosure. The site keeps tag, GitHub Release, OpenAI listing, and OpenAI approval claims explicitly separate. Domain-level redirects and the RUM opt-out remain Cloudflare account configuration, not `site/public/_redirects` or `site/public/_headers` behavior.

## GitHub and publication

The public repository was renamed in place and now resolves at:

```text
https://github.com/IndelibleVivi/servotab
```

The local `origin` uses `git@github-faye:IndelibleVivi/servotab.git`. GitHub returns a 301 from the old `/softpowers` URL, preserving the historical route. Core migration PR #7 merged as `f110fbcd` with post-merge run `33340000993`; public-availability PR #8 merged as `9e5213d` with run `33340162537`; live-state PR #9 merged as `9085f56` with run `33342268739`; directory-readiness PR #10 merged as `e53dcbc` with run `33344979371`; site-experience PR #11 merged as `c656ad7` with run `33349866213`; public-release-hardening PR #14 merged as `b2bacde` with run `33359648427`; submission-hardening PR #16 merged as `1356c1e` with run `33362683246`; and final-publisher-identity PR #18 merged as `21dceba` with run `33368067114`. All listed runs completed successfully.

Private Vulnerability Reporting is enabled and the repository security policy points to its active advisory route. Merged pull-request branches are deleted automatically. Repository ruleset `Protect main` (`21900625`) is active on the default branch: updates require a pull request, current strict checks are `public-tree`, `site-build`, both Ubuntu validation jobs, and the macOS validation job, review threads must be resolved, and the repository owner retains an explicit emergency bypass.

The public default branch contains `.agents/plugins/marketplace.json`, the final publisher identity under `plugins/servotab/`, and the layered licensing files. Source-checkout clone commands and `blob/HEAD` legal links currently resolve against the published `0.4.0-rc1` source line; the local `0.5.0` icon and availability update is not public until its protected-branch integration completes. No tag or GitHub Release has been created. The OpenAI listing is live at the recorded route, while the `0.5.0` update has not been submitted.

## Remaining boundaries

1. Retain the inactive legacy manifests, backups, and transitional helper until the documented recovery/operator dependency is deliberately retired; do not manually clean historical receipts.
2. Keep the current Cloudflare production path on clean manual direct deployments while the historical Git binding remains disconnected and stale. Repairing or replacing that binding, recreating the project, or re-enabling automatic deployments is a separate owner decision, not a hidden follow-up to this deployment.
3. Tag and GitHub Release creation remain unperformed and separate from the merged source candidate.
4. The package publisher identity remains owner-decided as `Yifei Fang`. The first public listing is live; creating an update draft, uploading the new ZIP, policy attestations, submission, review, and publication of `0.5.0` remain Faye-controlled. Preparing the local bundle does not cross any of those later states.

Update this file by replacing superseded facts, not by appending a development diary.
