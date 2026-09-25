# Packaging audit — Servotab 0.6.4 release candidate

Maintainer release-preparation audit. This defines checked source/package properties and their limits; it is not an independent security certification, directory approval, deployment receipt, or target-model effectiveness result. Exact CI and release identities are recorded by their run and `release-receipt.json`, not inferred from this filename.

## Identity and ownership

Product/plugin `servotab`; source version `0.6.4`; publisher and maintainer `Yifei Fang`; public creator credit `Faye & Cove`. The repository marketplace is `personal`, selecting `servotab@personal` from `plugins/servotab`. The current source candidate contains 70 manifest-owned files: one portable root manifest, one synchronized compatibility manifest, two rights files, two curated assets, 13 skill bodies, 13 metadata files, 26 skill icons, and 12 router references. The published 0.6.3 release remains the immutable 70-file artifact recorded by its receipt until a separately verified 0.6.4 publication replaces it as Latest.

`methods/*.md` owns method bodies, `skill_catalog.py` owns metadata/icon routing, `build_skills.py` owns the router and generation rules, and root `assets/` owns icon bytes. Generated files and `PACK_MANIFEST.json` are projections. The sole implicit-eligible skill is `servotab`; all twelve method leaves remain explicit-only. No hook, MCP server, hidden runtime, global instruction file, telemetry, or account is added to the package.

## Deterministic checks

The current gate verifies canonical LF source/generated text, exact binary bytes, required paths and metadata, duplicate-key rejection, finite SVG dimensions, and canonical manifest sizes/digests. A repository `.gitattributes` policy keeps fresh Windows checkouts on LF; the checks also recognize CRLF left in an existing worktree as the same text identity. Release snapshots still come from immutable Git blobs and retain byte-exact artifact verification. The gate rejects unowned package files/directories and symlinks and unowned generated content before generator mutation. JSON and YAML are parsed with duplicate-key rejection rather than last-key-wins behavior.

SVGs are parsed as XML with a real SVG namespace root and a narrow passive-geometry/paint allowlist. The observed upload scanner requires a viewBox of at least 48 × 48 even when explicit dimensions are larger. Non-finite dimensions, malformed XML, event attributes, external resources, and declarations are rejected. This does not claim to validate every aspect of SVG rendering.

Pillow verifies PNG structure and decodes image pixels. Exact dimensions, source 8-bit RGBA, one frame, bounded size, and complete termination are required. Skill icons are 400 × 400; the release builder also checks the 512 × 512 composer and 1024 × 1024 logo. Pillow and PyYAML are pinned maintainer-only dependencies, absent from the skill payload. No icon geometry or raster image changes are part of the 0.6.4 candidate.

Regressions cover the previously accepted malformed SVG/PNG inputs, metadata ambiguity, package expansion, generator writes through symlinks, archive reproducibility, dirty/staged/untracked source, output tampering, and exact payload membership. Public behavior fixtures retain the existing-normalizer and false-green publication controls, add discussion-intake coverage, and exercise cross-boundary diagnosis, missing native-host conditions, and information-bearing diagnostic progress. Their baselines and expected repairs are checked independently where executable; these are fixture controls, not model runs.

The 0.6.4 source pack contains twenty-four behavior cases. Twenty declare non-empty human-review requirements, and twelve adversarial controls are retained. The four cases added since 0.6.3 cover discussion intake plus three evidence-scoped diagnostic decisions. Disposable Git regressions establish removal/recovery mechanisms separately. Rehearsal file assertions, fixture controls, and Git tests do not establish target-agent behavior or general method effectiveness.

## Run the gate

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
python3 scripts/validate.py plugins/servotab/skills
python3 scripts/generate_pack_manifest.py --check
python3 scripts/selftest.py
python3 -m unittest discover -s scripts -p 'test_*.py' -q
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
(cd site && npm ci && npm test && npm run build)
```

CI retains Ubuntu Python 3.10/3.13 and macOS Python 3.13 validation, adds a Git-for-Windows-default checkout proof for generated payload identity, and keeps the public-tree and site-build jobs. The gated release-artifacts job creates both ZIPs, the receipt, and checksums. Failure in any prerequisite prevents that job from preparing artifacts. A green result is scoped to the exact revision and commands run.

## Distribution and verification limits

The plugin ZIP contains only `servotab/` and the exact manifest payload; the source ZIP contains the complete archived source and repository marketplace. Sorted paths, fixed timestamps/modes and stored ZIP entries make the outputs reproducible without dependence on compression-library versions. The receipt binds source commit/tree and manifest identity to both archives. Checksums detect inconsistency but do not authenticate the publisher by themselves.

The builder reads a clean Git commit, refuses unsafe/nonregular archived members and refuses output overwrites. It does not create a tag, GitHub release, directory submission, installation, or deployment. Final release and host acceptance follow [Releasing](docs/releasing.md) and [current state](docs/current-state.md). Standalone Field Lab and real target-model outcomes remain separate observations; unrun checks must not be described as passed.

## Retained history and rights

The [0.5 audit at its historical snapshot](https://github.com/IndelibleVivi/servotab/blob/04552977d5f6262c4f625fe71bd28090c056f1d0/PACKAGING_AUDIT.md) retains earlier archive, migration, and provenance observations. The fixed-ref Superpowers text comparison at `fe2ec57` was not rerun for 0.6.3 and is not a provenance certificate for this candidate. Original code/documentation licenses, package-local notices, third-party attribution, and the separate identity-asset boundary are unchanged. See [Licensing](LICENSING.md) and [Third-party notices](THIRD_PARTY_NOTICES.md).
