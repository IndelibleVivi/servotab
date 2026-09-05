# Preparing and publishing a Servotab release

A release is one reviewed source revision plus its validated artifacts. Publishing to GitHub, deploying the website, and updating the OpenAI directory are separate actions with separate authorization.

## Prepare exact artifacts

Use a clean checkout of the intended commit, with the pinned maintainer dependencies installed. Run the full gate in `PACKAGING_AUDIT.md`. The release version must match `VERSION`, plugin metadata, and the generated manifest.

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_release.py --output dist/release
python3 scripts/build_release.py --output dist/release --check
```

The builder refuses a dirty index/worktree, untracked source, unsafe archived files, invalid package content, or an existing output directory. Choose a new output directory for a new build; never overwrite evidence from another revision. Ignored local files are not archived: both ZIPs are produced from Git's exact committed snapshot.

Four outputs are required: `servotab-VERSION-plugin.zip`, `servotab-VERSION-source.zip`, `release-receipt.json`, and `SHA256SUMS`. The plugin ZIP has exactly the manifest-owned payload under `servotab/`; the source ZIP includes the marketplace and maintainer files under a versioned root. ZIP entries have fixed timestamps, sorted paths, normalized tracked executable modes, and no compression-version variability.

CI's `release-artifacts` job runs only after the five existing required validation jobs pass on that push. Download its four-file artifact for the exact intended commit. A PR-head artifact does not become a merge-commit artifact: after merging, obtain the successful main run's artifacts or rebuild at the exact merge commit. The receipt's source SHA must match the release target. Checksums alone do not authenticate the source.

## Create a draft

Before creating any tag or release, verify that the intended commit is reviewed, is on the accepted main history, and has successful required checks. Read existing tags and releases first; stop on a conflicting existing tag. Do not move a published tag or replace an existing release's assets silently.

For 0.6.1, with the artifacts built in `dist/release`, this example deliberately creates a draft at the receipt's exact source SHA:

```bash
set -e
SOURCE_SHA=$(python3 -c 'import json; print(json.load(open("dist/release/release-receipt.json"))["source_commit"])')
test "$(git rev-parse HEAD)" = "$SOURCE_SHA"
git fetch origin main
git merge-base --is-ancestor "$SOURCE_SHA" origin/main
python3 scripts/build_release.py --output dist/release --check
gh release create v0.6.1 \
  dist/release/servotab-0.6.1-plugin.zip \
  dist/release/servotab-0.6.1-source.zip \
  dist/release/release-receipt.json dist/release/SHA256SUMS \
  --repo IndelibleVivi/servotab --target "$SOURCE_SHA" \
  --title 'Servotab 0.6.1' --notes-file docs/releases/0.6.1.md --draft
```

Run these commands with failure-stop behavior (`set -e`) so a failed identity, ancestry, or verification check cannot fall through to release creation. `--target` prevents an absent tag from being silently created at a different default-branch tip. If the tag already exists, independently resolve it to its commit and require an exact receipt match before using the existing tag.

Read back the draft, target/tag, notes, and all four assets. Download the assets into a new directory and compare their bytes against the verified originals; use `build_release.py --output DOWNLOADED_DIRECTORY --check` from the same source checkout. Do not count GitHub's automatic source archives as the custom plugin payload.

## Publish and separate later surfaces

Only after owner-authorized draft inspection should publication occur. An explicit `gh release edit v0.6.1 --draft=false --repo IndelibleVivi/servotab` is a publication action, not part of the builder or normal tests. Verify the public tag/asset readback after publication and update the volatile state record with observed facts.

A GitHub release supplies no evidence that a Codex host installed or activated the new version. An OpenAI directory update uses the plugin ZIP and requires its own upload, declarations, review, and publication. Website deployment uses a separately built source revision and requires canonical-host verification. Never promote source/fixture/CI evidence into these later claims.
