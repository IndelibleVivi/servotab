# Servotab release state

Source snapshot reconciled on 2026-09-05 for `0.6.1` release preparation. This file records evidence boundaries, not a substitute for GitHub's current branch, checks, tags, or Releases API.

## Source and GitHub

This checkout declares `0.6.1`. The last public baseline independently checked before this patch was `04552977d5f6262c4f625fe71bd28090c056f1d0`: the 0.6 method/motion changes and both SVG scanner repairs were already merged through PRs #24, #25, and #26. Its Validate run `33972052853` completed all five required jobs successfully. The earlier statement that public main remained 0.5 pending integration is superseded.

For this patch's current integration and publication state, inspect the [pull requests](https://github.com/IndelibleVivi/servotab/pulls), [Validate runs](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml), and [GitHub Releases](https://github.com/IndelibleVivi/servotab/releases). A version number, successful build, or prepared archive is not a tag or published release. Each release artifact's `release-receipt.json` names its exact source commit and tree; a later merge requires a newly built receipt for that merge.

The canonical package remains one implicit router, twelve explicit-only leaves, twelve router references, and 69 manifest-owned files. Per-skill icons, publisher identity, public creator credit, licensing, and the skills-only runtime boundary are retained. There is no new workflow engine, hook payload, or runtime service.

## Evidence for 0.6.1

The deterministic gate covers canonical/generated identity; strict metadata and exact package ownership; parsed passive SVGs and decoded PNGs; packaging/migration selftests; package/release regressions; two new fixture baseline/expected-overlay controls; public-tree checks; and nine website motion tests plus the production build. See [Packaging audit](../PACKAGING_AUDIT.md) and [Releasing](releasing.md) for commands and claim limits.

`release-artifacts` runs after the existing source/package/site jobs succeed. It builds and rechecks the four immutable-source artifacts without credentials for publication. Its artifact is preparation evidence only. Tests of fixture repairs and release scripts do not establish natural-language skill activation or better model outcomes.

The Field Lab subject pack contains eleven cases. The nine earlier cases are retained and two cases cover existing-normalizer reuse and a misleading green unit test. Standalone Field Lab validation remains optional. No live target-model evaluation or 0.6.1 named-host installation/activation has been observed in this release-preparation review.

## Historical host and directory observations

The 2026-08-31 source-install and discovery receipt belongs to `0.4.0-rc1` on macOS with `codex-cli 0.147.0`. A 2026-09-05 maintainer receipt recorded a 69-file `0.6.0` personal installation and fresh-process router discovery. Neither observation proves that 0.6.1 is installed, that an existing process reloaded, or that a method was used successfully on a new task.

The previously recorded public OpenAI directory payload was `0.4.0-rc1`, at the [Servotab listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94). PRs #25 and #26 document 0.6 upload-scanner rejections and the resulting dimension fixes. No subsequent directory acceptance is established by this source review. New upload, attestations, submission, review, and publication remain owner-controlled; verify the actual directory state before announcing an update.

Previous 0.4/0.5 submission archives are historical artifacts and must not be used for 0.6.1. Use only an archive whose receipt, version, source commit, and manifest match the intended update.

## Website and infrastructure

The earlier production-site receipt was tied to merged source `4fbe889` on 2026-09-04, including motion/responsive checks. This release changes website source copy and builds it in CI; it does not establish a new Cloudflare deployment or fresh canonical-domain acceptance. Automatic deployment was disabled in the earlier observed configuration. No deployment, DNS, redirect, telemetry, or account configuration was changed by this preparation.

Keep private operational identifiers, personal cache paths, account details, and raw host traces outside this public state document. Historical source/install/provenance receipts remain available in [the pre-0.6.1 snapshot](https://github.com/IndelibleVivi/servotab/tree/04552977d5f6262c4f625fe71bd28090c056f1d0); do not repurpose them as current release proof.
