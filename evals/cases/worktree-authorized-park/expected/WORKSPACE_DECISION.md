# Authorized batch rehearsal

From the main checkout, announce that directory removal releases the paused experiment while keeping branch experiment at E, and retires the integrated checkout while keeping feature/done at D. Existing authorization covers these exact two unchanged items; no repeated approval and no merge of experiment are needed.

Refresh each item's tip, full local/ignored state, locks and active ownership immediately before its command. If unchanged, execute ordinary `git worktree remove ../experiment` and `git worktree remove ../integrated`. If either refuses, investigate without force. Leave ../changed pending because new notes invalidate its old disposition; do not stash, commit or discard the notes. This does not stop the two independent unchanged items.

Verify the two registrations/directories are gone and `git rev-parse refs/heads/experiment` still equals E and `git rev-parse refs/heads/feature/done` still equals D. Retain ../changed and all branches. Check the experiment restoration route: when needed, `git worktree add ../experiment experiment`, then restore dependencies from the committed lockfile. The local branch is not an off-device backup. No branch -d/-D, remote deletion, prune, unlock or force is included.

This file is a rehearsal plan over synthetic observations. No checkout was removed and no runtime restoration was verified here.
