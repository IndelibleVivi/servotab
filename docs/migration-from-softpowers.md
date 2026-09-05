# Migrating from a legacy Softpowers install

This guide moves an active, manifest-owned Softpowers `0.3.0-rc5` or earlier global-skill layer to the current Servotab `0.6.1` plugin package without manually deleting installed skills or rewriting legacy manifests.

> **Maintainer migration receipt — 2026-08-30:** Independent integrated review closed with no actionable P0–P2 findings. `servotab@personal` was freshly reinstalled with an exact 43-file source/cache match, then all 13 reachable manifest-owned layers under `~/.codex/skills` were retired one at a time with a fresh preflight before each invocation. Both supported roots now report `CLEAR`; no modified-skill snapshot was needed. This is a receipt for the inspected maintainer machine, not blanket authority to retire an uninspected root elsewhere.

The migration has three separate boundaries:

```text
validated Servotab source
        → plugin added to Codex
        → exact legacy global layer retired
        → restarted runtime accepted
```

Do not collapse them. A generated plugin package does not prove it is installed, and installing Servotab does not authorize deleting a legacy layer.

## Before you begin

Use a clean or intentionally reviewed Servotab checkout. Confirm the candidate identity before touching live Codex state, and confirm `docs/current-state.md` does not carry an active retirement hold:

```bash
git status --short
cat VERSION
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with-requirements requirements-dev.txt python3 scripts/validate.py plugins/servotab/skills
uv run --with-requirements requirements-dev.txt python3 scripts/generate_pack_manifest.py --check
uv run --with-requirements requirements-dev.txt python3 scripts/selftest.py
uv run --with-requirements requirements-dev.txt python3 -m unittest discover -s scripts -p 'test_*.py' -q
```

Expected candidate version: `0.6.1`. Do not continue from an unknown generated tree or stale manifest.

Close or pause active Codex tasks that could load or write the old skill directories during the cutover. Do not delete plugin caches, skill roots, manifests, backups, or snapshots by hand.

## 1. Inspect legacy ownership — read only

From the Servotab checkout, run:

```bash
python3 scripts/migrate_legacy_install.py
```

Without `--retire`, the helper is read-only. By default it inspects both supported historical roots:

```text
~/.agents/skills
~/.codex/skills
```

Interpret the result:

- `CLEAR ...`: no active `.softpowers-current-manifest` in that root;
- `ACTIVE ...`: one current manifest-owned layer exists;
- exit status `0`: all inspected roots are clear;
- exit status `2`: at least one active legacy layer was found;
- exit status `1`: the helper could not safely validate ownership; stop and inspect the reported error.

For a known custom root, inspect only that exact absolute path:

```bash
python3 scripts/migrate_legacy_install.py --dest /absolute/path/to/skills
```

Record the reported destination, version, manifest, previous layer, and `modified` count. A nonzero modified count is not permission to discard those edits; explicit retirement will preserve modified installed skill content under `.softpowers-retire-snapshots/`.

## 2. Add and inspect the Servotab plugin

Keep the legacy layer in place while establishing that Codex can discover and install the new package. From the Servotab checkout:

```bash
codex plugin marketplace add .
codex plugin list --marketplace personal --available --json
codex plugin add servotab@personal
codex plugin list --json
```

The expected selector is `servotab@personal`, sourced from `./plugins/servotab`.

At this point both the new plugin and the old global layer may be present. Do not use that overlap for ordinary acceptance tasks: two implicit-eligible engineering routers can make activation evidence ambiguous. Confirm package discovery and installed identity, then proceed directly to the deliberate retirement decision.

If plugin installation fails, stop here. The legacy layer has not been changed. Read the full Codex error and fix package discovery or manifest validity before retrying; do not retire the working fallback first.

## 3. Retire one exact legacy layer

This step mutates live installed files. Run it only after the current retirement hold has been removed following helper repair and fresh regression validation. State the exact target and confirm it matches the read-only report before running it.

```bash
python3 scripts/migrate_legacy_install.py \
  --dest /absolute/path/to/skills \
  --retire
```

The helper will:

1. validate the current pointer, manifest, destination, entries, digests, and backups;
2. stage the current manifest-owned targets;
3. restore same-name pre-install backups where recorded;
4. preserve modified installed skills in a timestamped snapshot;
5. mark that one manifest layer `uninstalled`;
6. restore the previous manifest pointer, or remove the pointer when the stack is empty;
7. roll back the operation if an error occurs before commit.

It retires exactly one LIFO layer. If the output says another legacy manifest is now current, run a fresh read-only preflight before deciding whether to retire the next layer:

```bash
python3 scripts/migrate_legacy_install.py --dest /absolute/path/to/skills
```

Repeat only after reviewing the newly exposed version, entries, and modified count. Never skip layers or edit `.softpowers-current-manifest` manually.

When the root is clear, the same read-only command returns status `0` and reports no active legacy manifest.

## 4. Restart and verify runtime identity

Restart the relevant Codex surface so plugin and skill discovery is fresh. Then verify separately:

- `codex plugin list --json` shows `servotab@personal` installed;
- `servotab` is the only current implicit-eligible Servotab router;
- the 12 explicit leaves use the current semantic ids;
- retired `softpowers`, `soft-*`, `brainstorm`, `receive-review`, and `parallel` entries are not active because of the retired layer;
- one ordinary repository task can route quietly through `servotab`;
- representative explicit calls such as `$review` or `$verify` resolve to the plugin package;
- unrelated user skills and standalone companions remain intact.

Run behavior acceptance in a disposable or already-authorized repository. Plugin presence is not enough to claim implicit routing quality.

## Rollback boundary

Before legacy retirement, removing a failed Servotab install is bounded:

```bash
codex plugin remove servotab@personal
```

The old manifest-owned layer remains untouched at that point.

After a legacy layer has been retired, `migrate_legacy_install.py` does not offer automatic reactivation. It preserves the manifest record, restores recorded pre-install backups, and snapshots modified active content, but it deliberately does not invent a forward install from historical bytes. If post-retirement acceptance fails:

1. stop using the ambiguous runtime;
2. keep the retired manifest, restored backups, and snapshots intact;
3. collect the plugin and restart error;
4. decide from a known historical source/ref whether reinstallation is actually required;
5. do not rewrite pointers or copy snapshot directories into active roots by hand.

That recovery decision is separate from the normal one-way migration and should use the exact historical source plus current filesystem evidence.

## What this migration does not change

- It does not install, remove, or update standalone License Boundary or Field Lab.
- It does not rename the GitHub repository or change a Git remote.
- It does not deploy the Servotab website or modify Cloudflare.
- It does not submit or publish a Servotab update in the OpenAI Plugins Directory.
- It does not alter historical Softpowers releases, licenses, manifests, or Git provenance.

## Helper retirement condition

Keep `scripts/migrate_legacy_install.py` only while a supported skill root may still have an active `.softpowers-current-manifest`. Remove it in a later source change after:

1. every supported root is read-only verified clear;
2. Servotab plugin installation and runtime behavior are accepted;
3. no documented recovery or operator path still depends on the helper.

Record that removal as a current architecture change; do not erase the historical migration record.
