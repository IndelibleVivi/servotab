# Workspace dispositions

Inspection only: zero creation, deletion, branch updates, unlocks or pruning.

| Candidate | Disposition | Reason and next step |
| --- | --- | --- |
| cache-only | Remove candidate, awaiting exact authorization | Current-tip integration and rebuildable cache evidence are sufficient for a proposal; refresh state before any approved directory removal; keep branch. |
| local-db | Unresolved / preserve | Clean status hides the unique ignored database; establish retention and an authorized preservation route first. |
| detached-lab | Unresolved / preserve | Commit existence alone is not a durable recovery anchor; obtain authority for a named ref before parking. |
| hosted | Keep | Active host task; respect host lifecycle, no manual fallback removal when host cleanup is unavailable. |
| offline | Keep registration | Disconnected disk and lock explain missing path; no unlock/prune; inspect after storage returns. |
| squash | Park candidate, awaiting authorization | Named branch may preserve work without an integration claim. Equal trees establish current content equality only; failed ancestry neither proves unintegrated content nor authorizes force branch deletion. |
| after-merge | Unresolved | PR at A does not account for current B; inspect B against correct target or establish a preservation route. Unavailable remote state is not an all-clear. |
| dirty | Keep / unresolved | Preserve staged edits and untracked notes; do not auto-commit, stash, archive or discard. |

Age, naming and clean status provide no general disposal rule. These are synthetic judgments, not live operations.
