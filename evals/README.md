# Servotab field evidence pack

`evals/` 保存 Servotab 自己的 subject evidence；通用 runner、schemas、process
containment、receipt contract 与 quota gate 已由 standalone Skill Field Lab companion
负责，不再 bundle 或投影进 Servotab plugin skills。

Servotab 继续拥有：

- `cases/`：二十四个 repository-owned canaries 及其 fixtures、assertions、expected overlays；其中二十个声明了非空的 `human_review_requirements`；
- `activation-prompts.csv`：较宽的 routing seed set；
- [`submission-test-cases.md`](submission-test-cases.md)：把现有 fixtures 整理成
  reviewer-ready 的 5 positive / 3 negative draft；它不是 portal receipt 或 submission claim；
- `candidates/`：外部 pattern intake 与 provenance decisions；
- `claims/`、`receipts/`、`decisions/`：项目自己的 evidence lifecycle；
- 根目录 `fieldlab-pack.json`：以 schema v2 `local-path` 直接声明当前 generated `plugins/servotab/skills/` tree，不复制第二份 runtime。

Field Lab 是 optional maintainer companion。Servotab 的安装、普通使用、release
payload 与 CI 都不依赖它；Servotab 也不安装、更新或卸载它的 CLI/controller
skills。

## No-spend gate

安装了当前 `fieldlab` CLI 的 maintainer 可以在 Servotab 根目录运行：

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

这三条命令不会启动 target model。`selftest` 会证明每个 unresolved fixture
至少失败一个 deterministic assertion，并在应用 `expected/` overlay 后全部通过。

当前 cases：

- `tiny-copy`：小改动的 scope 与 overhead；
- `stale-cursor`：consistency invariant 与 regression evidence；
- `spec-chain`：approved spec 的 end-to-end coverage。
- `owner-controlled-migration`：generic protocol 即使有研究价值，只要试图取代 authorized owner-controlled path 就判定为 `diverges`；
- `programme-reorder-review`：implementation PR 不能通过自写 decision log 批准 programme reorder。
- `adopted-foundation-review`：明确 adopted 的 foundational work 不因尚无 present consumer 被误判为越权。
- `repeated-review-scope-accretion`：第三轮 mixed-scope review 只修复 falsify accepted contract 的 blocker，同时保留并分离 adjacent、hardening 与 public-closure findings。
- `missing-host-test-seam`：material host boundary 缺少 cheap reproducer 时建立一个 bounded local surrogate，同时保留 named-host acceptance。
- `review-evidence-boundaries`：同一 bounded review corpus 同时保护 clean control、negative-space spec omission、false-green test 与 conditional finding 的 evidence boundary。

新增的 `local-reuse` 检查现有 normalizer 的真实复用；`weak-check` 保留一个原本绿色却不完整的测试，再用独立行为断言揭示缺陷。`scripts/test_behavior_fixtures.py` 现在对全部二十四个 fixture 复放文件/命令断言：基线必须失败，expected overlay 必须通过。`weak-check` 的实际候选测试也必须能拒绝旧实现；同时保留十二个审查反例与部分交付控制。它不复放 raw trace，不替代 Field Lab，也不执行模型。

0.6.4 候选新增三个诊断 case：`cross-boundary-diagnosis` 提供一个可执行的共享边界 admission 模型，包含健康 bypass 探针、一次被混淆的早期试验和一个独立残留延迟，验收要求真实的可比 pre/post 实验与成功交付，而不是计划或改过的计数器；`host-specific-diagnosis` 的桌面探针缺少 material native-host condition，因此无法排除该原因；`diagnosis-progress` 展示连续实验带来真实 causal progress 但整体尚未恢复，numeric failure count 不应触发无谓重启。它们沿用现有 Field Lab schema、baseline/expected overlay 与 semantic-review 边界；`scripts/test_diagnostic_fixtures.py` 提供确定性红/绿、残留症状、非绕过路径与错误修复的对照，不执行模型。

`discussion-intake` 检验“先完整吸收讨论、再决定范围”：fixture 是一段完全合成的产品讨论，重要目标和约束分布在前后，包含机制更正、吸引人的后段 subtopic，以及讨论内部提出但用户并未授权的对外动作。deterministic workspace gate 只检查 `INTAKE.md` 是否存在及写入范围是否精确；不以关键词裁定理解质量或权限判断。实际 trace 另外检查命令是否提及 `design.md` 路径；这不证明内容读取或 host selection，本地 fixture checks 也不复放这一层。完整覆盖、outcome 与 mechanism 的区分、更正和延后项的处理、以及阅读/采纳/执行许可的边界，均由 `human_review_requirements` 裁定。四个错误文本仍会通过结构检查，必须由语义审查拒绝；独立的写入反例验证修改原材料或额外文件会失败。没有 live target-model attempt 或已完成语义审查的声明。

新增 `tranche-only-plan` 覆盖显式 leaf 的阶段范围；`complete-notes` 用独立跨进程检查覆盖完整 CLI、持久化、迁移及失败路径。声明了 `human_review_requirements` 的 case 还必须经过 [最终验收](acceptance.md)：Field Lab 的自动 `pass` 本身不能关闭语义要求。

Delegate responsibility choice 由四个 canary 覆盖：

- `delegate-bounded-investigation`：failure、expected behavior、entry evidence、return contract 与 verification 都有界的 unknown-root-cause investigation，prompt 不命令 dispatch，agent 应从任务本身的 shape 选出一个 worker lane，Coordinator 保留 integration ownership 且不重复实现；
- `delegate-trivial-direct`：即使 lane 可用且协调收益看起来合理，trivial、可逆改动仍留在 direct path；
- `delegate-solo-request`：显式 solo request 禁止 delegation，即使工作本身达到 lane 门槛；
- `delegate-capability-unavailable`：host 不提供 subagent capability 时如实本地排序，不声称一个不存在的 lane。

正向 delegation 无法由当前 trace schema 的 ceiling 断言（只有 `max_*`，没有
`min_subagent_events`），因此 `delegate-bounded-investigation` 使用有界
`max_subagent_events: 1` 加 `reference_reads_include: ["delegate.md"]`，并把
topology（prompt 未命令时的真实 worker lane）、integration ownership 与证据边界
写成 `human_review_requirements`。这三个 negative canary 保持
`max_subagent_events: 0`。deterministic fixture pass 因此是必要条件而非
delegation 证明。2026-09-15 的一次授权 attempt 产生了一个 worker event，focused
test 与三条独立 semantic review 均获支持，但报告标题没有包含 case 要求的三条
exact literal strings，故 immutable receipt 为 `fail`，Servotab acceptance 为
`rejected`。它是 bounded host observation，不是 accepted evidence；第一次预算内
没有 retry。当前 canary 已移除这三条 literal label assertions；
deterministic workspace gate 只检查报告存在和 exact changed-file scope，报告中的
outcome、staffing 与 verification 是否有真实 runtime evidence 继续由三条逐项
`human_review_requirements` 判断，避免两个不同证据层重复裁同一语义。
在这一修订后的 case 上，另一次单独授权预算的 attempt 通过全部 deterministic
assertions；新的 separate-agent review 逐项支持 topology、integration 与 evidence，
Servotab acceptance 返回 `accepted`。该 receipt 只支持这一个 pinned
workspace-scoped attempt，不证明 exclusive causation、一般模型效果、安装激活或
长期改进。

任何 synthetic live attempt 都必须先生成 saved plan，再显式跨过 Field Lab 的
`run --live --max-invocations N` gate。Servotab 不把 live model eval 设为普通
release gate，也不自动增加 baseline、retry、repeat、full suite 或 LLM grader。

Raw trace 是 authority；receipt 与 summary 是 derived evidence。只有经过脱敏、确有
长期价值的 receipt 才进入版本库；`.fieldlab/` raw artifacts 保持 local-only。

## Worktree lifecycle evidence

0.6.3 增加三个 synthetic decision rehearsals：`worktree-reuse`（同任务复用、创建结果不明与 dirty prerequisite）、`worktree-organize`（显式调用只盘点及混合风险候选）、`worktree-authorized-park`（已有授权、保留未合并分支、状态变化只阻塞该项）。输入全部是合成观察；prompt 只授权写判断文件，不授权操作真实 workspace。

`worktree-organize` 包含 `assume-unchanged` / `skip-worktree` 隐藏 tracked 修改的候选。其显式入口由 required semantic review 核对实际 leaf 交付或读取证据（例如 `.agents/skills/worktree/SKILL.md`）；不要求重复读取 router reference，输出正确本身也不能证明方法已交付。

确定性 gate 检查输出存在及精确写入范围，三个反向对照证明错误决策文字仍可能通过结构检查；正确选择、可执行顺序和证据边界由 `human_review_requirements` 裁定。它们没有回放真实 agent 清理动作，也没有 live receipt。`scripts/test_worktree_git.py` 另外在一次性真实 Git 仓库验证底层机制，包括两条各覆盖上述两种 index 标记的参数化回归：只读内容核验不改真实 index，以及普通删除后保留分支仍无法恢复隐藏修改；Git regression 不能替代模型行为验收。需要实际执行清理的 target-agent evidence 时，另行定义可操作的 synthetic workspace case、saved plan 和显式调用预算；不要把这三个 rehearsal 的 pass 升格为该证据。

## Activation seed set

`activation-prompts.csv` 覆盖 implicit positive cases、contextual cases、explicit
controls 与 adjacent negative controls。不要为了通过 seed set 把 router description
扩成无边界的万能匹配器。真实 routing claim 还需要相同 repo revision、prompt、
model、effort、permissions 与可比较环境；一次 current exercise 不能冒充 later
longitudinal improvement。

Delegate seeds 另外区分 host/runtime capability 与 Servotab method selection：
Ultra、可用 slots 或已经发生的 harness spawn 都不能替代 independent-lane / clean-context
task topology，也不能单独证明 `delegate.md` 已被读取。

## External pattern intake

外部 repositories 通过 pinned、evidence-bound candidate process 进入 Servotab：

- governance 与 verification scope：[`../docs/pattern-intake.md`](../docs/pattern-intake.md)
- pinned source registry：[`../docs/external-patterns.md`](../docs/external-patterns.md)
- candidate records：[`candidates/`](candidates/)

一项 review 可以结束于 `ADOPT`、`ADAPT`、`REJECT`、`DEFER` 或
`ALREADY COVERED`。Documentation-only decision 不要求 model run；实际 method、
routing 或 packaging change 仍按 blast radius 做 fresh verification。
