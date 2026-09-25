# Servotab for Codex

[English](README.md) | 简体中文

[![Validate](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml/badge.svg)](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml)
[![License: layered](https://img.shields.io/badge/license-SUL--1.0%20%2B%20CC%20BY--NC--SA%204.0-blue.svg)](LICENSING.md)

Servotab 是一个 independent、community-maintained 的 Codex engineering plugin：清楚的改动保持直接，风险和不确定性升高时才加载更强的方法，最后用 fresh evidence 关闭真实 outcome。

> Method as exponent, not machinery.

最新 GitHub release：**[`0.6.4`](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.4)**，把已合并的 discussion-intake rehearsal 一起纳入 24 个 case 的 source pack，集中改进 `debug` 与 `verify` 的跨边界实验选择和结论范围，并小幅对齐 `execute` 的失败处理交接。其中 20 个 case 声明了非空的 semantic-review requirements，并保留十二个对抗控制；router／十二个 leaves／70 个文件的 package topology 不变。见 [0.6.4 release notes](docs/releases/0.6.4.md)。Tag 与 release receipt 证明 exact source 和 package identity，但不证明已安装、部署网站、更新目录或改善 live model behavior。

另行观察的 [OpenAI Plugins Directory listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94) 现在显示版本 `0.6.4`、开发者 `Yifei Fang`，并列出包含 `Worktree` 在内的完整 13 个 Servotab skills。tag 当时的 Directory 仍显示 `0.6.3`，那次观察作为历史保留。GitHub release 与 Directory publication 依旧被刻意记录为不同状态，listing 本身也不暴露 package digest。具体证据和边界见 [current state](docs/current-state.md) 与历史 [0.6.3 release notes](docs/releases/0.6.3.md)。

## 它做什么

Servotab 保持四个稳定承诺：

- Clear changes stay direct.
- Risk brings stronger method.
- Fresh evidence closes the loop.
- The requested outcome stays whole.

日常 repository work 只需正常描述任务，不必先挑 method。唯一具备 implicit-invocation eligibility 的 router 是 `servotab`；其余 12 个 leaf skills 都是 explicit-only shortcuts。它们不会覆盖你的 prompt、`AGENTS.md`、repo rules、权限边界、Git decision 或 deployment authority。

Servotab 也不会把日志、截图、review、旧计划或 generated artifact 自动当成指令。它们可能是 evidence；当前用户意图、accepted specification 与 canonical source 才决定工作方向。

当前 release 进一步明确了讨论材料的吸收方式：先覆盖重要目标与约束，再选择实施重点；分开看待需求与建议机制，为重要内容的舍弃或延后保留理由，并区分阅读覆盖、采纳判断和执行权限。明确限定的小任务仍保持有界，不新增 method、强制台账或审批轮次，见 [Design](methods/design.md)。

## 安装

在 ChatGPT 打开 [Servotab 官方 listing](https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94)，即可添加已公开上线的 plugin。

如果要 inspect source 或做 maintainer testing，可以从 public checkout 通过 repository marketplace 安装 tagged 0.6.4 package：

```bash
git clone --branch v0.6.4 --depth 1 https://github.com/IndelibleVivi/servotab.git
cd servotab
codex plugin marketplace add .
codex plugin add servotab@personal
```

`.agents/plugins/marketplace.json` 定义 repo marketplace `personal`，它指向 `plugins/servotab/`。`servotab@personal` 是当前 selector。

安装后请新开一个 Codex task 或 process，让 skill discovery 重新生成。先确认 package 已安装且启用：

```bash
codex plugin list --marketplace personal
```

当 checkout 的 `VERSION` 为 `0.6.4` 时，输出中应出现：

```text
servotab@personal  installed, enabled  0.6.4
```

如果本机同时有 `jq` 与 `rg`，可以进一步检查 fresh-process prompt input：

```bash
codex debug prompt-input "Check Servotab discovery." \
  | jq -r '.[].content[]?.text // empty' \
  | rg 'servotab:servotab'
```

命令应返回名为 `servotab:servotab` 的 installed plugin skill entry。2026-08-31，`0.4.0-rc1` 在 macOS 与 `codex-cli 0.147.0` 上完成过 source-checkout marketplace route、installed/enabled receipt 与 fresh-process router discovery。2026-09-05，当前 maintainer machine 又安装了 `0.6.0` source candidate，取得 69-file source/cache exact match，并在 fresh-process prompt input 中观察到 `servotab:servotab`。2026-09-06，同一台机器从 clean 的 0.6.1 release source 刷新 `servotab@personal`，核验 installed/enabled version 0.6.1、无 symlink 的 69-file source/cache exact match，以及 fresh-process `servotab:servotab` discovery。这些都是针对具名 payload 与具名机器的有限 compatibility / discovery receipts，不是猜测的最低版本承诺、implicit use 或模型效果的证明，也不代表所有 Codex client 都已验证。

这条 source-checkout 路径与已经公开的 directory payload 始终是两个独立状态。Tagged GitHub source 与最近观察到的 directory listing 现在都是 `0.6.4`，但两者互不证明，这里也不声称本机安装了 directory package。公开 listing 不暴露 archive digest，因此也不声称 directory payload 与任一 GitHub asset byte-identical。它取代旧版 `install.sh` / root `skills/` global installer；前述本机 receipt 也不会外推到其他机器或证明 live model behavior。

如果其他本机仍有 manifest-owned Softpowers `0.3.0-rc5` 或更早 global layer，请先读 [迁移指南](docs/migration-from-softpowers.md) 和 [current state](docs/current-state.md)。当前 maintainer roots 已完成 manifest-driven retirement 并验证为 clear；不要把这条 receipt 当成手动删除其他机器旧目录的许可。

## 怎么用

普通任务直接说：

```text
修复移动端输入时消息气泡上移的问题，找到根因后直接实现并验证。
```

Router 会按任务的真实 pressure 决定保持 direct，还是读取一份相关 reference。它不会宣布内部分类，也不会因为 method 可用就制造 plan、worktree、TDD、subagent 或第二轮 review。进入深层执行前，它还会先确定 responsibility：有界、noisy 或足够实质的 lane 可以交给一个 worker；显式 solo request 留在主 session；trivial 工作或频繁的 cross-owner 决策不会为了 coordination benefit 被拆分。Coupling 本身从不强制走主 session，一个 responsibility 内部耦合的部分只需留在同一个 lane 里。

明确需要某个 method 时可以直接调用：

```text
$review 审查当前 dirty diff，只报告可操作的 P0–P2 findings。
```

```text
$tdd 为这个 stale cursor bug 建立严格 red-green 回归证据。
```

```text
$spec-chain 依据这份 approved spec 建立完整 implementation plan；当前 tranche 不得替代完整 scope。
```

0.6.3 release 还会从普通请求里识别 workspace 生命周期：

```text
找回昨天实验的现场，先复用同一任务的 workspace，再判断是否需要另建。
```

```text
$worktree 盘点这个 repo 的 worktrees，建议哪些保留或收起；现在不要删除。
```

调用 `$worktree` 不等于要求新建 checkout。暂停的未合并实验可以保留 durable named branch 和恢复入口，再按授权移除目录。移除目录、删分支、丢弃数据和 prune 登记是不同动作；ignored 本地数据、被 index 标记隐藏的 tracked 修改、detached 成果、活跃宿主任务和暂时离线的存储都需要分别处理。已获明确授权且状态没变的批量项可以执行，不确定项单独保留。这版不新增 cleanup daemon、runtime dependency 或全局 workspace 数据库。

## Method set

Plugin 一共包含 13 个 skills：一个 implicit router 和 12 个 explicit leaves。

| Skill | Activation | 用途 |
|---|---|---|
| `servotab` | implicit eligible | 日常 repo work 的 quiet router |
| `design` | explicit only | 把仍有关键开放决策的 idea 变成可实现方向 |
| `spec-chain` | explicit only | 让 approved spec 的完整 scope 穿过 plan 与 execution |
| `plan` | explicit only | 为 settled multi-step work 建立实际 sequencing |
| `execute` | explicit only | 按清楚的 request 或 plan 完整实现 |
| `debug` | explicit only | 用 bounded hypotheses 和 boundary localization 修复根因 |
| `tdd` | explicit only | 对适合 test-first 的 contract、state 与 regression 做 risk-based TDD |
| `review` | explicit only | 做一轮 findings-first、evidence-backed review |
| `review-feedback` | explicit only | 先核实 external feedback，再采纳、调整或拒绝 |
| `verify` | explicit only | 用 fresh、risk-matched evidence 支撑 completion claim |
| `worktree` | explicit only | 选择、复用、恢复、收起和按明确授权清理 workspace |
| `delegate` | explicit only | 在深层执行前确定 responsibility；只在值得时把 bounded lane 交给一个 worker |
| `finish` | explicit only | 检查 final tree，并只执行已授权的 Git / PR / cleanup action |

Method 不创造权限，也不把 source-complete、installed、deployed、live、submitted 与 published 混成同一个状态。

## Source 与 package architecture

```text
methods/*.md + scripts/skill_catalog.py        canonical method + metadata source
                    │
                    ▼
          scripts/build_skills.py
                    │
                    ▼
plugins/servotab/
├── plugin.json                               portable Agent Plugins manifest
├── .codex-plugin/plugin.json                 compatibility fallback
├── LICENSE + NOTICE.md                       package-local rights boundary
├── skills/servotab/                          implicit router + 12 references
├── skills/{design,...,finish}/               12 explicit leaves
└── assets/                                   curated package assets

.agents/plugins/marketplace.json              repository marketplace entry
PACK_MANIFEST.json                            exact derived payload identity
```

根目录的 `plugins/servotab/plugin.json` 是 portable package entry point；`.codex-plugin/plugin.json` 作为旧版 Codex package reader 的同步 compatibility fallback 保留。验证会拒绝两份 manifest 在 identity 或 OpenAI interface 上发生漂移。

`methods/*.md` 是 12 个 method bodies 的唯一 canonical source；`scripts/skill_catalog.py` 是 names、descriptions、invocation 与 skill-icon source metadata 的 catalog。`plugins/servotab/skills/**` 是 generated projection，不要直接修改。Root `assets/` 保存 canonical identity assets 与十二枚 method glyph sources；generator 会把每个 skill 的透明 SVG / 400px PNG，以及 manifest 需要的 `composer-icon.png` 与 `logo.png` 投影进 plugin package。Paper-backed icon fallback 保留在 canonical assets 中，不进入默认 runtime payload。

已发布的 0.6.4 release 是 70-file manifest-owned payload，保持 one-router/twelve-leaf topology。它保留既有 portable root manifest、Windows-safe 文本身份、responsibility routing 与 worktree 生命周期指引，再加入 discussion-intake coverage 和 evidence-scoped diagnosis。Source pack 共 24 个 case，其中 20 个需要 semantic review，12 个是 adversarial controls。Release receipt 与 public asset readback 证明 tagged revision 的 source/package consistency；它们不证明 live model behavior、安装、生效或网站部署。公开 Directory listing 已单独观察到 `0.6.4`，这只说明 listing 层面的公开可见，不代表本机安装或行为效果。相关证据和缺口在 release notes 与 current state 中分别记录。

以下路径各有不同责任：

- `evals/` 与 `fieldlab-pack.json`：Servotab-owned behavior cases 和 Field Lab schema v2 subject pack；
- `site/`：Astro static website source，独立于 plugin runtime；
- `docs/current-state.md`：易变的 release / installed / deployed / live 状态；
- `docs/migration-from-softpowers.md`：旧 global installer layer 的一次性迁移；
- `AGENTS.md`：canonical / generated / release / authorization 的稳定 repo contract。

## Optional maintainer Field Lab

Servotab 保留 project-owned behavior cases，但不 bundle 通用 runner、schemas 或 controller skill。安装了 standalone `fieldlab` CLI 的 maintainer 可以运行不启动 target model 的 gate：

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

任何 synthetic live attempt 都需要单独计划和显式 invocation budget；它不是普通 build、install 或 release gate。完整 evidence contract 见 [evals/README.md](evals/README.md)。

## Maintainer checks

生成 projection：

```bash
python3 scripts/build_skills.py
```

Fresh deterministic gate：

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with-requirements requirements-dev.txt python3 scripts/validate.py plugins/servotab/skills
uv run --with-requirements requirements-dev.txt python3 scripts/generate_pack_manifest.py --check
uv run --with-requirements requirements-dev.txt python3 scripts/selftest.py
uv run --with-requirements requirements-dev.txt python3 -m unittest discover -s scripts -p 'test_*.py' -q
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

`scripts/selftest.py` 在 disposable fixtures 中检查 package identity、13-skill topology、source/generated sync、retired IDs、manifest、per-skill icon assets、marketplace route，以及 legacy helper 的 read-only preflight 与显式 one-layer retirement。它不安装 live plugin，也不提交 OpenAI directory update。

Website 的独立 build contract 见 [site/README.md](site/README.md)。

```bash
cd site
npm ci
npm test
npm run build
```

## 发布产物与验证边界

已公开的 [Servotab 0.6.4 GitHub Release](https://github.com/IndelibleVivi/servotab/releases/tag/v0.6.4) 提供用于 repository marketplace 的 `servotab-0.6.4-source.zip`，以及仅含 70 个 manifest-owned plugin 文件、供 owner 自行上传目录的 `servotab-0.6.4-plugin.zip`。较早 release assets 保持不可变历史。归档不会自动安装依赖或改动宿主。

`release-receipt.json` 将两个 ZIP 绑定到同一源码 commit、tree 与包 manifest；`SHA256SUMS` 覆盖两个 ZIP 和 receipt。摘要只能核对一致性，不能单独认证发布者身份，仍需检查 GitHub 来源。完整操作见 [Releasing](docs/releasing.md)。

维护校验使用 Python 3.10+，依赖固定在 `requirements-dev.txt`：PyYAML 与 Pillow 均不进入插件 payload。校验覆盖实际 PNG 解码、被动 SVG XML 解析、包结构与发布回归、源码/生成物一致性及网站测试和构建。0.6.4 release 有 24 个 case，其中 20 个声明了非空的 semantic-review requirements，12 个是 adversarial controls。全部 case 都有 deterministic fixture checks，但这不能自动关闭 semantic review requirements。正向 delegation 无法用 trace ceiling（`max_subagent_events`）断言，因此该 canary 把有界上限与要求提供真实 dispatch 与 integration 证据的 review requirements 配对；trivial、explicit-solo 与 capability-unavailable 三个 canary 继续保持 `max_subagent_events: 0`。已检查的 Field Lab 0.2 baseline source `d9f717a` 缺少所需 public input；Field Lab main `b87b14b` 已提供 `fieldlab review --requirement-outcomes`，并通过该 CLI 证明当时的 9 个 human-required cases 可被 Servotab 的 synthetic producer-consumer contract check 接受。`delegate-bounded-investigation` 的第一次 live attempt 虽获得三条 semantic support，却因重复的 fixed-label assertions 被拒；移除这些 literal checks、保留原 semantic review boundary 后，第二次独立预算的 attempt 通过 deterministic verification，新 reviewer 也支持全部三条 requirement，Servotab acceptance 返回 `accepted`。该证据只覆盖这一个 pinned workspace-scoped case；0.6.4 的 discussion-intake 与 diagnostic cases 尚无 live target-model acceptance receipt，release 本身也不等于 install 或 activate。任何后续 live eval 仍需新的计划和显式 invocation budget；Field Lab 不会自动 retry。

## Feedback

- [Behavior feedback](https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml)：activation、routing、完整 outcome、debug/review/verification 质量或无意义 overhead；
- [Plugin package bug](https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml)：marketplace discovery、manifest validation、install/update、activation 或 package assets。
- [Security policy](SECURITY.md)：无法安全放进 public issue 的 vulnerability 或 trust-boundary failure，使用其中的 private reporting route。

GitHub Issues 是公开的。请删掉 credentials、tokens、private source、聊天、个人数据、account details、local absolute paths 与无关 trace；保留最小可复现 evidence。

## 相关项目

- [MCP Boundary](https://indeliblevivi.github.io/mcp-boundary/zh/) — 面向 MCP server 与 app 的工程 skill、Guide 和可执行 Lab，用于设计、审查与验证。
- [Worker Routing](https://indeliblevivi.github.io/codex-worker-routing/zh/) — 将有明确边界的完整责任交给 native 或可选 ACP worker，并通过本地 Dispatch 面板查看工作记录。

## Companion boundaries

Repository licensing selection 不属于 Servotab router。需要具体 license 选择、audit 或 forward-only transition 时，使用独立维护的 [`IndelibleVivi/license-boundary`](https://github.com/IndelibleVivi/license-boundary)。Servotab 不 bundle、安装、替换或更新它。

Field Lab 同样是 standalone companion：Servotab 拥有自己的 subject cases，但不拥有或管理通用 evaluator runtime。

## Lineage、authorship 与 licensing

Servotab 从历史 Softpowers codebase 迁移而来，保留原有 Git history、release records 和 provenance；rename 不会把旧版本改写成新的历史。项目是独立重写，理念上受 Jesse Vincent / obra 的 [`superpowers`](https://github.com/obra/superpowers) 启发，也参考过 Worker Lanes、Better Harness 及其他明确登记的外部 mechanisms。具体 attribution 和不采用的 machinery 见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)、[docs/external-patterns.md](docs/external-patterns.md) 与 [docs/pattern-intake.md](docs/pattern-intake.md)。

Created by Faye & Cove. Published and maintained by Yifei Fang ([@IndelibleVivi](https://github.com/IndelibleVivi))；她只对自己控制的 project-original material 作为 legal licensor，external contributors 与 third-party rights 仍归相应 rights holders。

从 `0.3.0-rc1` 起，project-original functional materials 与 original documentation 使用分层 terms。这是 source-available / fair-code distribution，不是 OSI open source。逐路径 terms、历史 MIT boundary 与第三方例外分别见 [LICENSING.md](LICENSING.md)、[LICENSE-HISTORY.md](LICENSE-HISTORY.md) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。Repository、website 或 package metadata 不会为未明确覆盖的 assets 或 third-party material 创造额外 public grant。
