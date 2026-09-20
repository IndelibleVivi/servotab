# Synthetic observations

All identifiers below are synthetic, not live paths. The intended integration target is main.

- cache-only: manually managed, inactive linked tree created by this workflow; current tip is an ancestor of current main; no changes/untracked files; only a proven rebuildable build cache is ignored. No deletion authorized.
- local-db: ordinary status clean, branch integrated, but ignored local-state.sqlite contains the only local database; retention unknown.
- detached-lab: clean detached HEAD with unique commits and no named ref preserving its tip.
- hosted: host-managed, active task awaiting PR feedback, no supported host cleanup tool exposed.
- offline: missing registered path, locked with reason external disk temporarily disconnected.
- squash: clean and inactive, same file tree at inspected feature/main revisions, ancestry fails and branch -d would refuse; named branch retained.
- after-merge: PR merged at tip A; the current local branch is tip B with new commits. Current remote state is unavailable.
- dirty: staged edits and untracked notes; no saving or discard authorization.
