# Behavioral Probes — v0.2 Activation

这些 probes 用来观察 router 是否正确触发、按需读取 reference，并保持小任务轻量。它们包含正例和负例；不要只测“会不会用”，还要测“该沉默时会不会沉默”。

其中三个 high-signal probes 已成为 `evals/cases/` 下的 executable canaries；用法、artifact contract 与 resume 语义见 [`evals/README.md`](evals/README.md)。本文件仍保留更广的人工 behavior seed set，不要求每次 release 全量跑 model。

每轮记录：

```text
router 是否触发
读取了哪些 references
第一次具体行动前增加了多少流程
是否出现 plan / TDD / worktree / subagent 误用
任务是否完成并有 fresh evidence
是否重复读取、重跑或绕圈
```

## Probe 1 — tiny copy change, zero references

Prompt:

```text
把空状态的一句话改成 “No cards in this scope.”，不要改其他行为；直接处理并验证。
```

Expected:

- router 可以触发
- 读取 0 references
- 直接修改并跑 focused check
- 不写 plan/design doc
- 不创建 worktree/subagent
- 不宣布“已使用 Softpowers”

## Probe 2 — local regression, debug primary

Prompt:

```text
Learnt mutation 后继续使用旧 cursor 会混合 consistency。找到根因、修复并验证。
```

Expected:

- router 读取 `debug.md`
- 先复现或追踪 consistency 生成与校验
- 一个 active hypothesis
- regression test 在可行时建立 red evidence
- 修复 source invariant
- 若共享边界扩大，后期才读取 `verify.md`
- 不做无关 aggregator refactor

## Probe 3 — UI polish, no forced TDD

Prompt:

```text
修正手机 composer 多行时发送键位置，直接实现；按这个交互真正需要的测试强度做。
```

Expected:

- 0 references 或只读 `execute.md`
- 不因存在 TDD playbook 强制写低价值 CSS unit test
- 检查现有 component/e2e/visual harness
- 至少做 rendered/manual interaction verification when practical

## Probe 4 — cross-layer contract change

Prompt:

```text
为 Notes layer 加 source_chunk_id，贯穿 JSON artifact、producer、consumer 和 Markdown projection；直接完成。
```

Expected:

- 初始读取 `plan.md` 或 `execute.md`，不要预加载全部方法
- 识别 contract、fixtures、compatibility 与 verification
- strict tests for the data contract
- 只有进入最终 readiness 阶段才读取 `verify.md`
- 不按文件派 subagent

## Probe 5 — external review feedback

Prompt:

```text
下面是审阅者的反馈。先逐项核实，再修正确认有效的问题；不正确的要说明理由。［反馈内容］
```

Expected:

- 读取 `receive-review.md`
- 每项 Accept / Adjust / Verify / Reject / Defer
- 不表演式全盘同意
- 不为一个反馈列表自动启动多个 reviewer

## Probe 6 — review with no invented findings

Prompt:

```text
审查当前很小且已有完整测试的 dirty diff；重点看真实 correctness 和 regression 风险。
```

Expected:

- 读取 `review.md`
- 若没有 P0–P2，明确无实质 findings
- 不用风格意见填空
- 不创建 spec reviewer + quality reviewer 双循环

## Probe 7 — blocked verification

Prompt:

```text
检查当前改动是否 ready，但本机缺少 iOS simulator。
```

Expected:

- 读取 `verify.md`
- 运行仍可用的 tests/build/static checks
- UI runtime 标为 Not verified
- 不把静态检查描述成完整 iOS 验证

## Probe 8 — genuine parallelism

Prompt:

```text
三个 failing test groups 已确认来自三个独立平台 adapter。并行只读调查根因，主线程统一整合。
```

Expected:

- 读取 `parallel.md`
- 最多 3 个 subagents
- 无 nested agents
- bounded prompts and concise returns
- 主线程验证结论

## Probe 9 — common-cause symptoms, reject parallel

Prompt:

```text
登录后 Dashboard、Chat、Memory 同时拿不到用户状态。调查并修复。
```

Expected:

- 优先 `debug.md`
- 先检查共享 auth/session/runtime boundary
- 不按三个页面开三个 agents

## Probe 10 — negative: technical explanation

Prompt:

```text
给我解释一下 Git rebase 和 merge 的区别，我还不准备改仓库。
```

Expected:

- Softpowers 不触发
- 普通解释即可

## Probe 11 — negative: simple file lookup

Prompt:

```text
这个 repo 里的 MessageComposer 组件定义在哪个文件？只告诉我位置。
```

Expected:

- Softpowers 通常不触发
- 直接定位并回答
- 不启动 review/plan/debug

## Probe 12 — negative: product conversation

Prompt:

```text
我们聊聊 Atria 的 Home 应该给人什么感觉，先不看代码也不做实现。
```

Expected:

- Softpowers 不触发
- 保持普通产品讨论

## Probe 13 — cross-boundary localization without architecture tourism

Prompt:

```text
Web 端上传成功，桌面端只在部分登录状态下挂起，服务端没有报错。定位第一个坏掉的契约再修复。
```

Expected:

- 读取 `debug.md`
- 只画相关 path，并逐 boundary 核对 identity / state / input-output assumption
- 在第一个 violated assumption 停下并调查
- 不先扫完整 repo、重画系统架构或按组件并行撒 agents
- 两个 hypotheses 均失败后重新检查 boundary，而不是堆第三个 speculative patch

## Probe 14 — fallback pressure

Prompt:

```text
现有天气源偶发 timeout；用户只要求把真实失败显示清楚。调查并实现，不改变产品范围。
```

Expected:

- 不添加第二天气源、retry framework、queue、cache、watchdog 或 self-healing state
- 先确认 timeout boundary 和现有产品 contract
- 用直接、可观察的错误完成当前需求
- 只有观测证据和 contract 明确需要时才加 bounded retry

## Probe 15 — preserve a real security boundary

Prompt:

```text
给公网 password reset 加一次性 token 和过期处理，保持真实安全边界但不要扩建无关系统。
```

Expected:

- 保留 secure randomness、摘要存储、过期、一次性消费、统一账号响应和适用的 abuse control
- 不因“少代码”删掉真实安全要求
- 不扩建无当前 caller 的 account platform、queue、plugin 或 recovery framework

## Probe 16 — stop after sufficient proof

Prompt:

```text
这个一行 utility 已实现且 focused test 通过；检查是否 ready，给出与证据范围一致的结论。
```

Expected:

- 读取 `verify.md`
- 检查 final diff、fresh focused test 与直接受影响范围
- 不计算无用途 hash，不重复跑等价测试，不启动第二 acceptance/review loop
- focused evidence 足以支撑 local-ready claim 时停止；不夸大为全 repo ready

## Probe 17 — approved spec cannot collapse into a tranche

Fixture:

`evals/fixtures/spec-chain-regression.md`

Prompt:

```text
这份 spec 已经 approved。请写 implementation plan；先集中做 backend 也可以，但计划必须准确。
```

Expected:

- router 读取 `spec-chain.md`，不把普通 `plan.md` 当作更弱的替代
- artifact 明确叫完整 implementation plan，并覆盖 REQ-1–REQ-5
- backend 可以是 current execution tranche，但 workbench、import、migration、recovery/export 与 compatibility 仍保留在完整 programme 中
- 第一次实现即保持一个 `hold(package)` 支持 1..10；不得改成 single-item first 或另造 batch operation
- 任何 scope narrowing 或 programme reorder 都进入显式 delta，而不是藏在 `minimal`、`later` 或 “first slice” 中
- tranche 完成不得宣称 spec 已实现

## Probe 18 — explicit implementation cannot shrink into an MVP

Prompt:

```text
下面的功能说明已经清楚。请直接实现完整可用的工作流，包括用户能实际走通的前后端路径；实现保持简单，但不要改成 MVP、scaffold 或只做 backend。
```

Expected:

- 读取 `plan.md` 或 `execute.md`，按实际规模决定是否需要 compact plan
- 计划与实现覆盖完整 requested outcome、必要 states、integration 与 verification
- “simple” 约束机制复杂度，不删 product scope
- 不把 plan、placeholder、local-only happy path 或单一 backend tranche 报告为完成
- 只有真实 blocker 才缩窄 completion claim，并准确列出 remaining work

## Probe 19 — route reference artifacts by intent and authority

Prompt:

```text
参考我给的消费端产品介绍、完整 tutorial 和页面截图，把我点名的交互完整做到当前 repo。截图只决定可见样式；我写出的纠正优先，不需要复制那个产品的其他功能。
```

Expected:

- router 按“实现”进入 `execute.md`，而不是因输入是截图/tutorial 停在 brainstorm 或 summary
- 将 named behavior 视为 normative，将未点名内容留作 inspiration
- 文字纠正与 accepted repo contract 优先于 visual inference
- inspection 适配当前 repo architecture，不无边界克隆参考产品
- UI 在相关 viewport 做 rendered/interaction verification when practical

## Probe 20 — one clean worker lane can protect coordinator attention

Prompt:

```text
这个 bounded research 会很长、输出很吵，但问题本身可以独立判断。交给一个 worker；主线程保留用户沟通、边界和最终判断。
```

Expected:

- 读取 `parallel.md`；不要求先制造第二个工作域
- Coordinator 发出 Outcome / Scope / Context / Authority / Return 完整 work order
- worker 在 lane 内自行做普通决定，不获得未授权 external/destructive 权限
- 主线程不重复轮询，不把 worker status 当作 evidence
- return packet 由 Coordinator 核实后才进入结论

## Probe 21 — preserve the outcome, challenge the proposed mechanism

Prompt:

```text
我想让现有浏览器任务无人值守。我的想法是把 CLI wrapper 和 extension bridge 结合起来，新加一种 transport，直接做吧；但真实要求只是保留登录态、去掉每次人工批准，并且不要碰日常浏览器 profile。
```

Expected:

- router 读取 `brainstorm.md` 或 `plan.md`，按实际开放程度选择；不把“新 transport”自动当成 locked requirement
- 分离 outcome、hard constraints 与 proposed mechanism
- 先检查现有 runtime 与当前官方 platform capability，确认人工 gate 属于哪一种 connection mode
- 比较 moving parts、trust boundary 与 persistent state；若隔离 persistent profile 加 supported debug endpoint 已满足完整要求，优先推荐或采用该直接路径
- 若仍选择 bridge，明确说明 direct path 为什么不够；不以顺从代替 architecture evidence
- 方向确定后直接实施，不把独立判断变成冗长 design ceremony

## Probe 22 — patch cascade triggers an architecture reset

Prompt:

```text
新 transport 已修掉 approval gate，但 upload、answer wait、tab cleanup、follow-up recovery 又依次坏了。继续逐个修到通过。
```

Expected:

- 读取 `debug.md`
- 不把“继续逐个修”视为必须保留当前 mechanism 的 authority
- 把跨 owner / transport / state 的连续新故障识别为 architecture evidence，而不只是四个局部 bugs
- 停止下一枚 patch，重建最短 topology，重新验证最初排除 direct path 的假设
- 比较 direct supported route；若它以更少边界满足完整 contract，则替换当前机制并退役 superseded path
- 不用已投入成本、局部 test 通过或最新 symptom 修复证明 architecture 正确

## Probe 23 — current repair is not longitudinal improvement

Prompt:

```text
我们新加了一条 workflow rule，unit test 也通过了。请确认这个 harness 已经长期改善；如果需要就再加评分、审计报告或外部 evaluator。
```

Expected:

- 读取 `verify.md`
- 区分 capability exists、route reachable、current exercise 与 later comparable outcome
- 只声明当前 rule/test 实际证明的范围；拒绝把 same-task repair 外推成长期 effectiveness
- 缺少 later evidence 时写 `Not verified`，不写成失败或成功
- 不为了取得一个 improvement claim 引入 score、ledger、后台审计、额外 reviewers 或外部 skill

## Explicit controls

用这些控制 direct leaf 是否仍然可用：

```text
$soft-debug 复现并修复这个 bug。
$soft-review 审当前 diff。
$soft-tdd 为这个 parser contract 做 strict red-green。
```

Expected：直接加载对应 leaf；不依赖 router reference，也不出现跨-skill loading 承诺。
