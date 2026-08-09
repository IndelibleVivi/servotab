# Behavioral Probes — v0.2 Activation

这些 probes 用来观察 router 是否正确触发、按需读取 reference，并保持小任务轻量。它们包含正例和负例；不要只测“会不会用”，还要测“该沉默时会不会沉默”。

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

## Explicit controls

用这些控制 direct leaf 是否仍然可用：

```text
$soft-debug 复现并修复这个 bug。
$soft-review 审当前 diff。
$soft-tdd 为这个 parser contract 做 strict red-green。
```

Expected：直接加载对应 leaf；不依赖 router reference，也不出现跨-skill loading 承诺。
