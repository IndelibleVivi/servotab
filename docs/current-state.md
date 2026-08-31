# Servotab Current State

Last reconciled: `2026-08-31`

This is the volatile status surface. It records what has actually crossed each boundary; it does not replace the durable product contract in `README.md` or the repository contract in `AGENTS.md`.

## At a glance

| Surface | Current state | Evidence boundary |
|---|---|---|
| Product identity | `Servotab` adopted | Current source, manifest, assets, site, and docs use the new identity |
| Source candidate | `0.5.0` integrated on public `main` | Per-skill icon integration and publication-status reconciliation merged through PR #20 as `35c0147`; immutable package source remains `05434fa`, and no Servotab tag or GitHub Release exists |
| Canonical methods and icons | 12 current methods plus 13 skill icon pairs | `methods/*.md`, `scripts/skill_catalog.py`, `assets/servotab-mark-ink*`, and `assets/skill-icons/*`; paper-backed leaf fallbacks remain source-only |
| Plugin package | Generated 69-file candidate | `plugins/servotab/` contains one router, 12 leaves, two local icon assets per skill, two top-level plugin assets, and package-local rights files |
| Deterministic package gate | Green locally and in protected-branch CI on the 69-file `0.5.0` payload | Local generation/sync, exact YAML/topology/icon validation, manifest freshness, expanded packaging/migration selftest, public-tree audit, Python compilation, all 13 standalone `skill-validate` checks, and clean website build passed; PR #20 and post-merge run `33381722536` passed all five required jobs |
| Repo marketplace | Defined | `.agents/plugins/marketplace.json`; selector `servotab@personal` |
| Live Codex install | Published and personal `0.4.0-rc1` payloads remain installed; `0.5.0` not installed | The official `openai-curated-remote/servotab/0.4.0-rc1` cache and the exact 43-file `servotab@personal` receipt remain observable; they do not prove activation or icon rendering for the new 69-file candidate |
| Legacy global layer | Retired; both supported roots clear | Thirteen reachable LIFO layers under `~/.codex/skills` were retired one at a time after independent review; no active pointer or `soft-*` entrypoint remains |
| Field Lab | Schema v2 source subject; no-model checks green | `validate`, `selftest`, and `list` pass against `plugins/servotab/skills` with zero target-agent invocations; live model eval not run |
| Submission materials | `servotab-0.5.0-openai-submission-05434fa.zip` ready for owner-controlled update | Archived from `05434fa:plugins/servotab`; 69 files, 134,331 bytes, SHA-256 `08cf42f2561b9705be9d96f3d846fdf41cb16fc885c71c885922e71f79070153`; both `0.4.0-rc1` archives are historical and forbidden for this update |
| Website source | `0.5.0` listing-status and method-icon update live | Homepage, Docs, Terms, Footer, and Methods catalog link the live listing, separate the newer source candidate, and render the 12 canonical leaf glyphs; fresh desktop/mobile live QA is green |
| Cloudflare Pages | Production site live from exact merged source | Direct-upload deployment `e58d396f-e1ee-466a-b8db-c0bd2ab9845d` was clean-built and uploaded from merge commit `35c0147`; deployment readback reports Production, branch `main`, and source `35c0147`; automatic deployments remain disabled and the historical Git connection remains disconnected |
| `servotab.com` | Active; SSL enabled; RUM injection disabled | Proxied apex DNS, Pages custom-domain status, public HTTPS, strict headers, live interaction and responsive checks, same-origin script/network proof, and true 404 all verified |
| Canonical redirects | Active | `www.servotab.com` and `servotab.pages.dev` return 301 to `https://servotab.com` while preserving path suffix and query string |
| GitHub repository | Renamed to `IndelibleVivi/servotab` | New URL is live, the old `/softpowers` URL returns a 301 redirect, and public `main` now contains the Servotab package and website source |
| GitHub governance | Private reporting and protected `main` active | Private Vulnerability Reporting and merged-branch deletion are enabled; active ruleset `Protect main` requires PRs plus five current CI contexts and retains an explicit owner emergency bypass |
| Git publication | `0.5.0` integrated through PR #20 as `35c0147` | Immutable package source `05434fa` and artifact receipt `8db4e95` are public ancestors; required CI and post-merge run `33381722536` are green; tag and GitHub Release remain separate and unperformed |
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

The designated update artifact is `servotab-0.5.0-openai-submission-05434fa.zip`, generated from `05434fa841cccd8b7f9530791a49741e6cf53063:plugins/servotab`. It contains 69 regular files, is 134,331 bytes (131.2 KiB), and has SHA-256 `08cf42f2561b9705be9d96f3d846fdf41cb16fc885c71c885922e71f79070153`. ZIP integrity; safe paths; duplicate and symlink rejection; manifest path, size, and digest equality; recursive source/archive byte equality; and owner/private-copy byte equality all passed. The earlier `servotab-0.4.0-rc1-openai-submission-0e715e7.zip` (`149db94281c7bbc673e10fc2dac9cd7d5cfc8dc680cd73c86f8e5b95cc8afde7`) and `servotab-0.4.0-rc1-openai-submission-1356c1e.zip` (`cf0d3323b5a06f1a4a099308f75c0084660ae24b81bf2cc80ff8064069efca23`) are retained only as historical publication-era artifacts. Neither may be used for the `0.5.0` update.

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

Production deployment `e58d396f-e1ee-466a-b8db-c0bd2ab9845d` was uploaded with Wrangler 4.127.1 after a clean install and build from an exact `git archive` of merged commit `35c01470e32cb04f6f850d6a62c7a09e7e37c512`, with message `Add per-skill icons for v0.5`. The deployment-list readback records environment `Production`, branch `main`, and source `35c0147`; it is live through `https://servotab.com`.

The apex has a proxied CNAME to `servotab.pages.dev`. Pages reports the custom domain as active with SSL enabled. Fresh post-deployment public requests and rendered checks prove the canonical host, strict headers, exact live-listing CTA, current `0.5.0` source-candidate status, all 12 method glyphs loaded at 32 px desktop and 28 px mobile, 1440-pixel desktop and 390-pixel mobile no-overflow behavior, a 44-pixel mobile-menu target, same-origin resources returning 200, and zero browser console errors or warnings. Earlier accepted checks continue to cover invoke/return interaction, reduced-motion behavior, current Docs and Support routes, the 1200 × 630 social image, and a true 404 with `no-store`.

Cloudflare Configuration Rule `servotab_disable_rum` is active for all incoming requests with action `disable RUM`. A fresh real-browser load exposes only the same-origin `/method-motion.js` script and same-origin page resources, with no Cloudflare Insights script or beacon request and zero console errors or warnings. The edge rule leaves the published `script-src 'self'` CSP, ordinary page caching, and fallback 404 caching contract unchanged.

Cloudflare account configuration now contains the two-entry list `servotab_canonical_hosts` and enabled rule `servotab_canonical_redirects`. A proxied `www` trigger record is present. Fresh edge requests prove both `www.servotab.com` and `servotab.pages.dev` return 301 to the apex while preserving subpaths and query strings; following either redirect reaches a 200 response on `servotab.com`.

The deployed site now links the live OpenAI listing from the hero and footer, keeps the published `0.4.0-rc1` payload separate from the `0.5.0` update candidate, and uses the canonical leaf SVGs as quiet method-key marks. It also points Source and Issues to `IndelibleVivi/servotab`, publishes a source-checkout Quickstart plus the retained `0.4.0-rc1` installed/enabled and observed `codex-cli 0.147.0` receipts, explains the one-router/twelve-explicit-leaf topology and skills-only trust boundary, links the active private security-reporting route, and serves the deterministic wide social preview. The live privacy route explicitly states publisher collection, purpose, recipient, retention, and user controls. The site does not collapse directory availability into OpenAI authorship or publication of the newer update. Domain-level redirects and the RUM opt-out remain Cloudflare account configuration, not `site/public/_redirects` or `site/public/_headers` behavior.

## GitHub and publication

The public repository was renamed in place and now resolves at:

```text
https://github.com/IndelibleVivi/servotab
```

The local `origin` uses `git@github-faye:IndelibleVivi/servotab.git`. GitHub returns a 301 from the old `/softpowers` URL, preserving the historical route. Core migration PR #7 merged as `f110fbcd` with post-merge run `33340000993`; public-availability PR #8 merged as `9e5213d` with run `33340162537`; live-state PR #9 merged as `9085f56` with run `33342268739`; directory-readiness PR #10 merged as `e53dcbc` with run `33344979371`; site-experience PR #11 merged as `c656ad7` with run `33349866213`; public-release-hardening PR #14 merged as `b2bacde` with run `33359648427`; submission-hardening PR #16 merged as `1356c1e` with run `33362683246`; final-publisher-identity PR #18 merged as `21dceba` with run `33368067114`; and v0.5 icon PR #20 merged as `35c0147` with run `33381722536`. All listed runs completed successfully.

Private Vulnerability Reporting is enabled and the repository security policy points to its active advisory route. Merged pull-request branches are deleted automatically. Repository ruleset `Protect main` (`21900625`) is active on the default branch: updates require a pull request, current strict checks are `public-tree`, `site-build`, both Ubuntu validation jobs, and the macOS validation job, review threads must be resolved, and the repository owner retains an explicit emergency bypass.

The public default branch contains the `0.5.0` 69-file package candidate, its canonical/generated icon assets, exact artifact receipt, website source, repository marketplace, final publisher identity, and layered licensing files. Source-checkout clone commands and `blob/HEAD` links now resolve against that integrated source. No tag or GitHub Release has been created. The OpenAI listing is live at the recorded route, while the `0.5.0` update has not been submitted.

## Remaining boundaries

1. Retain the inactive legacy manifests, backups, and transitional helper until the documented recovery/operator dependency is deliberately retired; do not manually clean historical receipts.
2. Keep the current Cloudflare production path on clean manual direct deployments while the historical Git binding remains disconnected and stale. Repairing or replacing that binding, recreating the project, or re-enabling automatic deployments is a separate owner decision, not a hidden follow-up to this deployment.
3. Tag and GitHub Release creation remain unperformed and separate from the merged source candidate.
4. The package publisher identity remains owner-decided as `Yifei Fang`. The first public listing is live; creating an update draft, uploading the new ZIP, policy attestations, submission, review, and publication of `0.5.0` remain Faye-controlled. Preparing the local bundle does not cross any of those later states.

Update this file by replacing superseded facts, not by appending a development diary.
