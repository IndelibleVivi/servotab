# Packaging and Activation Audit — v0.2.0-rc4

This is a maintainer self-audit, not an independent security or compliance assurance.

This release preserves the v0.1.2 transaction layer and changes the runtime activation topology.

## Activation contract

- `softpowers`: `allow_implicit_invocation: true`
- 12 leaf skills: `allow_implicit_invocation: false`
- Manifest records the same split under `activation`.
- Router description contains both positive repository-work scope and negative controls.
- Router instructions require quiet activation and prohibit process theatre.

## Progressive disclosure

The implicit router owns exactly 12 references.

- Clear local work: 0 references.
- Initial specialist routing: 0–1 primary reference.
- Before first concrete action: at most 1 supporting reference.
- Later reads require a genuine phase change or new evidence.
- No reference may route to another reference.
- No repeated reference reads or lifecycle preloading.

The router body is 629 words, below the 650-word release gate.

## Single source of truth

`methods/*.md` is canonical. `scripts/build_skills.py` generates both:

- `skills/softpowers/references/*.md`
- leaf `skills/soft-*/SKILL.md` bodies

`build_skills.py --check` and `validate_sync.py` fail on drift or unexpected payload files. Leaf method bodies are rejected if they contain `$soft-` cross-skill invocations.

## Install payload

`PACK_MANIFEST.json` schema 2 records:

- 13 skill directories
- 12 router references
- 38 exact payload files
- file sizes and SHA-256 digests
- router-only implicit activation metadata

The user installation path uses only Python standard library.

## Skill-root compatibility

- Explicit `--dest` and environment overrides remain highest priority.
- `CODEX_HOME` remains supported.
- Existing Softpowers in `~/.agents/skills` or `~/.codex/skills` is upgraded in place.
- Fresh installs default to current `~/.agents/skills`.
- Legacy `~/.codex/skills` remains supported.
- Dual active roots are treated as ambiguity and rejected.
- Restoring a v0.1.x layer is supported; removing that restored legacy layer requires the matching legacy uninstaller because the v0.2 uninstaller intentionally rejects a 12-skill manifest.

## Retained transaction guarantees

- Staging before replacement
- Coexistence with unrelated skills
- Same-name backup and restoration
- Complete rollback after injected partial install failure
- LIFO current-schema manifest stack
- Non-LIFO rejection before mutation
- Snapshot preservation of post-install edits
- Install/uninstall under `python -S`

## Release checks

- Deterministic generation and sync check
- Real YAML parsing of all SKILL frontmatter and `openai.yaml`
- Router/leaf invocation-policy validation
- Reference set and no-cross-skill validation
- Manifest freshness and digest validation
- Python compilation and shell syntax
- Default current-root install
- Legacy-root in-place upgrade and restore
- Coexistence, stack, rollback, edit preservation, and no-site-packages tests
- Visible current-tree private-namespace, symlink, local-path, secret-pattern, environment-file, and macOS-junk audit via `scripts/audit_public_tree.py`
- Ubuntu Python 3.10 / 3.13 and macOS Python 3.13 CI matrix
