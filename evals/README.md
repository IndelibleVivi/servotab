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
