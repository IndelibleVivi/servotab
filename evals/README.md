# Softpowers behavior evals

`evals/` 现在同时保存 behavior-eval source of truth 与较宽的 activation seed set：

- `run_behavior_evals.py`：standard-library runner；
- `cases/`：repository-owned disposable Git fixtures 与 assertions；
- `schemas/`：case/result JSON contracts；
- `activation-prompts.csv`：尚未全部自动化的 routing seed set；
- `candidates/`：外部 pattern intake decisions，不是 runtime authority。

`scripts/build_skills.py` 会把 runner、cases 与 schemas 投影进 generated `skills/soft-eval/`。Source 与 installed payload 不能各自演化。

## Deterministic gate

这些命令不调用 model：

```bash
python3 -S evals/run_behavior_evals.py list
python3 -S evals/run_behavior_evals.py selftest
```

Self-test 对每个 case 执行 known-fail fixture 与 known-pass expected overlay，并覆盖 schema contract、Git fixture、rename status parsing、GPG-signing isolation、relative Codex executable resolution、strict resume identity 和 synthetic Codex JSONL parser。它是普通 pack self-test 的一部分。

## Live run

Live eval 必须显式选择 `--case` 或 `--all`；runner 不会因存在而自动花 model quota：

```bash
python3 -S evals/run_behavior_evals.py run \
  --case stale-cursor \
  --subject-id current-cli-environment \
  --model <exact-model-id>
```

Runner 在 disposable Git workspace 中调用 `codex exec --json --ephemeral`。Source run 默认把 prompt、case contract、raw JSONL、stderr、final message、Git diff、metadata 与 verification 写到 `.softpowers-evals/runs/<run-id>/`；installed runner 默认写到 `${CODEX_HOME:-~/.codex}/softpowers-evals/runs/<run-id>/`。也可以显式传 `--output-root`。同一个 `--run-id` 加 `--resume` 会跳过已有完整 result 的 attempts，并重新执行未完成 attempts；若 case/prompt/fixture digests、subject、runner、resolved Codex executable/version、model、timeout、workspace-retention setting 或 repeat 不一致则拒绝续跑，避免把不同 inputs 的 attempts 合并成一份 evidence。

`subject-id` 是 evidence label，不是 isolation mechanism。Codex 可能同时发现同名 repo-level 与 user-level skill；这种情况下只能把 subject 描述为当前 CLI environment，不能宣称某个 candidate 或 release 被单独加载。做比较时还要固定 prompt、fixture、model、effort、sandbox、permissions 与 repeat count。

当前 canaries：

- `tiny-copy`：小改动的 scope 与 overhead；
- `stale-cursor`：consistency invariant 与 regression evidence；
- `spec-chain`：approved spec 的 end-to-end coverage。

Raw trace 是 authority；derived telemetry 只记录观察到的 commands、plan updates、reference reads、subagent-like events、usage、malformed lines 与 unknown events。缺失 telemetry 不能反向证明某个动作没有发生。

## Activation seed set

`activation-prompts.csv` 是小型 seed set，覆盖：

- implicit positive cases
- contextual cases
- explicit controls
- adjacent negative controls

真实 Codex 环境里可使用 `codex exec --json` 保存 trace，并记录：

- skill 是否 invoked
- reference file reads
- command count / repeated commands
- subagent count
- usage input/output tokens
- completion outcome

先人工跑一轮，再把真实 miss、false positive、绕圈案例加入 CSV。不要为了通过 eval 把 router description 扩成无边界的万能匹配器。

## Efficiency comparisons

Token reduction is accepted only when completion quality and required boundary protection remain intact. Compare runs with:

- the same repository commit, prompt, model, effort, and tool permissions;
- fresh sessions without prior exposure to the candidate instructions;
- outcome and verification quality scored before looking at token totals;
- input/output tokens, reference reads, tool calls, repeated commands, hashes, tests, subagents, and elapsed turns recorded separately.

Treat a single task or account-balance delta as noisy. Do not make a causal savings claim from contaminated controls, unmatched prompts, or a run that saved tokens by skipping required evidence. The useful signal is a repeated reduction in irrelevant work across direct edits, complex failures, fallback pressure, real security boundaries, and completion stopping cases.

## Promote learning without bureaucracy

A costly incident, reviewer finding, or appealing external framework begins as a candidate, not an automatic Softpowers feature. First classify it as a general router/method problem, a repository-local contract, a tool/runtime defect, a framework mismatch, or an evidence gap.

Encode the smallest useful behavioral probe before adding a broad rule. A serious incident may justify an immediate narrow safety or correctness fix, but a same-task repair proves only that repair. Claim repeated workflow improvement only after a comparable later task supports it.

Do not require background surveillance, numeric scores, intervention ledgers, mandatory multi-agent review, or an external plugin to learn from real work. The eval layer should also provide evidence for declining new machinery.

## External pattern intake

External repositories enter Softpowers through a pinned, evidence-bound candidate process:

- governance and verification scope: [`../docs/pattern-intake.md`](../docs/pattern-intake.md)
- pinned source registry: [`../docs/external-patterns.md`](../docs/external-patterns.md)
- candidate template and decided samples: [`candidates/`](candidates/)

A source review may end in `ADOPT`, `ADAPT`, `REJECT`, `DEFER`, or `ALREADY COVERED`. Documentation-only decisions do not require model runs. Any applied method, routing, packaging, or runner change receives fresh verification matched to its blast radius.
