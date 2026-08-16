# Activation eval notes

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
