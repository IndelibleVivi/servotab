# Servotab release state

Servotab `0.6.3` was published on GitHub, deployed to the production website, and observed on the public OpenAI Plugins Directory on 2026-09-20. Installation, OpenAI directory, GitHub release, and production website observations remain separate states described below. This file records evidence boundaries, not a substitute for GitHub's current branch, checks, tags, Releases API, OpenAI portal, or Cloudflare deployment state.

## 0.6.3 release

The source and latest tagged GitHub release are `0.6.3`, with workspace lifecycle guidance in `worktree`, shared cleanup authority in `finish`, corrected write-surface guidance in `delegate`, and corresponding router/metadata projections. Three new synthetic decision rehearsals bring the Field Lab source pack to twenty cases. The package remains one router, twelve leaves, and 70 manifest-owned files. See [release notes](releases/0.6.3.md).

Fresh local validation passed canonical/generated sync, 13-skill and 70-file package validation, manifest freshness, packaging selftest, all 72 Python regressions (including nine disposable Git tests; the two new parameterized tests each cover assume-unchanged and skip-worktree), public-tree audit, and Python compilation. Standalone Field Lab validate/selftest/list passed all twenty cases with zero target-agent invocations. Main Validate run `35499926427` passed Windows generated sync, public-tree, site build, Ubuntu Python 3.10/3.13, macOS Python 3.13, and exact-source release artifacts for merge commit `6a57dbb`. These checks establish source, package, fixture, and build consistency, not runtime effectiveness. No 0.6.3 live target-model attempt, installed activation, or directory update is established by the GitHub release itself. The production website and public directory have separate receipts below.

The review follow-up adds index-flag inspection and non-mutating content checks (or an unresolved disposition) before accepting cleanup evidence and during each removal recheck. The explicit organization case now requires leaf delivery/read evidence in semantic review instead of a router-only reference assertion. Synthetic traces through the local Field Lab parser and trace verifier confirmed that the valid leaf path fails the old assertion and passes the corrected deterministic checks; this is not a live attempt or a semantic-review outcome.

[PR #34](https://github.com/IndelibleVivi/servotab/pull/34) merged into `main` as `6a57dbb656dc2d1fcd7674d109817e358cfeffdf` after both P2 review findings were fixed and the exact head passed Validate. [Servotab 0.6.3](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.3) is public, Latest, and non-prerelease. The `v0.6.3` tag resolves exactly to the merge commit. Its four custom assets are `servotab-0.6.3-plugin.zip`, `servotab-0.6.3-source.zip`, `release-receipt.json`, and `SHA256SUMS`; a fresh public download passed the complete release-builder check and matched the exact local build. The plugin ZIP SHA-256 is `36c453c64a460998a653d8238a32158f1e4e22f118696689e5dae6d387bb9a1c`. This GitHub publication does not by itself establish installation, website deployment, or an OpenAI directory payload update; those states are recorded separately.

## Source and GitHub

The current release source is merge commit `6a57dbb656dc2d1fcd7674d109817e358cfeffdf`; its tree is `50e1a664212430e9b68e052682470a5d51ad41d9`. Release assets and tag remain bound to that immutable source even when later documentation commits reconcile live state.

PR #32 merged the `0.6.2` release preparation into `main` as `3909242bf142e2b136dde4d96322f4ed649f0164`. That revision includes the Windows text-identity and portable-manifest repair from PR #30 plus the delegation responsibility-contract work from PR #31. Main Validate run `34984233762` completed Windows generated-sync, Ubuntu Python 3.10/3.13, macOS Python 3.13, public-tree, site-build, and exact-source release-artifact preparation successfully.

[Servotab 0.6.2](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.2) was published on 2026-09-15 Singapore time and is now the previous release. The `v0.6.2` tag resolves exactly to `3909242bf142e2b136dde4d96322f4ed649f0164`. Its four custom assets are `servotab-0.6.2-plugin.zip`, `servotab-0.6.2-source.zip`, `release-receipt.json`, and `SHA256SUMS`; a fresh public download passed the release builder's complete `--check` and matched the main CI and local artifacts byte for byte. The plugin ZIP SHA-256 is `45462ce1ac501bca10c07cb76990a12a24febfcca69071f9e981821af7e42966`. The immutable `v0.6.1` release remains available as history.

For current integration and publication state, inspect the [pull requests](https://github.com/IndelibleVivi/servotab/pulls), [Validate runs](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml), and [GitHub Releases](https://github.com/IndelibleVivi/servotab/releases). A version number, successful build, or prepared archive is not a tag or published release. Each release artifact's `release-receipt.json` names its exact source commit and tree; a later merge requires a newly built receipt for that merge.

The tagged 0.6.2 package contains one implicit router, twelve explicit-only leaves, twelve router references, and 70 manifest-owned files. It adds a portable root `plugin.json` beside the synchronized `.codex-plugin/plugin.json` fallback without changing skill topology. It also revises the responsibility-choice contract in `delegate`, `execute`, `debug`, and the implicit router, and adds four delegation behavior canaries. Existing 0.6.1 installations retain the previous delegation wording until updated. One workspace-scoped positive canary has an accepted synthetic attempt and independent review; that evidence supports only the pinned case, not general host effectiveness. Text identity is canonical LF and binary identity remains byte-exact, including compatibility for equivalent CRLF left in an existing Windows worktree. Publisher and maintainer identity is `Yifei Fang`; public creator credit remains `Faye & Cove`. Licensing and the skills-only runtime boundary are retained. There is no new workflow engine, hook payload, or runtime service.

## Evidence carried into the 0.6.2 release

The deterministic gate covers canonical/generated identity; strict metadata and exact package ownership; parsed passive SVGs and decoded PNGs; packaging/migration selftests; package/release regressions; two new fixture baseline/expected-overlay controls; public-tree checks; and nine website motion tests plus the production build. See [Packaging audit](../PACKAGING_AUDIT.md) and [Releasing](releasing.md) for commands and claim limits.

`release-artifacts` runs after the existing source/package/site jobs succeed. It builds and rechecks the four immutable-source artifacts without credentials for publication. Its artifact is preparation evidence only. Tests of fixture repairs and release scripts do not establish natural-language skill activation or better model outcomes.

The published 0.6.1 Field Lab subject pack contained eleven cases: the nine earlier
cases plus existing-normalizer reuse and misleading-green-test controls. The
0.6.2 release contains seventeen cases, adding explicit
tranche-planning, cross-process complete-delivery, and four delegation
responsibility-choice canaries. Its deterministic fixture checks pass. The
positive delegation canary cannot be asserted by a trace ceiling, so it relies on
declared review requirements for real dispatch and integration evidence.

The first explicitly budgeted `delegate-bounded-investigation` attempt ran on
2026-09-15 against source commit `0f747d5`, requesting `gpt-5.6-sol` with `xhigh`
reasoning, one repeat, and network disabled. It produced one subagent event, read
the delegation reference, changed exactly `queue_worker.py` and `LANE_REPORT.md`,
and passed the focused test. A separate read-only agent supported all three
semantic review requirements. The immutable attempt still recorded `fail`
because its Markdown headings did not contain three exact literal label strings;
the Servotab acceptance checker therefore returned `rejected`. No retry occurred
under that invocation budget.

The canary then removed those duplicate literal-label assertions while retaining
report existence, exact changed-file scope, the focused command, trace ceilings,
and the three exact-key semantic review requirements. A separately authorized
second attempt ran against commit `5616b50` with the same requested model, effort,
repeat, and network boundary. Field Lab recorded `pass`: one successful worker
lane, exact two-file scope, required reference reads, a quiescent process, and a
passing focused test. A new independent read-only reviewer supported all three
semantic requirements, and the Servotab checker returned `accepted` for receipt
digest `28fb489ae58ac5a367d18f93f2b990934cf36498b20007038c5b41b5d183d59c`.
The accepted pass also exposed a checker defect: Field Lab stores a normalized
case record, while the checker had compared it directly with raw `case.json`.
The checker now projects only Field Lab's declared loader defaults before exact
comparison; substantive case drift still fails closed, and the synthetic
acceptance suite covers the real record shape. Raw traces and reviews remain
local-only. This is bounded evidence for the pinned case, not exclusive causation,
deployment, general model effectiveness, installed activation, or owner acceptance.

Field Lab feature commit `57eb9ac` is merged into main at `b87b14b`; the main push
validate run `34393492283` completed successfully. That source adds public
`fieldlab review --requirement-outcomes` input with exact-key and bounded-file
validation. Synthetic receipts for the then-current nine human-required cases
produced CLI review records accepted by the Servotab checker with zero target-agent
invocations. The release has one accepted live receipt for
`delegate-bounded-investigation`; the other human-required cases remain
unobserved by this run. The compatible companion source is merged but not released,
installed or activated. Standalone Field Lab validation remains optional. The
named-host installation and discovery receipt below is a separate runtime-identity
observation, not a model-effectiveness claim.

## Host and directory observations

The 2026-08-31 source-install and discovery receipt belongs to `0.4.0-rc1` on macOS with `codex-cli 0.147.0`. A 2026-09-05 maintainer receipt recorded a 69-file `0.6.0` personal installation and fresh-process router discovery. On 2026-09-06, the maintainer checkout was fast-forwarded from the clean, behind-only 0.6 source revision to `863ac30850dc6d7558e824c519b923fd6f8f89e3`; `servotab@personal` then reported installed and enabled at `0.6.1`. The source package and installed cache contained the same 69 regular files with no missing, extra, differing, or symlink entries, and a new `codex debug prompt-input` process discovered `servotab:servotab` from the 0.6.1 cache. This proves the inspected machine's installed identity and fresh-process discovery, not use of a method or improved task outcome.

The previously recorded public OpenAI directory payload was `0.4.0-rc1`, at the [Servotab listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94). PRs #25 and #26 document 0.6 upload-scanner rejections and the resulting dimension fixes. On 2026-09-15, the owner reported that the exact 0.6.2 plugin ZIP was uploaded successfully after confirming the portal's expected portable-manifest normalization notice; no later publication was established for that upload.

On 2026-09-20, the owner reported uploading and publishing 0.6.3. A fresh logged-out readback of the public listing showed `Servotab`, an install entry, developer `Yifei Fang`, version `0.6.3`, and all thirteen public skills: the `Servotab` router plus `Debug`, `Delegate`, `Design`, `Execute`, `Finish`, `Plan`, `Review`, `Review Feedback`, `Spec Chain`, `TDD`, `Verify`, and `Worktree`. This establishes public directory availability and the visible 0.6.3 manifest surface. The listing does not expose an archive digest, so it does not establish byte identity with the GitHub plugin ZIP; it also does not prove installation on another host or live model behavior.

Previous 0.4/0.5 submission archives and the tagged 0.6.1/0.6.2 assets remain historical artifacts. Use only an archive whose receipt, version, source commit, and manifest match the intended operation.

## Website and infrastructure

The current 0.6.3 website was deployed to the existing Cloudflare Pages project from the exact `servotab-site` artifact produced by main Validate run `35502059074` for source `047825179421636cf6414e0430e479ff9195861b`. Cloudflare deployment `5faa2045-390f-4a59-b9a6-2578ecaac268` records environment `Production`, branch `main`, and source `0478251`; the earlier `ce89e9d5` production deployment remains in Pages history. Fresh canonical-host checks returned the 0.6.3 release and directory-publication status from `https://servotab.com/` and its Docs surface. HTTP, `www`, and `servotab.pages.dev` redirect to the canonical HTTPS host; an unknown apex path returns a true 404 with `no-store`; the expected CSP, framing, content-type, referrer, permissions, and cross-origin headers remain present; and page source contains no Cloudflare Insights script or beacon. Real-browser checks at 1280 px and 390 px found no horizontal overflow and zero console errors or warnings on the homepage and Docs. No DNS, telemetry, account topology, redirect configuration, or OpenAI directory state was changed during this website deployment.

Keep private operational identifiers, personal cache paths, account details, and raw host traces outside this public state document. Historical source/install/provenance receipts remain available in [the pre-0.6.1 snapshot](https://github.com/IndelibleVivi/servotab/tree/04552977d5f6262c4f625fe71bd28090c056f1d0); do not repurpose them as current release proof.
