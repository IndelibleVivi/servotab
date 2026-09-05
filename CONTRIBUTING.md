# Contributing to Servotab

Thank you for bringing evidence back from real work. Servotab `0.5.0` is a plugin-native source candidate. Activation misses, false positives, wrong routing, lost scope, package or icon failures, and unnecessary process are more useful than an abstract request for another workflow.

## Choose the right feedback path

- [Behavior feedback](https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml): routing, activation, complete outcomes, review/debug/verification quality, or unnecessary overhead;
- [Plugin package bug](https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml): marketplace discovery, plugin validation, installation/update, activation, or package assets;
- [Security policy](SECURITY.md): vulnerabilities or trust-boundary failures that require private reporting;
- another concrete proposal may use a normal issue, but explain the real task it improves rather than proposing only a new method name.

## Keep public issues public-safe

Before posting, remove:

- credentials, tokens, cookies, `.env` values, and account details;
- private repository source, client/course/application material, or internal logs;
- private chats, real personal data, and non-public filesystem paths;
- unrelated model output, full Codex transcripts, or long traces.

Preserve the smallest reproduction that still supports the report. Use placeholders or a synthetic fixture when the original evidence cannot be disclosed safely. Do not upload sensitive material to a public issue.

## What a behavior report should contain

When available, include:

1. Servotab version or commit;
2. Codex surface, relevant model, operating system, and repository type;
3. a sanitized original prompt;
4. expected and observed behavior;
5. whether `servotab` activated and which references were visible;
6. whether the complete requested outcome remained intact;
7. any unnecessary plan, reference read, test, hash, tool call, subagent, or repeated verification.

For delegation behavior, distinguish host capability from method selection:

- whether the host/runtime exposed subagent tools;
- whether the router read `delegate.md`;
- whether the task actually contained independent lanes;
- whether the coordinator verified worker output.

A subagent event alone does not prove that Servotab selected the `delegate` method. Token count alone is not a quality verdict; first inspect whether the requested outcome, authority, and necessary boundaries survived.

## Canonical source and generated package

The twelve canonical method bodies live under:

```text
methods/*.md
```

Names, descriptions, default prompts, and activation metadata are canonical in:

```text
scripts/skill_catalog.py
```

`scripts/build_skills.py` generates:

```text
plugins/servotab/skills/servotab/SKILL.md
plugins/servotab/skills/servotab/references/*.md
plugins/servotab/skills/{design,...,finish}/SKILL.md
plugins/servotab/skills/*/agents/openai.yaml
plugins/servotab/skills/*/assets/{icon.svg,icon-400.png}
plugins/servotab/assets/{composer-icon.png,logo.png}
```

Do not edit `plugins/servotab/skills/**` or curated plugin asset copies directly. Change the canonical method, catalog, or root asset—including `assets/skill-icons/*` for leaf glyphs—run the generator, and inspect canonical and generated diffs together.

The retired root `skills/`, `install.sh`, `uninstall.sh`, `scripts/install.py`, and `scripts/uninstall.py` paths must not return as a parallel installation system.

The plugin and marketplace contracts are:

```text
plugins/servotab/.codex-plugin/plugin.json
plugins/servotab/LICENSE
plugins/servotab/NOTICE.md
.agents/plugins/marketplace.json
PACK_MANIFEST.json
```

`PACK_MANIFEST.json` is generated identity for the exact payload. Never hand-edit a path, size, or digest to conceal source/generated drift.

## Method changes

- Make a method serve an observable engineering task rather than method ceremony.
- Preserve the complete requested usable outcome; do not default it to an MVP, scaffold, placeholder, or convenient tranche.
- Classify logs, screenshots, reviews, plans, and generated outputs as instruction, evidence, or inspiration under current intent and authority.
- Add a guard, fallback, hash, or test only for an observed failure, explicit contract, or real boundary.
- Keep the router quiet. Only `servotab` is implicit eligible; the twelve leaves remain explicit-only unless an authorized release proposal changes the topology.
- Keep current semantic IDs such as `design`, `review-feedback`, and `delegate`. Do not restore the retired `brainstorm`, `receive-review`, or `parallel` IDs to current source.

## Field Lab and behavior evidence

Servotab-owned subject material lives under:

```text
fieldlab-pack.json
evals/cases/
evals/candidates/
evals/claims/
evals/receipts/
evals/decisions/
```

The subject pack uses schema v2 and points at `plugins/servotab/skills`. Generic runners, schemas, containment, and quota controls belong to the optional standalone Skill Field Lab companion. Do not copy them into the Servotab plugin or make Servotab own the evaluator runtime.

## Website changes

`site/` is a separate Astro static application. It is not part of the plugin payload and cannot change installation or OpenAI directory status. Its Methods catalog imports the canonical leaf SVGs from root `assets/skill-icons/*`; do not maintain a second website-only glyph set.

Run:

```bash
cd site
npm ci
npm test
npm run build
```

Website copy must distinguish source candidate, installed plugin, Cloudflare deployment, custom-domain activation, the currently published OpenAI listing, a later directory update submission, and publication of that update. Cloudflare account settings and canonical-host redirects remain outside the static source tree.

## Maintainer gate

After changing methods or catalog metadata, regenerate before the final check:

```bash
python3 scripts/build_skills.py
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
python3 scripts/generate_pack_manifest.py
```

Run the fresh deterministic gate before submission:

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
uv run --with PyYAML==6.0.3 python3 scripts/generate_pack_manifest.py --check
uv run --with PyYAML==6.0.3 python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

If the standalone `fieldlab` CLI is installed, maintainers may also run the no-target-model subject checks:

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

Live model evaluation, live plugin installation, Cloudflare deployment, GitHub settings, commit/push/release, and OpenAI directory update submission are separate action surfaces. The deterministic gate does not authorize them.

## Documentation closure

Update the owning surface when package identity, method IDs, canonical/generated boundaries, installation, website behavior, security reporting, or release state changes:

- `README.md` and `README.zh-CN.md`: durable reader-facing product, installation, use, limitations, and support;
- `AGENTS.md`: stable source/generated, verification, documentation, and authorization contract;
- `docs/current-state.md`: volatile install, deployment, domain, repository, and submission facts;
- `docs/migration-from-softpowers.md`: supported legacy-layer migration;
- `CHANGELOG.md`: shipped history and unreleased changes;
- `site/README.md` and site copy: current observable website behavior.

The README editions require factual parity, not sentence-level translation. Reconcile installation, topology, version, availability, security/privacy, licensing, and public claims in both editions.

Do not rewrite historical Softpowers releases as if Servotab existed at the time. Keep private Faye/Cove continuity outside the Git tree.

## Contribution license

By contributing, you represent that you have the right to submit the material and provide it under the license mapped to the target path in [LICENSING.md](LICENSING.md). Repository visibility does not create one uniform license.

If a change spans several licensing surfaces, identify them in the pull request. Rights outside the public licenses, including any commercial permission, can be granted only by the relevant rights holder in a separate written agreement.

Pull requests should name the changed contract, fresh verification, documentation impact, and deliberately deferred work.
