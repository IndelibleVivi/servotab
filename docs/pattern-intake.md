# External Pattern Intake

Servotab 可以持续学习外部仓库，同时保持现有 routing、方法边界和个人开发者取向稳定。外部工作提供 comparative evidence、candidate mechanism 与反例；只有本地任务、已观察失败、维护中的 contract 或经过验证的机会，才能批准一个 pattern 进入 Servotab。

这套流程属于 maintainer / eval plane。它不会给日常 repo work 增加前置 stage，不要求每次输出统一报告，也不会让外部框架获得修改 runtime routing 的默认权限。

## Stable boundaries

外部 pattern 先经过这些长期边界：

- 用户的 intent、felt friction、priority 与 product texture 是一等信号。用户可以先说“这里感觉不对”，无需提前翻译成标准工程术语。
- repo state、runtime behavior、tests、schemas 与 authoritative documentation 约束事实判断。
- agent 可以用证据挑战 proposed mechanism；requested outcome、hard constraints 与用户明确保留的体验不能被悄悄缩窄。
- routing 保持 quiet、progressive、proportionate。清晰、局部、可逆的小任务继续保持轻量。
- methods 提供 decision support 与 closure discipline。聊天输出格式只在用户要求或 external artifact contract 需要时固定。
- configured capability、reachable wiring、current exercise 与 later effectiveness 是不同强度的 claims。
- worktree、plan、TDD、subagent、review loop、checkpoint、score 与 ledger 都需要 present purpose。可用性本身不构成调用理由。

与这些边界冲突的 candidate 通常进入 `REJECT`。只有 Servotab、本地使用条件、host platform 或外部机制出现实质变化，才重开判断。

## Decision vocabulary

| Decision | 含义 |
|---|---|
| `ADOPT` | 机制与 Servotab 高度吻合，只需很少结构调整。 |
| `ADAPT` | 保留有效 invariant，重写 activation、scope、workflow 或 surface。 |
| `REJECT` | 当前机制与本地证据、成本或稳定边界冲突。 |
| `DEFER` | 可能有价值，当前缺少 caller、failure、host capability 或足够 evidence。 |
| `ALREADY COVERED` | 现有 Servotab 已达到同一有效 outcome，无需再增加机制。 |

Decision 必须同时写明 accepted kernel 与 excluded machinery。`REJECT`、`DEFER` 和 `ALREADY COVERED` 都属于有效学习结果。

每条 record 的顶层 `Decision` 必须只使用一个 vocabulary value。一个来源同时含有不同可拆分 component 时，保留一个代表当前 record landing 的顶层 decision，并用可选的 `Component outcomes` 逐项记录其他 outcome；不要把多个 value 拼成一个无法验证的 composite string。

## Intake lifecycle

### 1. Pin the source

记录：

- repository 与适用 license；
- exact commit 或 release；
- 实际读过的文件；
- review date；
- 当前关注的 narrow pattern。

后续复查优先比较 `last_reviewed_ref..current_ref`，围绕已有 focus 看增量。source 更新不要求重新精读整个仓库。

### 2. Distill the pattern

去掉产品名、营销语言和领域专用名词，写出可与 Servotab 比较的机制。

例如：

```text
finder 与 grader 使用隔离容器
→ candidate production 与 candidate verification 使用不同 context；
  只有可验证 artifact 穿过边界
```

### 3. Name the local problem

Candidate 至少对应一项本地信号：

- 已观察的 routing / method failure；
- 重复出现的无意义 overhead；
- evidence、reproducibility 或 recovery gap；
- packaging、compatibility 或 supply-chain boundary；
- host capability 变化导致更短 supported path 出现。

找不到 local problem 时，使用 `DEFER`、`ALREADY COVERED` 或 `REJECT: no demonstrated need`。外部项目的名望不会自动创建 Servotab requirement。

### 4. Choose the landing plane

| Plane | 典型内容 | Admission threshold |
|---|---|---|
| Runtime methods | router 与日常 design/debug/review/verify 行为 | 最高；需要重复或严重的本地证据 |
| Field Lab / maintainer | canary、runner、grader、trace、checkpoint、comparison | 大多数 harness 经验的首选落点；通用 machinery 不回流 Servotab payload |
| Packaging / distribution | plugin package、marketplace、manifest、legacy migration、release 与 supply-chain checks | 明确 compatibility 或 trust need |
| Docs / provenance | source registry、decision rationale、操作说明、attribution | 不改变 runtime behavior |

优先选择能够解决问题的最低 plane。

### 5. Run a shadow probe

修改通用 method 前，先建立最小 case，区分：

- 当前行为已经稳定成功；
- 当前行为存在方差或缺少清晰 contract；
- 当前行为稳定失败。

Shadow probe 可以使用 synthetic repository、replayable trace、known pass/fail fixture，或经过脱敏的真实任务。Probe 检查 outcome 与边界，避免只查关键词或固定句式。

### 6. Record the decision

Decision record 至少包含：

```text
Source
Pinned ref
Reviewed files
Review date
Distilled pattern
Observed local problem
Landing plane
Decision
Component outcomes (optional; one vocabulary value per named component)
Accepted kernel
Excluded machinery
Probe
Verification if applied
Reopen condition
```

### 7. Apply the smallest delta

一次 intake 可能只产生：

- 一条新的 behavioral probe；
- 对现有 method 的窄幅澄清；
- router metadata 的局部调整；
- standalone Field Lab / eval companion 的一种能力；
- packaging check；
- docs / provenance 记录。

读过一个优秀仓库，不会自动导出新 skill、新 lifecycle stage、新 dependency、统一 response schema 或后台进程。

### 8. Verify repair

当前 case 通过后，可以声明：

```text
candidate repair verified
```

它证明本次 repair。更广泛的 “Servotab 已经长期改善” 需要 later comparable task、matched repeated runs 或另一个 independent case。

### 9. Promote cautiously

Pattern 进入 runtime method 前，至少满足一项：

- 同类真实任务再次暴露该 gap；
- 多个 matched cases 显示稳定收益；
- serious correctness / security boundary 需要立即窄修；
- host contract 已实质改变，旧 route 不再可靠。

进入 eval、packaging 或 docs plane 的门槛可以更低，因为这些改动不会扩大日常 routing。

## Verification by change surface

每个实际 apply 都要 fresh verification。测试范围由改动可能破坏的 surface 决定。

| Change | Minimum fresh verification |
|---|---|
| Source note、decision rationale、attribution | ref/link inspection、format check；适用时跑 public-tree audit |
| Candidate record 或 fixture | schema/fixture validation 与一个 known expected result |
| Local method wording | affected probe + 一个 adjacent negative/control case |
| Router description / activation topology | matched positive + negative cases；因 activation 有方差，需要重复运行 |
| Shared closure / verification contract | 覆盖受影响 task classes 的 representative canaries |
| Generator / canonical projection | build、sync、exact manifest、generated-tree checks |
| Plugin package / legacy migration | manifest、marketplace、digest、read-only preflight、explicit retirement 与 filesystem tests |
| Field Lab runner / grader | 在 companion repo 做 deterministic parser/schema tests + known pass/fail fixtures |
| Release candidate | full deterministic gate + representative behavior suite |

Documentation-only intake decision 通常不需要 model run。局部 method edit 也无需自动重跑完整 behavior suite。Router 与 shared contract 的 blast radius 更大，验证随之扩大。

Activation 相关 change 可以从 positive/negative 各 3 次开始；争议较大或方差明显时扩大到 5 次以上。数字根据实际 variance 调整，不写成永久仪式。

## Reopen conditions

Recorded decision 在以下情况下重开：

- comparable Servotab task 再次出现同一 gap；
- external source 对 reviewed mechanism 做了 material change；
- Codex 或其他支持 host 改变 skill/plugin contract；
- 新的 security、privacy 或 compatibility boundary 出现；
- deferred candidate 获得具体 caller；
- 当前 probes 已无法代表真实工作。

Stars、launch announcement 和 repository size 只提供 discovery signal。

## What stays outside runtime

External learning 不应默认引入：

- background surveillance；
- 每个任务的 numeric score；
- intervention ledger；
- mandatory multi-agent review；
- per-task baseline experiment；
- 为了证明 method 存在而固定输出流程报告；
- 自动追踪所有相似仓库。

真实工作触发 intake；release tranche 可以做 pinned-source delta sweep。其余时间，连帽衫小机继续直接工作。
