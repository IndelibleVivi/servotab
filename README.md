# Servotab for Codex

English | [简体中文](README.zh-CN.md)

[![Validate](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml/badge.svg)](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml)
[![License: layered](https://img.shields.io/badge/license-SUL--1.0%20%2B%20CC%20BY--NC--SA%204.0-blue.svg)](LICENSING.md)

Servotab is an independent, community-maintained engineering-method plugin for Codex. Clear changes stay direct. Stronger method appears only when risk, scope, or uncertainty warrants it. Fresh evidence closes the actual outcome.

> Method as exponent, not machinery.

Current source and tagged release: [`0.6.2`](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.2). This release fixes Windows text-identity checks, adopts the portable Agent Plugins manifest, and strengthens delegation responsibility routing with bounded evidence. The [OpenAI Plugins Directory listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94) is a separate distribution surface; a GitHub release does not prove that the directory payload has been updated. See [current state](docs/current-state.md), the [0.6.2 release notes](docs/releases/0.6.2.md), and the historical [0.6.1 release notes](docs/releases/0.6.1.md) for evidence and limits.

## What Servotab changes

Servotab keeps four stable promises:

- Clear changes stay direct.
- Risk brings stronger method.
- Fresh evidence closes the loop.
- The requested outcome stays whole.

Describe ordinary repository work normally. The only implicit-eligible skill is the `servotab` router; twelve method leaves remain explicit-only shortcuts. Servotab does not replace your prompt, `AGENTS.md`, repository rules, permission boundaries, Git decisions, or deployment authority.

A log, screenshot, review, old plan, or generated artifact may be useful evidence. It does not authorize itself or silently become the current specification.

## Install

Open the [official Servotab listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94) in ChatGPT to add the publicly available plugin.

For source inspection or maintainer testing, install the tagged 0.6.2 package from a public checkout:

```bash
git clone --branch v0.6.2 --depth 1 https://github.com/IndelibleVivi/servotab.git
cd servotab
codex plugin marketplace add .
codex plugin add servotab@personal
```

The repository marketplace is named `personal`; it resolves `servotab@personal` to the generated plugin package under `plugins/servotab/`.

Open a fresh Codex task or process after installation so skill discovery is rebuilt. Confirm the installed and enabled package with:

```bash
codex plugin list --marketplace personal
```

For a checkout whose `VERSION` is `0.6.2`, the receipt should contain:

```text
servotab@personal  installed, enabled  0.6.2
```

For a machine-readable discovery check on a system with `jq` and `rg`:

```bash
codex debug prompt-input "Check Servotab discovery." \
  | jq -r '.[].content[]?.text // empty' \
  | rg 'servotab:servotab'
```

The command must return a skill entry named `servotab:servotab` from the installed plugin cache.

### Tested compatibility receipt

On 2026-08-31, the `0.4.0-rc1` source-checkout marketplace route, installed/enabled package receipt, and fresh-process router discovery were verified on macOS with `codex-cli 0.147.0`. On 2026-09-05, the current maintainer machine installed the `0.6.0` source candidate with an exact 69-file source/cache match and observed `servotab:servotab` in fresh-process prompt input. On 2026-09-06, that machine refreshed `servotab@personal` from the clean 0.6.1 release source and verified installed/enabled version 0.6.1, an exact 69-file source/cache match with no symlinks, and fresh-process `servotab:servotab` discovery. These are bounded compatibility and discovery receipts for the named payloads on the inspected machine; they are not a guessed minimum-version guarantee, proof of implicit use or model effectiveness, or a claim about every Codex client.

This source-checkout route is distinct from the officially published directory payload. It replaces the retired root `skills/` installer and the old `install.sh` / `uninstall.sh` flow. If another machine still has a manifest-owned Softpowers `0.3.0-rc5` or earlier global layer, follow the [migration guide](docs/migration-from-softpowers.md). Do not manually delete legacy directories based on the maintainer machine's completed retirement receipt.

## Use

For ordinary work, ask directly:

```text
Fix the mobile message-bubble shift, identify the root cause, implement the repair, and verify the affected behavior.
```

The router may keep a clear, reversible change direct or read one relevant method when the work carries material pressure. It does not manufacture a plan, worktree, test ritual, subagent, or second review merely because those mechanisms exist. Before deep work it also settles responsibility: a bounded, noisy, or otherwise substantial lane can go to one worker, explicit solo requests stay in the main session, and trivial work or frequent cross-owner decisions are not split for coordination benefit. Coupling alone never forces the main session; the coupled parts of one responsibility simply stay together in whichever single lane owns them.

Invoke a method explicitly when you want precise control:

```text
$review inspect the current dirty diff and report only verified, actionable P0-P2 findings.
```

```text
$tdd establish strict red-green evidence for this stale-cursor regression.
```

```text
$spec-chain turn this approved specification into a complete implementation plan; the current tranche must not replace the full scope.
```

## Method set

The plugin contains thirteen skills: one implicit router and twelve explicit leaves.

| Skill | Activation | Purpose |
|---|---|---|
| `servotab` | implicit eligible | Quiet router for ordinary repository work |
| `design` | explicit only | Resolve open feature, interaction, or architecture decisions |
| `spec-chain` | explicit only | Preserve an approved specification across planning and execution |
| `plan` | explicit only | Sequence settled multi-step work |
| `execute` | explicit only | Implement a clear request or plan as a complete outcome |
| `debug` | explicit only | Localize the first violated assumption and repair the root cause |
| `tdd` | explicit only | Apply risk-based test-first work to contracts, state, and regressions |
| `review` | explicit only | Produce one findings-first, evidence-backed implementation review |
| `review-feedback` | explicit only | Verify external feedback before accepting, adjusting, or rejecting it |
| `verify` | explicit only | Match completion claims to fresh, proportionate evidence |
| `worktree` | explicit only | Isolate work only when dirt, risk, duration, or parallel writes justify it |
| `delegate` | explicit only | Choose responsibility before deep work; hand a bounded lane to a worker only when it pays |
| `finish` | explicit only | Inspect the final tree and perform only authorized Git or cleanup actions |

Methods do not create authority. Source-complete, installed, activated, committed, deployed, live, submitted, and published remain separate states.

## Source and package architecture

```text
methods/*.md + scripts/skill_catalog.py        canonical method + metadata source
                    │
                    ▼
          scripts/build_skills.py
                    │
                    ▼
plugins/servotab/
├── plugin.json                               portable Agent Plugins manifest
├── .codex-plugin/plugin.json                 compatibility fallback
├── LICENSE + NOTICE.md                       package-local rights boundary
├── skills/servotab/                          implicit router + 12 references
├── skills/{design,...,finish}/               12 explicit leaves
└── assets/                                   curated package assets

.agents/plugins/marketplace.json              repository marketplace entry
PACK_MANIFEST.json                            exact derived payload identity
```

Root `plugins/servotab/plugin.json` is the portable package entry point. The `.codex-plugin/plugin.json` file remains a synchronized compatibility fallback for older Codex package readers; validation rejects identity or OpenAI-interface drift between them.

The twelve method bodies under `methods/*.md` are canonical. `scripts/skill_catalog.py` owns names, descriptions, prompts, activation metadata, and skill-icon source routing. Root `assets/` owns the router projections and twelve leaf-glyph sources. `plugins/servotab/skills/**` is generated projection—including two icon assets per skill—and must not be edited directly. Paper-backed contrast fallbacks remain canonical source assets but are not shipped in the default runtime payload.

Other surfaces have separate jobs:

- `evals/` and `fieldlab-pack.json`: Servotab-owned behavior cases and optional Field Lab subject pack;
- `site/`: Astro static website source, not plugin runtime authority;
- `docs/current-state.md`: volatile release, install, deployment, and publication facts;
- `docs/migration-from-softpowers.md`: supported migration from manifest-owned legacy layers;
- `AGENTS.md`: stable canonical/generated, verification, documentation, and authorization contract.

## Evidence and claim boundaries

The tagged 0.6.2 release contains exactly 70 manifest-owned package files, adding the portable root manifest while retaining the compatibility fallback; the one-router/twelve-leaf skill topology remains unchanged. It revises the responsibility-choice contract in `delegate`, `execute`, `debug`, and the implicit router. Existing 0.6.1 installations do not contain that newer guidance until they are updated. One workspace-scoped positive canary has an accepted synthetic attempt and independent review, supporting that pinned case without establishing general host effectiveness. Repository checks use canonical LF identity for text and exact bytes for binary assets, so fresh Git for Windows checkouts and equivalent CRLF left in an existing worktree do not create false stale-package reports. They also cover exact skill and icon validation, manifest freshness, packaging and migration self-tests, public-tree safety, Python syntax, decoded PNGs, parsed passive SVGs, package/release regressions, website motion behavior tests, and the website production build.

Those gates prove current source and package consistency under the observed checks. They do not prove behavior on every machine, a website deployment, an OpenAI directory update, or owner acceptance on those separate surfaces. The GitHub Release is public; the existing official directory listing remains a separately observed distribution state.

Maintainers with the standalone `fieldlab` CLI may inspect the source-owned subject pack without invoking a target model:

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

The 0.6.2 release contains seventeen cases. Eleven shipped with the 0.6.1
release; 0.6.2 adds explicit tranche-planning and
cross-process complete-delivery controls, and now four delegation
responsibility-choice canaries. All seventeen have deterministic
baseline/expected-overlay checks, but those checks do not execute a target model
or close declared semantic-review requirements. Positive delegation cannot be
asserted by the trace ceiling (`max_subagent_events`), so its canary pairs a
bounded maximum with review requirements that demand evidence of an actual
dispatch and integration; the trivial, explicit-solo, and
capability-unavailable canaries keep `max_subagent_events: 0`. The inspected
Field Lab 0.2 baseline source at `d9f717a` lacks the required public input; Field
Lab main at `b87b14b` now exposes `fieldlab review --requirement-outcomes`. The
then-current nine human-required cases pass Servotab's synthetic
producer-consumer contract check through that CLI. An initial live attempt for
`delegate-bounded-investigation` supported its three semantic requirements but
failed duplicate literal report-label assertions. After those assertions were
removed in favor of the existing semantic review boundary, a separately budgeted
attempt passed deterministic verification, and a new independent review supported
all three requirements; Servotab acceptance returned `accepted`. This evidence is
limited to that pinned workspace-scoped case. The compatible Servotab source is
released, but the release does not by itself establish installation or activation.
Any further live synthetic attempt
still requires a new plan and explicit invocation budget; Field Lab does not retry
automatically.

## Release artifacts

The published [Servotab 0.6.2 GitHub Release](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.2) provides `servotab-0.6.2-source.zip` for the repository marketplace route and `servotab-0.6.2-plugin.zip` with the 70-file plugin payload for an owner-controlled directory upload. The 0.6.1 assets remain immutable historical artifacts. Neither archive installs dependencies or changes a host automatically.

`release-receipt.json` binds both archives to one source commit/tree and the package manifest. `SHA256SUMS` covers both ZIPs and the receipt. Checksums establish consistency, not publisher authentication. Verify the release source and GitHub provenance as well. Maintainer preparation and draft/publish steps are in [Releasing](docs/releasing.md).

## Feedback, support, and security

- [Behavior feedback](https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml): activation, routing, complete-outcome, review/debug/verification quality, or unnecessary overhead;
- [Plugin package bug](https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml): marketplace discovery, validation, installation, activation, or package assets;
- [Security policy](SECURITY.md): private reporting for vulnerabilities or trust-boundary failures that cannot be disclosed safely in a public issue.

GitHub Issues are public. Remove credentials, tokens, private source, personal data, account details, private paths, local notes, and full private Codex transcripts. Preserve only the smallest public-safe reproduction.

Servotab is skills-only. It adds no Servotab account, backend, database, telemetry service, or network endpoint. Codex and any repositories, terminals, browsers, tools, or external services it uses remain governed by their own permissions and data practices.

## Maintainer checks

Use Python 3.10+ and the pinned `requirements-dev.txt` (PyYAML and Pillow), or the `uv` commands below. These are maintainer dependencies; the skills-only plugin ships neither package.

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with-requirements requirements-dev.txt python3 scripts/validate.py plugins/servotab/skills
uv run --with-requirements requirements-dev.txt python3 scripts/generate_pack_manifest.py --check
uv run --with-requirements requirements-dev.txt python3 scripts/selftest.py
uv run --with-requirements requirements-dev.txt python3 -m unittest discover -s scripts -p 'test_*.py' -q
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

For the website:

```bash
cd site
npm ci
npm test
npm run build
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for canonical edit paths, generated projections, behavior evidence, documentation closure, and contribution terms.

## Lineage, authorship, and licensing

Servotab migrated from the historical Softpowers codebase while preserving its Git history, release records, licensing boundaries, and provenance. The rename does not relabel earlier versions as Servotab releases.

The project is an independent rewrite inspired conceptually by Jesse Vincent / obra's [`superpowers`](https://github.com/obra/superpowers) and by other mechanisms recorded in [third-party notices](THIRD_PARTY_NOTICES.md) and the repository's public pattern-intake documents. Those sources are not bundled dependencies merely because they informed the design.

Created by Faye & Cove. Published and maintained by Yifei Fang ([@IndelibleVivi](https://github.com/IndelibleVivi)), who is the legal licensor only for project-original material she controls. External contributors and third-party rights holders retain their respective rights.

Project-original functional materials and original documentation use layered terms beginning with the `0.3.0-rc1` line. This is source-available / fair-code distribution, not OSI open source. See [LICENSING.md](LICENSING.md), [LICENSE-HISTORY.md](LICENSE-HISTORY.md), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exact path-level terms, the historical MIT boundary, and third-party exceptions.
