# Packaging and Activation Audit — v0.3.0-rc4

This is a maintainer self-audit, not an independent security or compliance assurance.

This release preserves the transaction layer while returning the install
payload to one engineering router plus its explicit method leaves.

## Activation contract

- `softpowers`: `allow_implicit_invocation: true`
- 13 `soft-*` leaf skills: `allow_implicit_invocation: false`
- Manifest records the same split under `activation`.
- Router description contains both positive repository-work scope and negative controls.
- Repository license selection is explicitly outside router scope and retained
  as a negative-routing seed.
- Router instructions require quiet activation and prohibit process theatre.

## Progressive disclosure

The implicit router owns exactly 13 references.

- Clear local work: 0 references.
- Initial specialist routing: 0–1 primary reference.
- Before first concrete action: at most 1 supporting reference.
- Later reads require a genuine phase change or new evidence.
- No reference may route to another reference.
- No repeated reference reads or lifecycle preloading.

The router body is 645 words, below the 650-word release gate.

## Single source of truth

`methods/*.md` is canonical for the 13 `soft-*` engineering leaves.
`scripts/build_skills.py` generates both:

- `skills/softpowers/references/*.md`
- leaf `skills/soft-*/SKILL.md` bodies

`evals/run_behavior_evals.py`, `evals/schemas/`, and `evals/cases/` are the
canonical behavior-eval sources. The same generator projects them into the
installed `soft-eval` skill's `scripts/` and `assets/` directories.

`build_skills.py --check` and `validate_sync.py` fail on drift or unexpected payload files. Leaf method bodies are rejected if they contain `$soft-` cross-skill invocations.

## Recommended companion

[`IndelibleVivi/license-boundary`](https://github.com/IndelibleVivi/license-boundary)
`v0.1.0-rc3` is the tested licensing companion. Its standalone repository is
both authoring and distribution authority. Softpowers carries no same-named
directory, source projection, manifest entry, backup ownership, or updater.

## Install payload

`PACK_MANIFEST.json` schema 2 records:

- 14 skill directories
- 13 router references
- 60 exact payload files
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
- Historical manifests are validated from their own entries, so current code can
  safely restore old 12/13/14/15-skill layers.
- Install stops before staging when the active historical layer still manages a
  skill retired from the current pack; the user must uninstall that layer first.

## Retained transaction guarantees

- Staging before replacement
- Coexistence with unrelated skills
- Same-name backup and restoration
- Complete rollback after injected partial install failure
- LIFO manifest stack across historical skill sets
- Non-LIFO rejection before mutation
- Snapshot preservation of post-install edits
- Install/uninstall under `python -S`

## Release checks

- Deterministic generation and sync check
- Real YAML parsing of all SKILL frontmatter and `openai.yaml`
- Router/leaf invocation-policy validation
- Reference set and no-cross-skill validation
- Manifest freshness and digest validation
- Historical retired-skill migration and independent-ownership validation
- Three repository-owned eval canaries with known-fail/known-pass assertions
- Installed-layout eval runner discovery and JSONL trace-parser self-test
- Python compilation and shell syntax
- Default current-root install
- Legacy-root in-place upgrade and restore
- Coexistence, stack, rollback, edit preservation, and no-site-packages tests
- Visible current-tree private-namespace, symlink, local-path, secret-pattern, environment-file, and macOS-junk audit via `scripts/audit_public_tree.py`
- Ubuntu Python 3.10 / 3.13 and macOS Python 3.13 CI matrix
