# Servotab for Codex

[![Validate](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml/badge.svg)](https://github.com/IndelibleVivi/servotab/actions/workflows/validate.yml)
[![License: layered](https://img.shields.io/badge/license-SUL--1.0%20%2B%20CC%20BY--NC--SA%204.0-blue.svg)](LICENSING.md)

Servotab 是一个 independent、community-maintained 的 Codex engineering plugin：清楚的改动保持直接，风险和不确定性升高时才加载更强的方法，最后用 fresh evidence 关闭真实 outcome。

> Method as exponent, not machinery.

当前 source candidate：`0.4.0-rc1`。Public repository 提供 source-checkout installation，但当前 candidate 尚未 tagged 或创建 GitHub Release。Servotab 不是 OpenAI 官方产品，也尚未提交或列入 OpenAI plugin directory；directory submission 与 publication 仍是 owner-controlled release gate。实时的 package、GitHub、website 与 Cloudflare 状态见 [docs/current-state.md](docs/current-state.md)。

## 它做什么

Servotab 保持四个稳定承诺：

- Clear changes stay direct.
- Risk brings stronger method.
- Fresh evidence closes the loop.
- The requested outcome stays whole.

日常 repository work 只需正常描述任务，不必先挑 method。唯一具备 implicit-invocation eligibility 的 router 是 `servotab`；其余 12 个 leaf skills 都是 explicit-only shortcuts。它们不会覆盖你的 prompt、`AGENTS.md`、repo rules、权限边界、Git decision 或 deployment authority。

Servotab 也不会把日志、截图、review、旧计划或 generated artifact 自动当成指令。它们可能是 evidence；当前用户意图、accepted specification 与 canonical source 才决定工作方向。

## 安装（public source checkout）

当前 public route 是 repository marketplace/source checkout：

```bash
git clone https://github.com/IndelibleVivi/servotab.git
cd servotab
codex plugin marketplace add .
codex plugin add servotab@personal
```

`.agents/plugins/marketplace.json` 定义 repo marketplace `personal`，它指向 `plugins/servotab/`。`servotab@personal` 是当前 selector。

这条 plugin-native 路径取代旧版 `install.sh` / root `skills/` global installer。当前 maintainer environment 已从精确 checkout 添加 marketplace `personal`，并把 `servotab@personal` 重新安装为最终 43-file candidate；source/cache exact diff、fresh-process prompt-input 和一条 representative fresh-task behavior smoke 都已通过。Source-checkout install 不是 OpenAI plugin directory install，也不把 candidate 自动变成 tag、GitHub Release 或其他机器上的 acceptance receipt。

如果其他本机仍有 manifest-owned Softpowers `0.3.0-rc5` 或更早 global layer，请先读 [迁移指南](docs/migration-from-softpowers.md) 和 [current state](docs/current-state.md)。当前 maintainer roots 已完成 manifest-driven retirement 并验证为 clear；不要把这条 receipt 当成手动删除其他机器旧目录的许可。

## 怎么用

普通任务直接说：

```text
修复移动端输入时消息气泡上移的问题，找到根因后直接实现并验证。
```

Router 会按任务的真实 pressure 决定保持 direct，还是读取一份相关 reference。它不会宣布内部分类，也不会因为 method 可用就制造 plan、worktree、TDD、subagent 或第二轮 review。

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
| `worktree` | explicit only | 只在 dirty state、风险、时长或并发写入值得时隔离 workspace |
| `delegate` | explicit only | 给少量独立 lanes 明确 ownership、authority 与 return contract |
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
├── .codex-plugin/plugin.json                 plugin manifest
├── LICENSE + NOTICE.md                       package-local rights boundary
├── skills/servotab/                          implicit router + 12 references
├── skills/{design,...,finish}/               12 explicit leaves
└── assets/                                   curated package assets

.agents/plugins/marketplace.json              repo marketplace entry
PACK_MANIFEST.json                            exact derived payload identity
```

`methods/*.md` 是 12 个 method bodies 的唯一 canonical source；`scripts/skill_catalog.py` 是 names、descriptions 与 invocation metadata 的 catalog。`plugins/servotab/skills/**` 是 generated projection，不要直接修改。Root `assets/` 保存项目的 canonical asset files；generator 只把 manifest 需要的 `composer-icon.png` 与 `logo.png` 投影进 plugin package。`logo-transparent.png` 仍是 repository asset，不是当前 plugin payload 或已接受的 dark-mode contract。

以下路径各有不同责任：

- `evals/` 与 `fieldlab-pack.json`：Servotab-owned behavior cases 和 Field Lab schema v2 subject pack；
- `site/`：Astro static website source，独立于 plugin runtime；
- `docs/current-state.md`：易变的 candidate / installed / deployed / live 状态；
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
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
uv run --with PyYAML==6.0.3 python3 scripts/generate_pack_manifest.py --check
uv run --with PyYAML==6.0.3 python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

`scripts/selftest.py` 在 disposable fixtures 中检查 package identity、13-skill topology、source/generated sync、retired IDs、manifest/assets、marketplace route，以及 legacy helper 的 read-only preflight 与显式 one-layer retirement。它不安装 live plugin，也不提交 OpenAI directory。

Website 的独立 build contract 见 [site/README.md](site/README.md)。

## Feedback

- [Behavior feedback](https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml)：activation、routing、完整 outcome、debug/review/verification 质量或无意义 overhead；
- [Plugin package bug](https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml)：marketplace discovery、manifest validation、install/update、activation 或 package assets。

GitHub Issues 是公开的。请删掉 credentials、tokens、private source、聊天、个人数据、account details、local absolute paths 与无关 trace；保留最小可复现 evidence。

## Companion boundaries

Repository licensing selection 不属于 Servotab router。需要具体 license 选择、audit 或 forward-only transition 时，使用独立维护的 [`IndelibleVivi/license-boundary`](https://github.com/IndelibleVivi/license-boundary)。Servotab 不 bundle、安装、替换或更新它。

Field Lab 同样是 standalone companion：Servotab 拥有自己的 subject cases，但不拥有或管理通用 evaluator runtime。

## Lineage、authorship 与 licensing

Servotab 从历史 Softpowers codebase 迁移而来，保留原有 Git history、release records 和 provenance；rename 不会把旧版本改写成新的历史。项目是独立重写，理念上受 Jesse Vincent / obra 的 [`superpowers`](https://github.com/obra/superpowers) 启发，也参考过 Worker Lanes、Better Harness 及其他明确登记的外部 mechanisms。具体 attribution 和不采用的 machinery 见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)、[docs/external-patterns.md](docs/external-patterns.md) 与 [docs/pattern-intake.md](docs/pattern-intake.md)。

Created by Faye & Cove. Faye ([@IndelibleVivi](https://github.com/IndelibleVivi)) maintains the project and is the legal licensor only for project-original material she controls；external contributors 与 third-party rights 仍归相应 rights holders。

从 `0.3.0-rc1` 起，project-original functional materials 与 original documentation 使用分层 terms。这是 source-available / fair-code distribution，不是 OSI open source。逐路径 terms、历史 MIT boundary 与第三方例外分别见 [LICENSING.md](LICENSING.md)、[LICENSE-HISTORY.md](LICENSE-HISTORY.md) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。Repository、website 或 package metadata 不会为未明确覆盖的 assets 或 third-party material 创造额外 public grant。
