# Packaging and Activation Audit — Servotab 0.4.0-rc1

This is a maintainer self-audit of the source candidate. It is not an independent security, compliance, installed-runtime, Cloudflare, or OpenAI directory assurance.

## Package identity

- Plugin id: `servotab`
- Candidate version: `0.4.0-rc1`
- Plugin root: `plugins/servotab/`
- Plugin manifest: `plugins/servotab/.codex-plugin/plugin.json`
- Repo marketplace: `.agents/plugins/marketplace.json`
- Marketplace name: `personal`
- Install selector: `servotab@personal`
- Exact package manifest: `PACK_MANIFEST.json`

The plugin manifest describes Servotab as an independent engineering method layer, uses the approved `#315EFB` brand color, and points to the current website, privacy, terms, and curated package assets. It does not claim OpenAI approval or directory availability.

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

`methods/*.md` is canonical for the 12 method bodies. `scripts/skill_catalog.py` is canonical for plugin skill names, descriptions, prompts, and activation metadata.

`scripts/build_skills.py` generates:

- `plugins/servotab/skills/servotab/SKILL.md`;
- 12 router references under `plugins/servotab/skills/servotab/references/`;
- 12 explicit leaf packages under `plugins/servotab/skills/`;
- each skill's `agents/openai.yaml`;
- two curated package assets, `composer-icon.png` and `logo.png`, copied from root `assets/`.

Root `skills/` is retired. `build_skills.py --check` and `validate_sync.py` fail on missing, unexpected, or stale generated files; they also reject a reintroduced root projection.

`PACK_MANIFEST.json` schema 1 records:

- 13 skill directories;
- 12 router references;
- 43 exact payload files: one plugin manifest, two plugin-local rights files, two curated assets, and the generated skill tree;
- file sizes and SHA-256 digests;
- one implicit router and 12 explicit-only leaves.

The digest manifest is used to decide source/package identity. It is not used as a ritual runtime health claim.

## Plugin and marketplace contract

The repo marketplace contains exactly one entry:

```text
personal → servotab → ./plugins/servotab
```

`scripts/runtime_validate.py` checks:

- exact plugin name, version, description, author credit, package path, public URLs, brand color, prompts, and asset targets;
- presence and manifest inclusion of plugin-local `LICENSE` and `NOTICE.md`, which preserve the functional-material and identity-asset rights split inside the installable package;
- exact marketplace source, policy, category, and display name;
- exact manifest file set and digests;
- absence of retired global-installer and method paths.

The source candidate can be discovered with:

```bash
codex plugin marketplace add .
codex plugin add servotab@personal
```

Those commands are the current CLI contract. In the maintainer environment, marketplace `personal` has been added from this checkout and `servotab@personal` `0.4.0-rc1` is installed and enabled. A final remove/add refresh produced an exact recursive match between the 43-file source package and the installed cache. A fresh-process prompt-input probe exposes the implicit router as `servotab:servotab` and exposes no legacy Softpowers skill. Those local receipts do not generalize to other machines or prove representative natural-language routing and structured explicit-leaf behavior.

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

## Retained verification guarantees

The deterministic gate covers:

- source/generated skill and asset sync;
- exact 13-skill and 12-reference topology;
- real YAML parsing of `SKILL.md` frontmatter and `agents/openai.yaml`;
- router-only implicit activation;
- retired identifier and path exclusion;
- plugin manifest and repo marketplace shape;
- exact payload identity and asset integrity;
- disposable tamper, missing-skill, wrong-marketplace, and wrong-identity controls;
- fail-closed generation when the retired root `skills/` path reappears, with a disposable sentinel proving that its contents remain untouched;
- read-only legacy ownership detection and explicit one-layer retirement in a disposable fixture;
- Python syntax and visible current-tree public-safety audit;
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
- the local marketplace selector is defined, and the maintainer installation is enabled with an exact 43-file source/cache equality receipt;
- a fresh Codex process exposes only the namespaced implicit router at baseline; a normal newly opened worktree task then exercised an ordinary-language router path and a structured explicit `$review` leaf path without mutating the checkout, while other-machine installation remains a separate runtime check;
- after independent review closed with no actionable P0–P2 findings, all 13 reachable legacy Softpowers layers were retired one at a time with fresh preflight evidence; both supported roots are clear, while inactive historical receipts remain preserved;
- the website deployment and custom-domain state are tracked separately in `docs/current-state.md`;
- the GitHub repository has been renamed in place to `IndelibleVivi/servotab`; core migration PR #7 merged to public `main` as `f110fbcd`, public-availability PR #8 merged as `9e5213d`, and both post-merge Validate runs succeeded; no tag or GitHub Release is implied;
- OpenAI directory submission has not been made and remains owner-gated.

A green source gate proves package consistency; the separate maintainer source/cache, fresh-process, and fresh-task receipts prove only the named local installation and behavior boundaries. They do not prove other-machine installation, general behavior quality, or OpenAI review. Website deployment and Cloudflare topology remain separate facts tracked in `docs/current-state.md`.
