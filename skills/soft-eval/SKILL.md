---
name: soft-eval
description: "Run reproducible Softpowers behavior evaluations with repository-owned canaries, JSONL traces, deterministic assertions, and evidence-bounded comparisons. Use explicitly for maintainer evals, release evidence, or investigating routing and workflow behavior; do not run model evals as a routine gate for ordinary repository work."
---

# Soft Eval

Evaluate Softpowers behavior with executable evidence. Keep this maintainer capability separate from ordinary repository work: loading the method does not justify spending model quota or turning every change into a benchmark.

## Establish the subject

Name what the run actually exercises before comparing results:

- `current-cli-environment`: whatever skills and configuration the selected Codex CLI currently loads;
- an exact installed manifest or release commit;
- an isolated candidate only when its skill identity is demonstrably unambiguous.

If repo-local and user-level skills share a name, do not claim the run isolated one of them. Codex can expose both. Record the collision or use an environment with one authoritative skill identity.

Keep prompt, fixture, model, reasoning effort, sandbox, permissions, and repeats matched when comparing variants. A cheaper run that skips required outcome or verification does not win.

## Use the bundled runner

Resolve `scripts/run_behavior_evals.py` relative to this skill's `SKILL.md`. In the Softpowers source repository, the canonical entrypoint is `evals/run_behavior_evals.py`.

Start without a model call:

```bash
python3 evals/run_behavior_evals.py list
python3 evals/run_behavior_evals.py selftest
```

Run only the smallest relevant live set:

```bash
python3 evals/run_behavior_evals.py run \
  --case tiny-copy \
  --subject-id current-cli-environment \
  --model <exact-model-id>
```

Use `--repeat` when variance matters. Use `--run-id <id> --resume` to continue an interrupted batch at case boundaries. Do not use a normal user repository as a fixture; the runner creates a disposable Git workspace from repository-owned canary inputs.

## Read the evidence

Each attempt stores a prompt snapshot, case contract, raw JSONL trace, stderr, final message, Git diff, metadata, and deterministic verification. Source runs default to `.softpowers-evals/runs/` in the Softpowers checkout; the installed runner defaults to `${CODEX_HOME:-~/.codex}/softpowers-evals/runs/`. Both are local-only. Use `--output-root` when a different private durable location is required.

Treat the layers separately:

- process completion: Codex exited or timed out;
- deterministic outcome: fixture assertions passed or failed;
- trace observations: commands, plan updates, reference reads, subagent-like events, usage, unknown events, and malformed lines;
- semantic quality: human judgment when the contract cannot be reduced to assertions.

Preserve unknown event types in the raw trace. Do not reinterpret missing telemetry as proof that an action did or did not happen.

## Promote carefully

Use one failed canary to diagnose that case or its contract. Change a shared method only when the failure reflects a real Softpowers gap rather than fixture ambiguity, host configuration, model variance, or an unavailable tool.

After a repair, rerun the affected case and one adjacent control. Claim broader workflow improvement only from later comparable evidence or matched repeated runs.

## Stop

Stop when the requested behavior claim has enough fresh evidence. Do not automatically run every canary, add a grader, create a score, or launch a baseline solely because the eval capability exists.
