# Servotab Repository Contract

This file is the stable project-specific contract for agents working in this repository. Read it before editing canonical methods, generated plugin files, package metadata, behavior evidence, the website, or release surfaces.

## Product identity

- Product and plugin id: `servotab`
- Canonical domain: `https://servotab.com`
- Product form: a quiet, risk-scaled Codex engineering method layer
- Core thesis: “Method as exponent, not machinery.”
- Stable promise: keep clear changes direct, add stronger method only when risk or uncertainty requires it, close claims with fresh evidence, and preserve the complete requested outcome.

Servotab is independent and community-maintained. Do not claim it is an official OpenAI product, approved by OpenAI, submitted to the plugin directory, or available there unless current owner-authorized evidence proves that exact state.

## Truth ownership

| Surface | Authority |
|---|---|
| `methods/*.md` | Canonical bodies for the 12 engineering methods |
| `scripts/skill_catalog.py` | Canonical skill ids, descriptions, prompts, and activation metadata |
| `scripts/build_skills.py` | Canonical generation rules for plugin skills and curated package assets |
| `plugins/servotab/skills/**` | Generated projection; never edit directly |
| `assets/` | Canonical repository asset files and usage notes |
| `plugins/servotab/assets/` | Generated curated package copies, not a second asset authority |
| `plugins/servotab/.codex-plugin/plugin.json` | Plugin package metadata and public interface contract |
| `plugins/servotab/LICENSE` and `NOTICE.md` | Package-local functional-material and identity-asset rights boundary |
| `.agents/plugins/marketplace.json` | Repository marketplace route |
| `PACK_MANIFEST.json` | Exact generated package identity; regenerate, do not hand-edit |
| `fieldlab-pack.json` and `evals/` | Servotab-owned behavior subject and evidence surfaces |
| `site/` | Static public website source; not plugin runtime authority |
| `README.md` | Durable user-facing identity, installation, use, and limitations |
| `docs/current-state.md` | Volatile candidate, install, GitHub, deployment, domain, and submission state |
| `docs/migration-from-softpowers.md` | Supported transition from manifest-owned legacy global layers |

Logs, screenshots, design boards, reviews, external repositories, generated files, deployments, and previous plans are evidence or projections unless the current task explicitly gives them authority. They do not silently override current user intent, accepted specifications, or canonical source.

## Current package topology

The package contains exactly one implicit-eligible router, `servotab`, and 12 explicit-only leaves:

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

Retired current IDs are `brainstorm`, `receive-review`, and `parallel`. Preserve them only in historical release records, provenance, and migration explanation. Do not restore them as active methods, skills, references, invocation examples, issue fields, or package paths.

Root `skills/`, `install.sh`, `uninstall.sh`, `scripts/install.py`, and `scripts/uninstall.py` are retired. Do not add a parallel global-skill installer around the plugin package.

`scripts/build_skills.py` fails closed if the retired root `skills/` path exists. The generator must never recursively delete that path: remove known tracked legacy projection files through the reviewed migration diff, and preserve any unknown or untracked content for explicit disposition.

## Editing workflow

For a method or metadata change:

1. Edit `methods/*.md` and/or `scripts/skill_catalog.py`.
2. Run `python3 scripts/build_skills.py`.
3. Inspect canonical and generated diffs together.
4. Run the package validation gate.
5. Update documentation whose current contract changed.

For a canonical package asset change:

1. Edit or replace only the intended file under `assets/` with rights and provenance understood.
2. Run `python3 scripts/build_skills.py` to update curated plugin copies.
3. Regenerate `PACK_MANIFEST.json` only after plugin validation passes.
4. Inspect visual output and the exact package diff.

Do not infer a public license for an asset from its presence in the repository. Existing license texts, the path map, third-party terms, and actual rights evidence control what may be distributed.

## Verification

The complete deterministic source/package gate is:

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
uv run --with PyYAML==6.0.3 python3 scripts/generate_pack_manifest.py --check
uv run --with PyYAML==6.0.3 python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

When the website changes, also run from `site/`:

```bash
npm ci
npm run build
```

Use rendered desktop/mobile and relevant interaction checks for visual or behavior changes. Build output alone does not prove the public domain, redirects, headers, reduced-motion behavior, or owner acceptance.

When standalone Field Lab is available, the no-target-model subject checks are:

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

Do not run a live Field Lab attempt without an explicit plan and invocation budget.

## Legacy migration

`scripts/migrate_legacy_install.py` is a narrow transitional helper, not a general installer.

- Its default inspection is read-only.
- `--dest` identifies one exact skill root.
- Mutation requires `--retire` and an explicit `--dest`.
- Never run retirement while `docs/current-state.md` records a migration hold; close helper safety findings and rerun the regression gate first.
- Retirement is one manifest-owned LIFO layer at a time.
- Run a fresh read-only preflight before every retirement.
- Do not manually delete legacy directories, pointers, manifests, backups, or snapshots.
- Remove the helper only after supported roots have no active `.softpowers-current-manifest` and plugin migration has been accepted.

Because retirement changes live installed files, state the exact target and why the action is needed before running it.

## Release and external-action boundaries

Keep these states separate:

```text
source-complete
validated candidate
installed in local Codex
activated after restart
committed
pushed
GitHub repository renamed
Cloudflare candidate deployed
custom domain active
redirects active
OpenAI directory submitted
OpenAI directory published
owner accepted
```

One state never proves the next.

- GitHub rename, remote URL changes, commit, push, tag, release, deployment, DNS, redirect, and account mutations need authority for that exact surface.
- Website and Cloudflare work do not authorize an OpenAI submission.
- OpenAI submission and publication remain explicit owner gates even if package and website checks are green.
- A deployment URL does not prove the canonical domain or redirects.
- Domain-level redirects belong to Cloudflare account configuration, not `site/public/_redirects`.
- A Git-connected Pages project and a direct-upload project are different topologies; do not recreate or switch the project without current evidence and authority.

Record volatile outcomes in `docs/current-state.md` only after observing them. Do not put account ids, tokens, personal paths, local cache data, or private deployment traces in the public repository.

## Documentation closure

Update current-facing docs whenever method ids, plugin routes, install commands, supported surfaces, domain behavior, privacy boundaries, or status claims change. Preserve historical changelog and provenance wording; add a transition entry instead of rewriting old Softpowers releases as Servotab releases.

Before stage, commit, or push:

- inspect `git status --short` and the intended diff;
- stage explicit public paths;
- run the relevant fresh verification;
- run `git diff --cached --check` when a staged diff exists;
- ensure private continuity, raw exports, secrets, local caches, build output, and unrelated changes are absent;
- confirm docs do not claim a later release or deployment state than the evidence.

Private Faye/Cove continuity belongs outside the Git worktree. Public documentation may describe product architecture and verified state, but must not include private reasoning, personal filesystem paths, account details, or internal transcripts.
