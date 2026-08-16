# External Pattern Intake Samples — 2026-08

Status: `DECIDED`

这些 samples 示范当前选中来源怎样进入 Softpowers 的长期 intake。它们记录可吸收 kernel、调整方式、拒绝边界、可能的 probe 与 apply 后验证。当前文件本身不修改 router、methods、installer 或 runtime behavior。

## 1. Clean verifier and executable canaries

Decision: `ADAPT`

### Source

- Repository: `anthropics/defending-code-reference-harness`
- Pinned ref: `d3bea6b5793b5f3d59a75ebe69a58efa88383145`
- License: Apache-2.0
- Reviewed surfaces: `docs/best-practices.md`, `docs/pipeline.md`, `docs/security.md`, `harness/artifacts.py`, `.claude/skills/_lib/checkpoint.py`, captured canary outputs

### Distilled pattern

Candidate production与 candidate verification 使用隔离 context。只有可复现 artifact、最终 diff 或必要 evidence 穿过边界。Canary 使用已知 ground truth 检查真实 outcome。长运行把 transcript、result 与 progress 原子写盘，允许中断后恢复。

### Local signal

Softpowers 已有丰富 behavioral probes 与 matched-control 原则，当前 public tree 还缺少统一 executable runner、replayable run artifacts 和少量 micro-repo canaries。

### Existing coverage

- `BEHAVIORAL_PROBES.md` 已定义正例、负例与 expected behavior。
- `evals/README.md` 已要求 matched controls、fresh sessions 与先看 outcome。
- `scripts/` 已有 deterministic validation 与 packaging gates。

### Decision hypothesis

- Accepted kernel: clean grading、canary、durable trace、atomic result、resume、executable witness。
- Excluded machinery: security-specific recon/find/grade/judge/report/patch 全流水线；日常 task 强制 sandbox；普通 edit 的多 agent adjudication。
- Landing plane: eval / maintainer。
- Smallest useful delta: 先实现三个 canary case 与一个薄 runner，保持 runtime untouched。

### Probe

第一批 fixture：

1. `tiny-copy`：一处 copy change，要求零 reference、focused check、无 plan/subagent。
2. `stale-cursor`：预埋 consistency regression，要求定位 boundary、建立 regression evidence、修 source invariant。
3. `spec-chain`：完整 spec 与局部 tranche 同时存在，要求 coverage ledger 保留全部 requirements。

Programmatic assertions 检查 diff、tests、file scope、trace event 与 completion claim。主观判断只覆盖无法机械判定的 diagnosis quality 或 product texture。

### Verification if applied

- runner parser/schema unit tests；
- known pass / known fail fixture；
- interrupted write 与 resume test；
- candidate vs pinned previous release matched runs；
- 每个关键 canary 至少 3 次；
- router 没有改动时，不自动跑全部 activation seed set。

### Result

`ADAPT` approved for a future eval tranche. No runtime method change is authorized by this sample.

---

## 2. Paired skill evaluation without displacing user judgment

Decision: `ADAPT`

### Source

- Repository: `anthropics/skills`
- Component: `skills/skill-creator`
- Pinned ref: `f6656c1256d5a8adfa37db9110046ef20bac644c`
- License: Apache-2.0
- Reviewed surfaces: `SKILL.md`, eval schemas, benchmark aggregation and review workflow

### Distilled pattern

在相同 prompt、fixture 与执行条件下并行运行 candidate 与 baseline。客观 outcome 使用 assertions；主观质量保留 human qualitative review。记录 tokens、time 与 variance，先判断 completion quality，再比较 overhead。

### Local signal

Softpowers 计划证明 routing 与 methods 是否减少无意义流程，同时不能用低 token 掩盖 scope loss、缺少测试或错误 completion claim。

### Existing coverage

`evals/README.md` 已规定 matched repository commit、prompt、model、effort、permissions 与 fresh sessions，也已禁止从单次余额变化推导因果。

### Decision hypothesis

- Accepted kernel: matched pair、objective/subjective split、timing、variance、iteration viewer。
- Excluded machinery: 每次真实 user task 自动跑 baseline；所有 task 都需要 grader；主观 artifact 被机械 score 取代；用户 feedback 降为 benchmark 附件。
- Landing plane: eval / maintainer。
- Smallest useful delta: runner 支持 `candidate / previous-release / no-skill` 三种可选 baseline，case 自己声明是否需要 semantic grader。

### Probe

用同一 tiny-copy fixture 比较：

- current candidate；
- previous tagged Softpowers；
- 无 Softpowers baseline（只在研究新增价值时使用）。

先看 full outcome 与 required boundary，再看 reference reads、tool calls、tokens 和 elapsed turns。一个 baseline 若跳过必要 verification，即使更省 token 也不能胜出。

### Verification if applied

- baseline identity 与 candidate identity 写入 metadata；
- prompt、fixture、model、effort、permissions mismatch 时 fail closed；
- assertion grader 先跑 deterministic checks；
- semantic grader 不读取执行者自评；
- aggregation 输出 mean、variance 与 per-case evidence；
- subjective case 允许没有 numeric assertion。

### Result

`ADAPT` approved for eval design. The user remains final judge for felt quality and product texture.

---

## 3. Cross-host distribution without mandatory lifecycle

Decision: `ADAPT` + `REJECT` + `ALREADY COVERED`

### Source

- Repository: `obra/superpowers`
- Pinned ref: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- License: MIT
- Reviewed surfaces: README workflow and host installation model

### Distilled pattern

一套 composable engineering skills 可以通过多个 host 的原生 packaging 与 marketplace surface 分发，并提供清楚 onboarding。

### Local signal

Softpowers 当前是 source-distributed Codex pack，未来可能需要官方 plugin projection 或其他 host projection。现有 canonical method generation 已经具备单一 source 基础。

### Existing coverage

Softpowers 已覆盖 brainstorming、planning、execution、debug、TDD、review、verification、worktree、parallel 与 finishing 等方法域，并主动采用 quiet/proportionate routing。

### Decision hypothesis

- Accepted kernel: cross-host packaging、installation clarity、marketplace metadata、discoverability。
- Excluded machinery: mandatory brainstorming、固定 worktree、universal red-green、per-task subagent development、双 review、每个 task 先检查完整 lifecycle。
- Landing plane: packaging / distribution。
- Smallest useful delta: 在真实 distribution need 出现时，从 canonical catalog 生成 plugin manifest 和 host projection。

### Probe

无需模型行为 probe。先做 deterministic projection fixture：

- version、skill list、descriptions 与 canonical catalog 一致；
- generated projection 不成为第二 source of truth；
- plugin install/uninstall 不破坏现有 user-skill install；
- host-specific metadata 不反向污染 methods。

### Verification if applied

- generator check；
- exact manifest/schema validation；
- install smoke；
- duplicate root / conflicting install test；
- rollback/uninstall；
- existing pack selftest；
- public-tree audit。

### Result

Method domains are `ALREADY COVERED`. Distribution pattern is `ADAPT`. Mandatory lifecycle remains `REJECT`.

---

## 4. Evidence maturity without default scorecards

Decision: `ALREADY COVERED` + narrow `ADAPT`

### Source

- Repository: `QoderAI/better-harness`
- Pinned ref: `36c85c40ffb7596d413cc14bfbc8e66c741c182e`
- License: MIT
- Reviewed surfaces: Agent Work Loop model and evidence-state distinctions

### Distilled pattern

Configured mechanism、reachable route、current exercise 与 later comparable outcome 支持不同强度的 claims。Observation 缺失应保留为 unknown/unobserved，不能自动变成 defect 或 success。

### Local signal

Softpowers 需要防止 “文件存在 = 已生效”“当前 task 修好 = workflow 长期改善” 这类过度声明。

### Existing coverage

`Soft Verify` 已明确区分 capability existence、wiring、focused exercise、same-task repair 与 later comparable improvement，也要求 blocked check 进入 `Not verified`。

### Decision hypothesis

- Accepted kernel: evidence maturity 与 honest unknown。
- Excluded machinery: 默认五维评分、每次任务生成大报告、intervention ledger、background surveillance、finding-bound bureaucracy。
- Landing plane: existing verify language；future eval schema。
- Smallest useful delta: 当前 methods 无需修改。未来 eval result 可使用简洁 evidence-state field，前提是 runner 真正需要。

### Probe

`ALREADY COVERED` shadow probe：

Prompt 要求判断一个已配置但从未运行的 check 是否证明 feature 有效。期待 Softpowers 将存在、可达与实际执行分开，并把缺少 runtime observation 写成 `Not verified`。

### Verification if later wording changes

- blocked-verification case；
- configured-but-unexercised case；
- same-task repair vs later-improvement case；
- 一个 negative control，确保真实 missing contract 仍能被报告。

### Result

Current runtime method remains unchanged. This source mainly validates an existing Softpowers strength.

---

## 5. Own control flow without turning work into a DAG

Decision: `ALREADY COVERED` + `ADAPT`

### Source

- Repository: `humanlayer/12-factor-agents`
- Pinned ref: `d20c728368bf9c189d6d7aab704744decb6ec0cc`
- License: code Apache-2.0；content CC BY-SA-4.0
- Reviewed concepts: own prompts、own context、own control flow、pause/resume、compact errors、small focused agents

### Distilled pattern

LLM judgment嵌入由普通软件掌管的 state、permissions、execution 与 recovery。Context 和 control flow 应由应用持有，长任务需要清晰 pause/resume 与 compact failure evidence。

### Local signal

未来 Softpowers eval runner 需要可检查、可恢复、容易 debug 的 control flow。日常 Softpowers 已依赖 host-native agent behavior，不应被外部 orchestrator 接管。

### Existing coverage

- canonical methods = prompt ownership；
- progressive disclosure = context discipline；
- Worker Lanes = bounded focused agents；
- installer manifests = explicit state；
- runtime routing 仍由 Codex + user/repo context 决定。

### Decision hypothesis

- Accepted kernel: maintainer tooling 自己掌管 state、run identity、resume、error compaction。
- Excluded machinery: 把每个 coding task 编译成固定 DAG；用 deterministic stages 夺走 agent 的局部判断；要求用户管理 workflow engine。
- Landing plane: eval runner architecture。
- Smallest useful delta: future runner 使用显式 state machine 和 append-only trace，Softpowers runtime 保持 host-native。

### Probe

Runner interruption fixture：

- 在 case 执行后、grading 前停止；
- resume 后复用 immutable candidate output；
- 不重复执行已经终结的 stage；
- corrupt state fail closed；
- error packet 保留可采取行动的原因，避免把整段 noisy trace重新塞回 context。

### Verification if applied

deterministic unit/integration tests 足够；无需 model run，除非 runner 改变传给 Codex 的 prompt 或 permissions。

### Result

Runtime principle is `ALREADY COVERED`. Runner implementation guidance is `ADAPT`.

---

## 6. Thin eval runner and linear trajectories

Decision: `ADAPT`

### Source

- Repository: `SWE-agent/mini-swe-agent`
- Pinned ref: `a83fcae82d2a08f0ee0c688f9d137b3566c097f8`
- License: MIT
- Reviewed pattern: minimal control loop、linear history、independent subprocess actions、easy sandbox substitution

### Distilled pattern

Eval runner 保持薄、线性、可阅读。每个外部 action 有独立输入输出，trajectory 直接成为可回放 evidence。复杂性留给 model 与 case contract，runner 不发展成第二个 agent framework。

### Local signal

Softpowers 需要行为 evidence，但核心价值仍是 methods 与 routing。一个过重 runner 会重新制造项目试图减少的 ceremony。

### Decision hypothesis

- Accepted kernel: small runner、JSONL trace、independent process invocation、explicit adapter boundary。
- Excluded machinery: 把 Softpowers runtime 降为 bash-only agent；复制 mini-swe-agent 的完整 platform；为 benchmark 重写 Codex。
- Landing plane: eval implementation。
- Smallest useful delta: `prepare fixture → run Codex → capture JSON → assert → optional grade → summarize`。

### Probe

用 fake Codex stream 测：

- tool event 与 final response 顺序保留；
- interrupted JSONL 保留已完成 events；
- adapter 能识别 skill invocation、reference reads、commands、subagents 与 usage；
- unknown event type 被保存并标记，避免静默丢失。

### Verification if applied

- parser fixtures；
- malformed/truncated stream；
- subprocess timeout/exit；
- stable run metadata；
- one real Codex smoke after deterministic suite passes。

### Result

`ADAPT` approved as implementation style only.

---

## 7. Reproducible fixture identity and honest cache semantics

Decision: `ADAPT`

### Source

- Repository: `SWE-bench/SWE-bench`
- Pinned ref: `ca6e4e0d252f32f8762625b73575d5dee49d0a5a`
- License: MIT
- Reviewed pattern: fixed repository snapshots、containerized evaluation、saved logs、run identity、re-grading outputs

### Distilled pattern

Evaluation result 绑定明确的 fixture identity、candidate identity、environment 与 run id。Cache key 必须覆盖会改变结果的输入；保存的 raw outputs 可以被重新 grading，而无需重新执行昂贵 agent run。

### Local signal

Softpowers candidate、previous release 和 no-skill baseline 很容易因 repo state、model effort 或 permissions 不一致产生污染比较。

### Decision hypothesis

- Accepted kernel: immutable fixture identity、complete metadata、raw-run/regrade separation、honest cache key。
- Excluded machinery: 大型 benchmark dataset、重 Docker 基础设施、排行榜导向、把真实个人 repo 上传为公开 task。
- Landing plane: eval implementation。
- Smallest useful delta: run metadata 记录 fixture tree hash、Softpowers commit、host/model/effort/permissions、prompt digest 与 grader version。

### Probe

故意使用同一 run id、不同 candidate commit：

- runner 必须拒绝复用旧 result，或生成新 identity；
- grader version 改变时允许 regrade raw output；
- fixture 内容改变时 cache invalid；
- private path 不进入 public summary。

### Verification if applied

deterministic cache-key tests、regrade tests、metadata redaction tests；无需全套 model behavior run。

### Result

`ADAPT` approved for future eval identity contract.

---

## 8. Task / solver / scorer separation without an early framework dependency

Decision: `DEFER` + conceptual `ADAPT`

### Source

- Repository: `UKGovernmentBEIS/inspect_ai`
- Pinned ref: `286163f12aa627af22051bd95321bc6404e237ae`
- License: verify the exact reused component before copying code
- Reviewed pattern: dataset/task、solver、scorer、sandbox、approval、log separation

### Distilled pattern

Evaluation case、agent strategy、scoring 与 execution environment 使用独立 contracts。Raw run output 可以被不同 scorer 重新判断；task 定义不应锁死一种 solver。

### Local signal

Softpowers 的早期 eval runner需要区分 case、Codex adapter、assertion grader 与 semantic grader。当前规模很小，直接依赖成熟 eval framework可能扩大 dependency 和 concepts。

### Decision hypothesis

- Accepted kernel: clean internal interfaces for case / executor / grader / result。
- Excluded machinery: 第一版直接引入 Inspect dependency、复制完整 extension system、提前支持大量 model providers。
- Landing plane: eval architecture。
- Smallest useful delta: local dataclasses/JSON schemas 保持可替换，等 local runner 出现真实限制再评估 framework migration。

### Reopen conditions

- case 数量与 scorer 类型快速增长；
- multi-model / multi-sandbox 成为真实需求；
- local logging、retry 或 regrade 已开始重复造轮子；
- Inspect 提供显著更短 supported path，且 dependency cost 可接受。

### Verification if later adopted

先用现有 canaries 做 adapter parity；对比 raw outputs、scores、resume、cost 与 debugging clarity。Migration 不能只以“framework 更专业”为依据。

### Result

Dependency remains `DEFER`. Interface separation is accepted conceptually.

---

## 9. Generated plugin projection with canonical ownership preserved

Decision: `DEFER` + planned `ADAPT`

### Source

- Repository: `openai/plugins`
- Pinned ref: `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`
- Reuse note: no repository-level license file exists at this ref；inspect each plugin manifest and component before copying
- Reviewed pattern: `.codex-plugin/plugin.json` plus skills、agents、commands、hooks、MCP and assets

### Distilled pattern

Codex distribution 可以把多种 surface 收进一个 versioned plugin，manifest 描述 identity、capabilities、interface 与 bundled skills。

### Local signal

Softpowers 当前 installer 已成熟，plugin distribution 还没有明确 release requirement。手工维护第二套 manifest 会引入 drift。

### Decision hypothesis

- Accepted kernel: future plugin projection、single package identity、host-native discovery。
- Excluded machinery: 现在立即迁移；让 plugin manifest 成为 method source of truth；为填满 plugin surface 增加 agents/hooks/MCP。
- Landing plane: packaging / distribution。
- Smallest useful delta: distribution need 成立后，从 `VERSION`、skill catalog、README metadata 与 canonical methods 生成 manifest。

### Probe

Deterministic projection fixture：

- manifest version 与 `VERSION` 一致；
- skills 路径与 generated pack 一致；
- capability 只声明真实 bundled behavior；
- source-distributed installer继续可用；
- plugin projection 删除后可完全再生成。

### Verification if applied

schema、generation check、install smoke、host discovery、existing pack selftest、rollback path、public-tree audit。只有 implicit routing metadata 改变时才跑 behavior activation suite。

### Result

`DEFER` until a real distribution target exists.

---

## 10. Adversarial packaging fixtures without importing malicious payloads

Decision: `ADAPT` + `REJECT`

### Source

- Repository: `trailofbits/overtly-malicious-skills`
- Pinned ref: `4ffbf9461ef0505f9ce76a0d3694a18ec33ea531`
- License/reuse note: no license file exists at this ref；security research reference only
- Safety boundary: do not install or execute upstream skills

### Distilled pattern

Skill package 可以通过 misleading description、hidden document payload、bytecode artifact、environment access 或 prompt injection 绕过浅层 scanner。Public packaging audit 应检查实际 files 与 side effects，不能只相信 metadata。

### Local signal

Softpowers 已有 manifest digest、transactional install、safe uninstall 和 public-tree audit。未来 plugin distribution 会扩大 artifact surface，适合增加 inert adversarial fixtures。

### Decision hypothesis

- Accepted kernel: attack-shape inventory、synthetic inert fixtures、fail-closed audit cases。
- Excluded machinery: clone 后运行 upstream sample；把恶意 payload 放入 release tree；CI 安装未知 skill；复制无 license code。
- Landing plane: packaging security tests。
- Smallest useful delta: 本地构造无害 fixture，分别模拟 suspicious extension、symlink escape、unexpected executable、hidden archive content marker、environment-file inclusion 与 manifest/content mismatch。

### Probe

每个 fixture 只包含 inert marker：

- public-tree audit 应拒绝；
- error 指向具体 violated boundary；
- clean Softpowers pack 继续通过；
- scanner 不执行 fixture；
- test environment 无 network 和 secret access。

### Verification if applied

deterministic security tests、clean-tree control、platform path variations、archive/symlink handling。无需 model run。

### Result

Audit ideas are `ADAPT`. Upstream payload execution is permanently `REJECT` absent a separate isolated security-research project.

---

## Cross-source synthesis

当前十个来源共同支持四个方向：

1. **Executable claims**：canary、paired run、raw trace、independent grading。
2. **Thin maintainer tooling**：own state、linear trajectory、complete identity、regrade。
3. **Projection without duplicate authority**：canonical methods 生成 host packaging。
4. **Trust through inspected artifacts**：manifest、rollback、public-tree audit、inert adversarial fixtures。

它们没有授权改写现有 routing。Softpowers 的 daily-facing contract 继续是：

- 用户直接描述 task；
- 小任务直接做；
- 复杂度随真实风险增长；
- user intuition 能触发调查；
- mechanism 可以被挑战；
- outcome 与 product texture 被保留；
- evidence 支撑准确 completion claim；
- 输出随任务自然形成。
