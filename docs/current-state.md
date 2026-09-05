# Servotab Current State

Last reconciled: `2026-09-05`

This is the volatile status surface. It records what has actually crossed each boundary; it does not replace the durable product contract in `README.md` or the repository contract in `AGENTS.md`.

## At a glance

| Surface | Current state | Evidence boundary |
|---|---|---|
| Product identity | `Servotab` adopted | Current source, manifest, assets, site, and docs use the new identity |
| Source candidate | `0.6.0` prepared on local branch `feat/servotab-0.6-astra`; not pushed or integrated into public `main` | The candidate strengthens the router plus `design`, `execute`, and `verify`, retains the 69-file icon-bearing topology, and repairs the homepage motion timer race; no Servotab tag or GitHub Release exists |
| Canonical methods and icons | 12 current methods plus the revised router and 13 skill icon pairs | `methods/*.md`, `scripts/build_skills.py`, `scripts/skill_catalog.py`, `assets/servotab-mark-ink*`, and `assets/skill-icons/*`; paper-backed leaf fallbacks remain source-only |
| Plugin package | Generated 69-file `0.6.0` candidate | `plugins/servotab/` contains one router, 12 leaves, two local icon assets per skill, two top-level plugin assets, and package-local rights files |
| Deterministic package gate | Green locally on the 69-file `0.6.0` branch candidate; protected-branch CI still reflects public `0.5.0` | Fresh generation/sync, exact YAML/topology/icon validation, manifest freshness, packaging/migration selftest, public-tree audit, Python compilation, all 13 standalone `skill-validate` checks, nine website behavior tests, production build, and real-browser motion/responsive QA passed locally; latest public post-merge run remains `33856781309` |
| Repo marketplace | Defined | `.agents/plugins/marketplace.json`; selector `servotab@personal` |
| Live Codex install | `servotab@personal` `0.6.0` installed and enabled; official published cache remains `0.4.0-rc1` | The personal cache is an exact recursive match for the 69-file repo package and fresh-process prompt input discovers `servotab:servotab` at `0.6.0`; this does not prove implicit method use in every task or publication of the update |
| Legacy global layer | Retired; both supported roots clear | Thirteen reachable LIFO layers under `~/.codex/skills` were retired one at a time after independent review; no active pointer or `soft-*` entrypoint remains |
| Field Lab | Schema v2 source subject; no-model checks green | `validate`, `selftest`, and `list` pass against `plugins/servotab/skills` with zero target-agent invocations; live model eval not run |
| Submission materials | No `0.6.0` submission archive prepared | The earlier `servotab-0.5.0-openai-submission-05434fa.zip` remains a verified historical candidate artifact and must not be used for `0.6.0`; upload, attestations, submission, review, and publication remain owner-controlled |
| Website source | `0.6.0` source candidate tested locally; public production remains the merged `0.5.0` site | Source now cancels stale motion timers, settles an in-flight transition when reduced motion becomes active, and runs nine Node behavior tests in CI; fresh 1440px/390px Chromium interaction QA is green, but no Cloudflare deployment was performed |
| Cloudflare Pages | Production site live from exact merged source | Direct-upload deployment `d12a9daf-d994-40d7-b8f2-77bf66a1a731` was clean-built and uploaded from merge commit `4fbe889`; deployment readback reports Production, branch `main`, and source `4fbe889`; automatic deployments remain disabled and the historical Git connection remains disconnected |
| `servotab.com` | Active; SSL enabled; RUM injection disabled | Proxied apex DNS, Pages custom-domain status, public HTTPS, strict headers, live interaction and responsive checks, same-origin script/network proof, and true 404 all verified |
| Canonical redirects | Active | `www.servotab.com` and `servotab.pages.dev` return 301 to `https://servotab.com` while preserving path suffix and query string |
| GitHub repository | Renamed to `IndelibleVivi/servotab` | New URL is live, the old `/softpowers` URL returns a 301 redirect, and public `main` now contains the Servotab package and website source |
| GitHub governance | Private reporting and protected `main` active | Private Vulnerability Reporting and merged-branch deletion are enabled; active ruleset `Protect main` requires PRs plus five current CI contexts and retains an explicit owner emergency bypass |
| Git publication | Public `main` remains the `0.5.0` package/site state; the `0.6.0` branch is local-only | Immutable package source `05434fa` and artifact receipt `8db4e95` remain public ancestors; `0.6.0` has not been pushed, opened as a PR, tagged, or released |
| OpenAI directory | Public listing live at published `0.4.0-rc1`; `0.6.0` not submitted | Owner publication report, listing route `plugins_6a952d7c729c819196646fda7ec9ad94`, and the official local curated cache establish the published state; upload and publication of the current update remain owner-controlled |

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
narrative and creator credit did not change. The local source candidate version is now
`0.6.0`; this is a candidate/update boundary, not a rename or authorship change.

The old root `skills/` projection and transaction installer remain retired. The local marketplace `personal` now exposes `servotab@personal` `0.6.0` as installed and enabled, while the official curated cache separately exposes the published `0.4.0-rc1` package. Both preserve `Yifei Fang` for `author.name` and `interface.developerName`. The personal `0.6.0` cache is a recursive exact match for the 69-file repo package, and fresh-process prompt input discovers its router. This is installation and discovery evidence, not proof that an already-running task reloaded the package, that natural-language activation occurred in every task, or that ChatGPT/OpenAI published the update.

The generated `0.6.0` package contains 69 exact manifest-owned files. The local gate passes source/generated sync, exact 13-skill and 12-reference topology, 26 icon-file and interface-path checks, manifest freshness, expanded packaging/migration selftests including icon metadata/missing-file/digest tamper controls, public-tree audit, Python compilation, all 13 standalone `skill-validate` checks, nine motion-state Node tests, the Astro production build, and real-browser interaction/responsive QA. The new router and the `design`, `execute`, and `verify` methods encode dependency-ordered decisions, reuse research boundaries, behavior-disproving evidence, and explicit review disposition. Field Lab `validate`, `selftest`, and `list` also pass against the `0.6.0` source with zero target-agent invocations; those checks remain separate from natural-language activation evidence. The older fixed-ref text-comparison receipt at package commit `fe2ec57` remains a bounded historical receipt for the then-current 41 text files; it is not relabelled as byte or provenance proof for the new package.

The earlier update artifact `servotab-0.5.0-openai-submission-05434fa.zip`, generated from `05434fa841cccd8b7f9530791a49741e6cf53063:plugins/servotab`, remains a bounded historical receipt: 69 regular files, 134,331 bytes (131.2 KiB), SHA-256 `08cf42f2561b9705be9d96f3d846fdf41cb16fc885c71c885922e71f79070153`, with ZIP, safe-path, duplicate/symlink, manifest, digest, source/archive, and private-copy checks green at the time. It does not contain the `0.6.0` behavior or motion changes and must not be uploaded for this candidate. No `0.6.0` submission archive has been created. The two `0.4.0-rc1` archives likewise remain historical publication-era artifacts.

Independent review closed with no actionable P0–P2 findings in the repaired retirement helper. The verified 13-layer live chain was then retired against the exact root `~/.codex/skills`, one LIFO layer per invocation with a fresh read-only preflight before each layer. Both supported roots now report `CLEAR`; the active pointer and all top-level `softpowers` / `soft-*` entrypoints are absent. Nineteen historical manifest receipts remain with status `uninstalled`, and no modified-skill snapshot was needed.

A fresh-process `codex debug prompt-input` probe includes the implicit router as `servotab:servotab` from the installed `0.6.0` cache and includes no legacy Softpowers skill. It also shows the managed global Servotab anchor followed by the repository `AGENTS.md`, establishing model-visible instruction delivery for a new process without claiming the current task retroactively reloaded it. The 12 leaves remain explicit-only by `agents/openai.yaml` policy and are intentionally omitted from the baseline implicit catalog.

A previous `0.5.0`-era Codex worktree task received an ordinary-language, read-only regression-test question with no named skill invocation. It loaded `servotab:servotab`, kept the task narrow, and routed the evidence question through the debug and TDD references without editing the checkout; a follow-up explicit `$review` invocation entered the review leaf. That historical receipt does not prove `0.6.0` natural-language behavior. No live target-model behavior eval was run for this candidate.

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

Production deployment `d12a9daf-d994-40d7-b8f2-77bf66a1a731` was uploaded with Wrangler 4.129.0 after a clean install and build from an exact `git archive` of merged commit `4fbe889e8541497ebf49d1f6e5e4c736f1be9e86`, with message `Polish site motion cues`. The deployment-list readback records environment `Production`, branch `main`, and source `4fbe889`; it is live through `https://servotab.com`.

The local `0.6.0` website source adds stale-timer cancellation, generation-guarded callbacks, in-flight reduced-motion settlement, and precise Node tests for selectors, button/ARIA state, live-region updates, repeated activation, and independent widgets. A fresh local Astro build and headed Chromium checks at 1440px and 390px passed, including rapid double-click, reduced-motion activation, preference change during a pending transition, zero horizontal overflow, and zero console errors or warnings. This source has not been deployed to Cloudflare, so the production receipt below remains tied to `4fbe889` and the `0.5.0` page state.

The apex has a proxied CNAME to `servotab.pages.dev`. Pages reports the custom domain as active with SSL enabled. Fresh post-deployment public requests and rendered checks prove the canonical host, strict headers, exact live-listing CTA, current `0.5.0` source-candidate status, all 12 method glyphs, the homepage invoke/return status transition, immediate reduced-motion status updates, Methods hover and keyboard-focus cues, 1440-pixel desktop and 390-pixel mobile no-overflow behavior, a 44-pixel mobile-menu target, successful same-origin resources, and zero browser console errors or warnings. Earlier accepted checks continue to cover current Docs and Support routes, the 1200 × 630 social image, and a true 404 with `no-store`.

Cloudflare Configuration Rule `servotab_disable_rum` is active for all incoming requests with action `disable RUM`. A fresh real-browser load exposes only the same-origin `/method-motion.js` script and same-origin page resources, with no Cloudflare Insights script or beacon request and zero console errors or warnings. The edge rule leaves the published `script-src 'self'` CSP, ordinary page caching, and fallback 404 caching contract unchanged.

Cloudflare account configuration now contains the two-entry list `servotab_canonical_hosts` and enabled rule `servotab_canonical_redirects`. A proxied `www` trigger record is present. Fresh edge requests prove both `www.servotab.com` and `servotab.pages.dev` return 301 to the apex while preserving subpaths and query strings; following either redirect reaches a 200 response on `servotab.com`.

The deployed site now links the live OpenAI listing from the hero and footer, keeps the published `0.4.0-rc1` payload separate from the `0.5.0` update candidate, and uses the canonical leaf SVGs as quiet method-key marks. The homepage status copy crossfades with its method state, while Methods rows move their glyph and isolated contract arrow on hover or keyboard focus; the reduced-motion path updates status immediately and collapses CSS transition duration. The site also points Source and Issues to `IndelibleVivi/servotab`, publishes a source-checkout Quickstart plus the retained `0.4.0-rc1` installed/enabled and observed `codex-cli 0.147.0` receipts, explains the one-router/twelve-explicit-leaf topology and skills-only trust boundary, links the active private security-reporting route, and serves the deterministic wide social preview. The live privacy route explicitly states publisher collection, purpose, recipient, retention, and user controls. The site does not collapse directory availability into OpenAI authorship or publication of the newer update. Domain-level redirects and the RUM opt-out remain Cloudflare account configuration, not `site/public/_redirects` or `site/public/_headers` behavior.

## GitHub and publication

The public repository was renamed in place and now resolves at:

```text
https://github.com/IndelibleVivi/servotab
```

The local `origin` uses `git@github-faye:IndelibleVivi/servotab.git`. GitHub returns a 301 from the old `/softpowers` URL, preserving the historical route. Core migration PR #7 merged as `f110fbcd` with post-merge run `33340000993`; public-availability PR #8 merged as `9e5213d` with run `33340162537`; live-state PR #9 merged as `9085f56` with run `33342268739`; directory-readiness PR #10 merged as `e53dcbc` with run `33344979371`; site-experience PR #11 merged as `c656ad7` with run `33349866213`; public-release-hardening PR #14 merged as `b2bacde` with run `33359648427`; submission-hardening PR #16 merged as `1356c1e` with run `33362683246`; final-publisher-identity PR #18 merged as `21dceba` with run `33368067114`; v0.5 icon PR #20 merged as `35c0147` with run `33381722536`; and site-motion polish PR #22 merged as `4fbe889` with run `33856781309`. All listed runs completed successfully.

Private Vulnerability Reporting is enabled and the repository security policy points to its active advisory route. Merged pull-request branches are deleted automatically. Repository ruleset `Protect main` (`21900625`) is active on the default branch: updates require a pull request, current strict checks are `public-tree`, `site-build`, both Ubuntu validation jobs, and the macOS validation job, review threads must be resolved, and the repository owner retains an explicit emergency bypass.

The public default branch contains the `0.5.0` 69-file package candidate, its canonical/generated icon assets, exact artifact receipt, live website motion polish, repository marketplace, final publisher identity, and layered licensing files. The local `feat/servotab-0.6-astra` branch contains the newer candidate but has not been pushed or opened as a PR. No tag or GitHub Release has been created. The OpenAI listing is live at the recorded route, while neither the superseding `0.6.0` candidate nor its absent submission archive has been submitted.

## Remaining boundaries

1. Retain the inactive legacy manifests, backups, and transitional helper until the documented recovery/operator dependency is deliberately retired; do not manually clean historical receipts.
2. Keep the current Cloudflare production path on clean manual direct deployments while the historical Git binding remains disconnected and stale. Repairing or replacing that binding, recreating the project, or re-enabling automatic deployments is a separate owner decision, not a hidden follow-up to this deployment.
3. Push, PR creation, tag, and GitHub Release creation for `0.6.0` remain unperformed and separate from the local source candidate.
4. The package publisher identity remains owner-decided as `Yifei Fang`. The first public listing is live; creating a `0.6.0` archive or update draft, uploading it, policy attestations, submission, review, and publication remain Faye-controlled. Local installation and instruction delivery do not cross any of those later states.

Update this file by replacing superseded facts, not by appending a development diary.
