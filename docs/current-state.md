# Servotab release state

Source and release state reconciled through 2026-09-15 for `0.6.1`. This file records evidence boundaries, not a substitute for GitHub's current branch, checks, tags, or Releases API.

## Source and GitHub

This checkout declares `0.6.1`. The last public baseline independently checked before this patch was `04552977d5f6262c4f625fe71bd28090c056f1d0`: the 0.6 method/motion changes and both SVG scanner repairs were already merged through PRs #24, #25, and #26. Its Validate run `33972052853` completed all five required jobs successfully. The earlier statement that public main remained 0.5 pending integration is superseded.

PR #27 merged the release-preparation revision as `863ac30850dc6d7558e824c519b923fd6f8f89e3`; main Validate run `33977223008` completed its five source/package/site jobs and the dependent `release-artifacts` job successfully. [Servotab 0.6.1](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.1) was published as the latest, non-prerelease GitHub Release on 2026-09-06 Singapore time. The `v0.6.1` tag resolves exactly to that merge commit. Its four custom assets are `servotab-0.6.1-plugin.zip`, `servotab-0.6.1-source.zip`, `release-receipt.json`, and `SHA256SUMS`; a fresh public download passed the release builder's complete `--check` and matched the reviewed CI artifacts byte for byte.

For this patch's current integration and publication state, inspect the [pull requests](https://github.com/IndelibleVivi/servotab/pulls), [Validate runs](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml), and [GitHub Releases](https://github.com/IndelibleVivi/servotab/releases). A version number, successful build, or prepared archive is not a tag or published release. Each release artifact's `release-receipt.json` names its exact source commit and tree; a later merge requires a newly built receipt for that merge.

The tagged 0.6.1 package remains one implicit router, twelve explicit-only leaves, twelve router references, and 69 manifest-owned files. The current unreleased source candidate adds a portable root `plugin.json` beside the synchronized `.codex-plugin/plugin.json` fallback, bringing its package identity to 70 files without changing skill topology. It also revises the responsibility-choice contract in `delegate`, `execute`, `debug`, and the implicit router, and adds four delegation behavior canaries. That guidance exists only in this source candidate: the installed and activated 0.6.1 package still carries the previous delegation wording. One workspace-scoped synthetic host attempt has exercised the candidate, but its immutable receipt was rejected and does not establish accepted host behavior. Text identity is canonical LF and binary identity remains byte-exact, including compatibility for equivalent CRLF left in an existing Windows worktree. Per-skill icons, publisher identity, public creator credit, licensing, and the skills-only runtime boundary are retained. There is no new workflow engine, hook payload, or runtime service.

## Evidence for 0.6.1

The deterministic gate covers canonical/generated identity; strict metadata and exact package ownership; parsed passive SVGs and decoded PNGs; packaging/migration selftests; package/release regressions; two new fixture baseline/expected-overlay controls; public-tree checks; and nine website motion tests plus the production build. See [Packaging audit](../PACKAGING_AUDIT.md) and [Releasing](releasing.md) for commands and claim limits.

`release-artifacts` runs after the existing source/package/site jobs succeed. It builds and rechecks the four immutable-source artifacts without credentials for publication. Its artifact is preparation evidence only. Tests of fixture repairs and release scripts do not establish natural-language skill activation or better model outcomes.

The published 0.6.1 Field Lab subject pack contains eleven cases: the nine earlier
cases plus existing-normalizer reuse and misleading-green-test controls. The
current unreleased source candidate contains seventeen cases, adding explicit
tranche-planning, cross-process complete-delivery, and four delegation
responsibility-choice canaries. Its deterministic fixture checks pass. The
positive delegation canary cannot be asserted by a trace ceiling, so it relies on
declared review requirements for real dispatch and integration evidence.

One explicitly budgeted `delegate-bounded-investigation` attempt ran on
2026-09-15 against source commit `0f747d5`, requesting `gpt-5.6-sol` with `xhigh`
reasoning, one repeat, and network disabled. It produced one subagent event, read
the delegation reference, changed exactly `queue_worker.py` and `LANE_REPORT.md`,
and passed the focused test. A separate read-only agent supported all three
semantic review requirements. The immutable attempt still recorded `fail`
because its Markdown headings did not contain the three exact literal strings
required by the workspace assertions; the Servotab acceptance checker therefore
returned `rejected`. No retry or second target invocation was run. Raw trace and
review records remain local-only. This is a bounded host observation, not accepted
behavior evidence, exclusive causation, deployment, or owner acceptance.

Field Lab feature commit `57eb9ac` is merged into main at `b87b14b`; the main push
validate run `34393492283` completed successfully. That source adds public
`fieldlab review --requirement-outcomes` input with exact-key and bounded-file
validation. Synthetic receipts for the then-current nine human-required cases
produced CLI review records accepted by the Servotab checker with zero target-agent
invocations. The candidate's thirteen human-required cases still have no accepted
live receipt. The compatible companion source is merged but not released,
installed or activated. Standalone Field Lab validation remains optional. The
named-host installation and discovery receipt below is a separate runtime-identity
observation, not a model-effectiveness claim.

## Historical host and directory observations

The 2026-08-31 source-install and discovery receipt belongs to `0.4.0-rc1` on macOS with `codex-cli 0.147.0`. A 2026-09-05 maintainer receipt recorded a 69-file `0.6.0` personal installation and fresh-process router discovery. On 2026-09-06, the maintainer checkout was fast-forwarded from the clean, behind-only 0.6 source revision to `863ac30850dc6d7558e824c519b923fd6f8f89e3`; `servotab@personal` then reported installed and enabled at `0.6.1`. The source package and installed cache contained the same 69 regular files with no missing, extra, differing, or symlink entries, and a new `codex debug prompt-input` process discovered `servotab:servotab` from the 0.6.1 cache. This proves the inspected machine's installed identity and fresh-process discovery, not use of a method or improved task outcome.

The previously recorded public OpenAI directory payload was `0.4.0-rc1`, at the [Servotab listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94). PRs #25 and #26 document 0.6 upload-scanner rejections and the resulting dimension fixes. No subsequent directory acceptance is established by this source review. New upload, attestations, submission, review, and publication remain owner-controlled; verify the actual directory state before announcing an update.

Previous 0.4/0.5 submission archives are historical artifacts and must not be used for 0.6.1. Use only an archive whose receipt, version, source commit, and manifest match the intended update.

## Website and infrastructure

The earlier production-site receipt was tied to merged source `4fbe889` on 2026-09-04, including motion/responsive checks. This release changes website source copy and builds it in CI; it does not establish a new Cloudflare deployment or fresh canonical-domain acceptance. Automatic deployment was disabled in the earlier observed configuration. No deployment, DNS, redirect, telemetry, or account configuration was changed by this preparation.

Keep private operational identifiers, personal cache paths, account details, and raw host traces outside this public state document. Historical source/install/provenance receipts remain available in [the pre-0.6.1 snapshot](https://github.com/IndelibleVivi/servotab/tree/04552977d5f6262c4f625fe71bd28090c056f1d0); do not repurpose them as current release proof.
