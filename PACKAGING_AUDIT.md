# Packaging and Activation Audit — Servotab 0.5.0

This is a maintainer self-audit of the `0.5.0` source candidate. It is not an independent security, compliance, installed-runtime, Cloudflare, or OpenAI directory-update assurance. The already-live public listing is recorded as a separate observed distribution state.

## Package identity

- Plugin id: `servotab`
- Candidate version: `0.5.0`
- OpenAI package publisher: `Yifei Fang`
- Public creator credit: `Faye & Cove`
- Plugin root: `plugins/servotab/`
- Plugin manifest: `plugins/servotab/.codex-plugin/plugin.json`
- Repo marketplace: `.agents/plugins/marketplace.json`
- Marketplace name: `personal`
- Install selector: `servotab@personal`
- Exact package manifest: `PACK_MANIFEST.json`

The plugin manifest describes Servotab as an independent engineering method layer, uses `Yifei Fang` for both the package `author.name` and install-surface `interface.developerName`, uses the approved `#315EFB` brand color, and points to the current website, support, privacy, terms, and curated package assets. The publisher fields match the owner-selected verified individual identity; they do not replace the `Faye & Cove` creator credit retained in the repository, README editions, and website. Its directory-facing short description stays within 30 characters, and its three starter prompts are distinct, single-line workflow examples within 128 characters. Public documentation links the live listing while keeping directory availability separate from any claim that Servotab is an official OpenAI product.

The standalone package `NOTICE.md` carries the attribution, source, and CC BY 4.0
license link for the five retained Worker Lanes field labels used by `delegate`;
an uploaded ZIP therefore does not depend on the repository-level notice to
explain that packaged provenance boundary.

[`evals/submission-test-cases.md`](evals/submission-test-cases.md) prepares five
positive and three negative reviewer cases from the repository-owned fixtures.
It is preparation material, not evidence that a portal draft was opened or that
the cases were executed by OpenAI review.

### Bounded submission provenance receipt

The pre-identity-patch text-comparison pass fixed the Servotab package at commit
`fe2ec57d84f6b158124c13d4ff79f1c76bc3fd53` and the recorded comparative
source at `obra/superpowers@b36e0829c6d0140e93cfef2ca599b1b07d4a7797`.
It compared all 41 UTF-8 text files in the exact 43-file Servotab payload with
all 194 tracked UTF-8 text files at that upstream ref; the two Servotab PNG
identity assets were outside a text comparison.

The automated pass reported:

- zero normalized contiguous matches of 10 or more words; and
- zero near-exact paragraph candidates after requiring 12–220-word blocks, a
  minimum 0.55 length ratio, at least two shared four-word anchors, a word-level
  sequence ratio of at least 0.72, and trigram Jaccard similarity of at least
  0.30.

An initial run found one common TDD sentence shared with two upstream design
documents. The canonical Servotab wording was independently revised before the
fixed commit, generated projections and `PACK_MANIFEST.json` were refreshed,
and the comparison was rerun to the zero-match result above. Package-local
`NOTICE.md` now names the Superpowers comparative lineage and states the
inclusion boundary directly.

This is a bounded maintainer receipt, not a legal opinion, a whole-history
forensic audit, or a claim that general engineering ideas and terminology do not
overlap. It supports the narrower submission statement that the compared payload
contains no identified Superpowers code, documentation, artwork, or other
licensed payload under the recorded comparison.

The later publisher-identity commit `0e715e7` changed only the two publisher
strings in `.codex-plugin/plugin.json`, the corresponding fail-closed validation
expectations and tamper controls, and the derived manifest digest. The `0.5.0`
candidate adds owner-authored icon files, icon metadata and validation, a
package-rights path clarification, and current publication-state copy; it does
not change any method body or router reference. The fixed-ref text comparison
was not rerun, so its zero-match result remains attached to the `fe2ec57`
textual snapshot rather than being repurposed as provenance or byte-identity
proof for the new ZIP. The new artifact's exact paths and bytes are proven
separately after its immutable source commit exists.

### `0.5.0` update artifact

The designated update artifact is
`servotab-0.5.0-openai-submission-05434fa.zip`, archived from immutable source
`05434fa841cccd8b7f9530791a49741e6cf53063:plugins/servotab`. It contains one
top-level `servotab/` directory and exactly 69 regular files, is 134,331 bytes
(131.2 KiB), and has SHA-256
`08cf42f2561b9705be9d96f3d846fdf41cb16fc885c71c885922e71f79070153`.

The archive passes ZIP integrity, safe-path, duplicate-member, and symlink
checks. Its regular-file path set, sizes, and SHA-256 digests match
`PACK_MANIFEST.json`; an independently extracted source archive from the same
commit is recursively byte-equal; and the owner-facing download and private
continuity copies are byte-identical.

The earlier `servotab-0.4.0-rc1-openai-submission-0e715e7.zip` artifact, SHA-256
`149db94281c7bbc673e10fc2dac9cd7d5cfc8dc680cd73c86f8e5b95cc8afde7`, and
`servotab-0.4.0-rc1-openai-submission-1356c1e.zip`, SHA-256
`cf0d3323b5a06f1a4a099308f75c0084660ae24b81bf2cc80ff8064069efca23`, are
historical publication-era artifacts and must not be used for the `0.5.0`
directory update.

## Activation contract

- `servotab`: `allow_implicit_invocation: true`
- 12 semantic leaf skills: `allow_implicit_invocation: false`
- `PACK_MANIFEST.json` records the same split under `activation`.
- Ordinary-language work may stay direct or route through the implicit router's own references.
- Explicit leaves are stable shortcuts and evaluation controls; the router does not invoke another skill.
- Host-provided subagent tools, concurrency, and model tier are capability inputs, not evidence that Servotab selected `delegate`.
- Repository license selection remains outside router scope.
- Router instructions require quiet activation and prohibit process theatre.

The exact leaf set is:

```text
design
spec-chain
plan
execute
debug
tdd
review
review-feedback
verify
worktree
delegate
finish
```

Retired active identifiers `brainstorm`, `receive-review`, and `parallel` remain only where historical or migration provenance requires them. They are rejected from the current generated package.

## Canonical and derived boundaries

`methods/*.md` is canonical for the 12 method bodies. `scripts/skill_catalog.py` is canonical for plugin skill names, descriptions, prompts, activation metadata, and icon-source routing. Root `assets/servotab-mark-ink*` and `assets/skill-icons/*` are canonical for the router and leaf icon bytes.

`scripts/build_skills.py` generates:

- `plugins/servotab/skills/servotab/SKILL.md`;
- 12 router references under `plugins/servotab/skills/servotab/references/`;
- 12 explicit leaf packages under `plugins/servotab/skills/`;
- each skill's `agents/openai.yaml` and local `assets/icon.svg` / `assets/icon-400.png` pair;
- two curated package assets, `composer-icon.png` and `logo.png`, copied from root `assets/`.

Root `skills/` is retired. `build_skills.py --check` and `validate_sync.py` fail on missing, unexpected, or stale generated files; they also reject a reintroduced root projection.

`PACK_MANIFEST.json` schema 1 records:

- 13 skill directories;
- 12 router references;
- 69 exact payload files: one plugin manifest, two plugin-local rights files, two curated top-level assets, 26 local skill-icon files, and the generated instruction/reference tree;
- file sizes and SHA-256 digests;
- one implicit router and 12 explicit-only leaves.

The digest manifest is used to decide source/package identity. It is not used as a ritual runtime health claim.

## Plugin and marketplace contract

The repo marketplace contains exactly one entry:

```text
personal → servotab → ./plugins/servotab
```

`scripts/runtime_validate.py` checks:

- exact plugin name, version, description, publisher identity, package path, public URLs, brand color, prompts, and asset targets;
- current final-directory constraints for the 30-character short description,
  non-empty long description, 1–3 unique single-line starter prompts of at most
  128 characters, and the absence of app `@mentions`;
- presence and manifest inclusion of plugin-local `LICENSE` and `NOTICE.md`, which preserve the functional-material and identity-asset rights split inside the installable package;
- exact marketplace source, policy, category, and display name;
- exact manifest file set and digests, including all 26 skill icons;
- absence of retired global-installer and method paths.

The source candidate can be discovered with:

```bash
codex plugin marketplace add .
codex plugin add servotab@personal
```

Those commands remain the source-checkout CLI contract. The maintainer environment still carries the earlier `servotab@personal` `0.4.0-rc1` installed/enabled and exact 43-file source/cache receipt; the official curated cache separately exposes the published `0.4.0-rc1` payload. Neither is an installed-runtime receipt for the new 69-file candidate, so host rendering of the new icons remains unverified.

## Legacy ownership boundary

The current repo no longer carries `install.sh`, `uninstall.sh`, `scripts/install.py`, `scripts/uninstall.py`, or an active root `skills/` package.

`scripts/migrate_legacy_install.py` exists only to retire a manifest-owned Softpowers global layer safely:

- default and `--dest` inspection are read-only;
- an active layer returns status `2` and reports its version, manifest, previous layer, skill count, and modified-skill count;
- mutation requires both an exact `--dest` and `--retire`;
- retirement is one LIFO layer at a time;
- same-name backups are restored;
- post-install edits are preserved in a snapshot;
- failure restores prior state;
- a fresh preflight is required before retiring another revealed layer.

The helper is transitional. Its removal condition is: every supported skill root has no active `.softpowers-current-manifest`, and the Servotab plugin migration has been accepted. It is not a new general installer or rollback manager.

## Field Lab v2 subject pack

`fieldlab-pack.json` uses schema version 2 and names `plugins/servotab/skills` as the `servotab-source` subject. It keeps repository-owned canaries and evidence metadata separate from the standalone Field Lab runtime.

The no-spend maintainer commands are:

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

They do not start target-model invocations. A live Field Lab attempt requires its own plan and explicit invocation budget; live model behavior is not inferred from package validation.

The current `0.5.0` no-spend run passed all three commands with one source
subject, nine cases, and zero target-agent invocations.

## Retained verification guarantees

The deterministic gate covers:

- source/generated skill and asset sync;
- exact 13-skill and 12-reference topology;
- real YAML parsing of `SKILL.md` frontmatter and `agents/openai.yaml`;
- router-only implicit activation;
- retired identifier and path exclusion;
- plugin manifest and repo marketplace shape;
- exact 69-file payload identity, 26-icon path/format checks, and asset integrity;
- disposable icon-metadata, missing-icon, icon-digest, missing-skill, wrong-marketplace, and wrong-identity controls;
- fail-closed generation when the retired root `skills/` path reappears, with a disposable sentinel proving that its contents remain untouched;
- read-only legacy ownership detection and explicit one-layer retirement in a disposable fixture;
- Python syntax and visible current-tree public-safety audit;
- all 13 generated skills passing the standalone `skill-validate` entrypoint;
- Field Lab schema validation, fixture selftest, and subject listing with zero
  target-agent invocations;
- desktop/mobile rendered website checks covering the live-listing route, all
  12 method glyphs, responsive sizing, navigation, overflow, console, and
  resource-load state;
- CI matrix on Ubuntu Python 3.10 / 3.13 and macOS Python 3.13.

Maintainer commands:

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
uv run --with PyYAML==6.0.3 python3 scripts/generate_pack_manifest.py --check
uv run --with PyYAML==6.0.3 python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

## Acceptance boundary

As of this source candidate:

- repository package generation and deterministic validation are implemented;
- the local marketplace selector is defined; the retained exact 43-file install receipt belongs to `0.4.0-rc1`, not the new candidate;
- a fresh Codex process exposes only the namespaced implicit router at baseline; a normal newly opened worktree task then exercised an ordinary-language router path and a structured explicit `$review` leaf path without mutating the checkout, while other-machine installation remains a separate runtime check;
- after independent review closed with no actionable P0–P2 findings, all 13 reachable legacy Softpowers layers were retired one at a time with fresh preflight evidence; both supported roots are clear, while inactive historical receipts remain preserved;
- the website deployment and custom-domain state are tracked separately in `docs/current-state.md`; current direct-upload deployment `e58d396f-e1ee-466a-b8db-c0bd2ab9845d` was clean-built from merged source `35c0147` and passed fresh live desktop/mobile checks;
- the GitHub repository has been renamed in place to `IndelibleVivi/servotab`; v0.5 icon PR #20 merged to public `main` as `35c0147`, its post-merge Validate run `33381722536` succeeded, and no tag or GitHub Release is implied;
- the OpenAI directory listing is publicly live at `plugins_6a952d7c729c819196646fda7ec9ad94`; manual upload, submission, review, and publication of the `0.5.0` update remain owner-gated.

A green source gate proves package consistency; the retained maintainer source/cache, fresh-process, and fresh-task receipts prove only the named `0.4.0-rc1` local installation and behavior boundaries. They do not prove `0.5.0` installation, host icon rendering, other-machine behavior, or publication of the directory update. Website deployment and Cloudflare topology remain separate facts tracked in `docs/current-state.md`.
