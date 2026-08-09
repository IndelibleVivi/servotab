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
