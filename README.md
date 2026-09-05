# Servotab for Codex

English | [简体中文](README.zh-CN.md)

[![Validate](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml/badge.svg)](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml)
[![License: layered](https://img.shields.io/badge/license-SUL--1.0%20%2B%20CC%20BY--NC--SA%204.0-blue.svg)](LICENSING.md)

Servotab is an independent, community-maintained engineering-method plugin for Codex. Clear changes stay direct. Stronger method appears only when risk, scope, or uncertainty warrants it. Fresh evidence closes the actual outcome.

> Method as exponent, not machinery.

Source version in this checkout: `0.6.1`. This patch hardens asset and package validation, clarifies evidence checks, and adds reproducible release archives. The [GitHub Releases page](https://github.com/IndelibleVivi/servotab/releases) records tagged distribution; the [OpenAI Plugins Directory listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94) is a separate distribution surface. A source version or GitHub release does not prove that the directory payload has been updated. Servotab remains independent and community-maintained. See [current state](docs/current-state.md) and the [0.6.1 notes](docs/releases/0.6.1.md) for evidence and limits.

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

For source inspection or maintainer testing, install the separate current repository candidate from a public checkout:

```bash
git clone https://github.com/IndelibleVivi/servotab.git
cd servotab
codex plugin marketplace add .
codex plugin add servotab@personal
```

The repository marketplace is named `personal`; it resolves `servotab@personal` to the generated plugin package under `plugins/servotab/`.

Open a fresh Codex task or process after installation so skill discovery is rebuilt. Confirm the installed and enabled package with:

```bash
codex plugin list --marketplace personal
```

For a checkout whose `VERSION` is `0.6.1`, the receipt should contain:

```text
servotab@personal  installed, enabled  0.6.1
```

For a machine-readable discovery check on a system with `jq` and `rg`:

```bash
codex debug prompt-input "Check Servotab discovery." \
  | jq -r '.[].content[]?.text // empty' \
  | rg 'servotab:servotab'
```

The command must return a skill entry named `servotab:servotab` from the installed plugin cache.

### Tested compatibility receipt

On 2026-08-31, the `0.4.0-rc1` source-checkout marketplace route, installed/enabled package receipt, and fresh-process router discovery were verified on macOS with `codex-cli 0.147.0`. On 2026-09-05, the current maintainer machine installed the `0.6.0` source candidate with an exact 69-file source/cache match and observed `servotab:servotab` in fresh-process prompt input. Neither historical receipt verifies installation or model behavior for `0.6.1`. These are bounded compatibility and discovery receipts for the named payloads; they are not a guessed minimum-version guarantee, proof of implicit use in every task, or a claim about every Codex client.

This source-checkout route is distinct from the officially published directory payload. It replaces the retired root `skills/` installer and the old `install.sh` / `uninstall.sh` flow. If another machine still has a manifest-owned Softpowers `0.3.0-rc5` or earlier global layer, follow the [migration guide](docs/migration-from-softpowers.md). Do not manually delete legacy directories based on the maintainer machine's completed retirement receipt.

## Use

For ordinary work, ask directly:

```text
Fix the mobile message-bubble shift, identify the root cause, implement the repair, and verify the affected behavior.
```

The router may keep a clear, reversible change direct or read one relevant method when the work carries material pressure. It does not manufacture a plan, worktree, test ritual, subagent, or second review merely because those mechanisms exist.

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
| `delegate` | explicit only | Give a small number of independent lanes explicit ownership and return contracts |
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
├── .codex-plugin/plugin.json                 plugin manifest
├── LICENSE + NOTICE.md                       package-local rights boundary
├── skills/servotab/                          implicit router + 12 references
├── skills/{design,...,finish}/               12 explicit leaves
└── assets/                                   curated package assets

.agents/plugins/marketplace.json              repository marketplace entry
PACK_MANIFEST.json                            exact derived payload identity
```

The twelve method bodies under `methods/*.md` are canonical. `scripts/skill_catalog.py` owns names, descriptions, prompts, activation metadata, and skill-icon source routing. Root `assets/` owns the router projections and twelve leaf-glyph sources. `plugins/servotab/skills/**` is generated projection—including two icon assets per skill—and must not be edited directly. Paper-backed contrast fallbacks remain canonical source assets but are not shipped in the default runtime payload.

Other surfaces have separate jobs:

- `evals/` and `fieldlab-pack.json`: Servotab-owned behavior cases and optional Field Lab subject pack;
- `site/`: Astro static website source, not plugin runtime authority;
- `docs/current-state.md`: volatile candidate, install, deployment, and publication facts;
- `docs/migration-from-softpowers.md`: supported migration from manifest-owned legacy layers;
- `AGENTS.md`: stable canonical/generated, verification, documentation, and authorization contract.

## Evidence and claim boundaries

The integrated candidate contains exactly 69 manifest-owned package files, including two generated icon assets for each of its thirteen skills. Repository checks cover canonical/generated sync, exact skill and icon validation, manifest freshness, packaging and migration self-tests, public-tree safety, Python syntax, decoded PNGs, parsed passive SVGs, package/release regressions, website motion behavior tests, and the website production build.

Those gates prove current source and package consistency under the observed checks. They do not prove behavior on every machine, publication of this newer candidate, a deployment, or owner acceptance. The existing official listing is a separately observed public-distribution state.

Maintainers with the standalone `fieldlab` CLI may inspect the source-owned subject pack without invoking a target model:

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

The source pack now contains eleven cases. The two new reuse and false-green fixtures have deterministic baseline/expected-overlay checks; those checks do not execute a target model. Any live synthetic attempt requires its own plan and explicit invocation budget.

## Release artifacts

Use the source checkout or the `servotab-0.6.1-source.zip` asset for the repository marketplace route. `servotab-0.6.1-plugin.zip` contains only the 69-file plugin payload for an owner-controlled directory upload; it has no repository marketplace. Neither archive installs dependencies or changes a host automatically.

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

Created by Faye & Cove. Faye ([@IndelibleVivi](https://github.com/IndelibleVivi)) maintains the project and is the legal licensor only for project-original material she controls. External contributors and third-party rights holders retain their respective rights.

Project-original functional materials and original documentation use layered terms beginning with the `0.3.0-rc1` line. This is source-available / fair-code distribution, not OSI open source. See [LICENSING.md](LICENSING.md), [LICENSE-HISTORY.md](LICENSE-HISTORY.md), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exact path-level terms, the historical MIT boundary, and third-party exceptions.
