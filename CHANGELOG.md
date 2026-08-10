# Changelog

## 0.2.0-rc4 — 2026-08-11

Complete-outcome and Worker Lanes refinement.

- Made the complete requested usable outcome the implementation default; simplicity now constrains mechanism rather than silently reducing product scope to an MVP, scaffold, placeholder, or convenient tranche.
- Required plans to preserve end-to-end coverage and meaningful order, with MVP/prototype scope and material reordering treated as explicit decisions.
- Routed product descriptions, tutorials, screenshots, examples, logs, and reviews by user intent and source authority (`inspiration`, `evidence`, or `normative`) instead of by artifact format.
- Reworked `soft-parallel` around Requester / Coordinator / Task Worker / optional Helper responsibilities, bounded work orders, one-writer ownership, explicit return packets, and coordinator verification.
- Allowed one clean worker lane when context isolation or coordinator attention materially helps, while retaining fewest-lanes, no-duplicate-worker, no-routine-polling, and authorization boundaries.
- Added behavioral probes for anti-MVP regression, reference-led implementation, and a single bounded worker lane.

## 0.2.0-rc3 — 2026-08-10

Specification-to-implementation continuity.

- Added `soft-spec-chain` for major approved specifications that must survive planning and multi-tranche execution without scope loss.
- Required an implementation plan for an approved specification to cover the complete accepted scope; phase and tranche documents are execution views, not substitutes.
- Added compact coverage-ledger, dependency-order, explicit-delta, and tranche-versus-full-completion rules while avoiding specification restatement.
- Hardened generic Plan and Execute so explicit use cannot silently narrow an approved specification.
- Added a behavioral regression fixture for unified 1..N package semantics, migration, UI/import/recovery coverage, and rejection of single-item transitional plans.

## 0.2.0-rc2 — 2026-08-09

Evidence-economy and failure-localization refinement.

- Added a router-level complexity and evidence budget so direct work avoids unsupported abstractions, fallback paths, repeated reads, unused hashes, and duplicate proof.
- Added the same current-job test to explicit `soft-execute` and claim-driven stopping rules to `soft-verify`.
- Consolidated the unique boundary-mapping behavior from the local `trace-complex-failures` experiment into `soft-debug`, including first-violated-assumption localization and a stronger reset after two failed hypotheses.
- Tightened retry and fallback guidance so external failures receive direct diagnostics unless observed evidence and the product contract justify machinery.
- Recast parallel dispatch as a compact Outcome / Scope / Context / Authority / Return contract, preserved permission boundaries, prevented ambiguous duplicate dispatch, and discouraged routine polling.
- Added activation and behavioral pressure cases for cross-boundary bugs, fallback temptation, public security requirements, and stopping after sufficient proof.
- Documented a cleaner pairwise evaluation protocol; no token-savings percentage is claimed without uncontaminated repeated runs.

## 0.2.0-rc1 — 2026-07-28

Activation and progressive-disclosure redesign.

- Made `softpowers` the only implicitly discoverable skill.
- Kept all 11 leaf skills explicit-only as direct shortcuts and eval controls.
- Replaced the old router’s unsupported “load another skill” promise with 11 router-owned `references/*.md` playbooks.
- Reduced the implicit router to roughly 550 words and instructed it to remain silent about activation and internal task labels.
- Added staged reference loading: zero references for clear local work, zero or one primary reference initially, at most one supporting reference before first action, and later reads only on genuine phase changes or new evidence.
- Removed cross-skill invocation language from standalone method bodies so every leaf remains self-contained.
- Added canonical `methods/*.md`, deterministic skill generation, and source/generated sync validation.
- Added activation metadata to `PACK_MANIFEST.json`; the install payload now covers 12 skills and 11 router references.
- Added auto-detection that upgrades an existing v0.1.x `~/.codex/skills` install in place while using `~/.agents/skills` for fresh current-path installs.
- Added positive, contextual, explicit, and negative activation probes.
- Preserved v0.1.2 transaction, rollback, LIFO manifest, edit-snapshot, and standard-library-only installation guarantees.

## 0.1.2 — 2026-07-27

Final packaging hardening after release-candidate review.

- Refused explicit non-LIFO uninstall requests before any filesystem mutation; `--manifest` must match `.softpowers-current-manifest`.
- Added a regression self-test proving rejected non-LIFO uninstalls leave the pointer, manifests, backups, and active skills untouched.
- Removed PyYAML from the user installation and uninstall path.
- Added release-generated `PACK_MANIFEST.json` with the exact 12-skill payload, file sizes, and SHA-256 digests.
- Added standard-library runtime payload validation for source, staging, and installed targets.
- Kept real YAML parsing as a maintainer release gate through `scripts/validate.py` and `scripts/generate_pack_manifest.py`.
- Added a no-site-packages install/uninstall smoke test.

## 0.1.1 — 2026-07-27

Packaging and contract hardening after isolated Codex review.

- Fixed invalid YAML in `soft-finish` frontmatter and switched validation to PyYAML for both frontmatter and `agents/openai.yaml`.
- Changed the default personal skill root to `${CODEX_HOME:-$HOME/.codex}/skills`.
- Made installed-directory validation target only the 12 Softpowers directories, allowing unrelated skills to coexist.
- Replaced the copy loop with staged transactional installation and rollback.
- Added install manifests, content digests, and restoration of replaced same-named skills during uninstall.
- Preserved user-modified installed skills during uninstall instead of silently deleting them.
- Aligned `soft-execute` and Behavioral Probe 1 with applicable user, repository, and global Git instructions.
- Added isolated packaging self-tests for YAML parsing, coexistence, restoration, and rollback.

## 0.1.0 — 2026-07-27

Initial private pack.

- Added explicit risk router with Quick / Deliberate / Deep modes.
- Added 11 focused engineering skills.
- Added risk-based TDD and verification ladders.
- Bounded subagents to independent domains with no nested delegation.
- Combined requirement and quality review into one findings-first pass.
- Made worktree, planning documents, Git integration, and destructive cleanup conditional.
- Added installer, uninstaller, validator, and behavioral probes.
