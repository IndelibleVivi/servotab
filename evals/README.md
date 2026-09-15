# Servotab field evidence pack

`evals/` 保存 Servotab 自己的 subject evidence；通用 runner、schemas、process
containment、receipt contract 与 quota gate 已由 standalone Skill Field Lab companion
负责，不再 bundle 或投影进 Servotab plugin skills。

Servotab 继续拥有：

- `cases/`：十七个 repository-owned canaries 及其 fixtures、assertions、expected overlays；
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

新增的 `local-reuse` 检查现有 normalizer 的真实复用；`weak-check` 保留一个原本绿色却不完整的测试，再用独立行为断言揭示缺陷。`scripts/test_behavior_fixtures.py` 现在对全部十七个 fixture 复放文件/命令断言：基线必须失败，expected overlay 必须通过。`weak-check` 的实际候选测试也必须能拒绝旧实现；同时保留五个审查反例与部分交付控制。它不复放 raw trace，不替代 Field Lab，也不执行模型。

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
delegation 证明；真实 worker lane 仍需要一次授权的 host attempt 与独立 review。

任何 synthetic live attempt 都必须先生成 saved plan，再显式跨过 Field Lab 的
`run --live --max-invocations N` gate。Servotab 不把 live model eval 设为普通
release gate，也不自动增加 baseline、retry、repeat、full suite 或 LLM grader。

Raw trace 是 authority；receipt 与 summary 是 derived evidence。只有经过脱敏、确有
长期价值的 receipt 才进入版本库；`.fieldlab/` raw artifacts 保持 local-only。

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
