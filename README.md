# Softpowers for Codex

[![Validate](https://github.com/IndelibleVivi/softpowers/actions/workflows/validate.yml/badge.svg)](https://github.com/IndelibleVivi/softpowers/actions/workflows/validate.yml)
[![License: layered](https://img.shields.io/badge/license-SUL--1.0%20%2B%20CC%20BY--NC--SA%204.0-blue.svg)](LICENSING.md)

一个 community-maintained、非 OpenAI 官方的 Codex 工程 workflow pack：让方法跟着任务走，保留真正需要的设计、调试、测试、review 与 verification，同时避免把每个小改动都拖进固定仪式。

> Quiet, proportionate engineering workflows for Codex.

当前版本：`0.3.0-rc3`（public release candidate）

## 先看结论

- 日常只需要正常描述任务，不必背 skill 名称。
- Invocation metadata 允许 `softpowers` router 与窄域 specialist
  `license-boundary` 被 implicit invocation；其余 13 个 `soft-*` leaf skills
  都是 explicit-only shortcuts，不会自己抢活。
- 安装完整 pack 不等于每个 skill 都会频繁运行。`spec-chain`、`worktree`、`parallel` 等本来就是特定情境工具，低频是设计的一部分。
- 清晰、局部、可逆的小任务直接做；复杂任务才按需读取一份 playbook。
- Softpowers 不覆盖你的 prompt、`AGENTS.md`、repo 规则、权限边界或 Git 决策。

如果你愿意试用，最有价值的不是一句“好用”，而是告诉我们：它有没有在该出现时出现、有没有绕路、有没有漏掉完整 outcome。见 [反馈](#反馈)。

## 快速安装

需要：Git、Bash、Python 3.10+，以及支持 local skills 的 Codex desktop app、CLI 或 IDE extension。

```bash
git clone https://github.com/IndelibleVivi/softpowers.git
cd softpowers
./install.sh
```

安装后在 Codex 运行：

```text
/skills
```

你应当看到：

- `softpowers`：具备 implicit-invocation eligibility 的工程 router；
- `license-boundary`：只处理 concrete repository licensing decisions
  的 standalone implicit specialist；
- 13 个 `soft-*` skills：explicit-only；
- 如果列表没有刷新，重启 Codex。

这是 source-distributed release candidate，还不是 plugin-directory 安装包。安装脚本只使用 Python 标准库，不会联网下载 dependency。

### 只安装 licensing skill

不想安装 Softpowers pack 的用户，可以直接从 canonical standalone repo
安装这个 self-contained skill：

```text
Use $skill-installer to install skills/license-boundary from
IndelibleVivi/license-boundary at v0.1.0-rc2.
```

它不依赖 `softpowers` router 或其他 leaf skills。安装后，用户可以直接说
“这个项目该选什么 license”“我不想别人拿去收费托管”“准备公开这个 fork，
哪些内容能换证”，不需要先知道 skill 名称。Skill 会先用实际使用后果给出
一个 best-fit recommendation，只保留真正影响选择的 alternatives；exact
license 与适用 scope 仍由用户确认。

Standalone [`IndelibleVivi/license-boundary`](https://github.com/IndelibleVivi/license-boundary)
是 authoring authority。Softpowers 只携带 `v0.1.0-rc2` 的 exact pinned
projection，包括完整的 packaged SUL terms 与 project notice，并通过
`sources/license-boundary.json` 离线验证 source commit、path、size 与
digest；pack build 不在网络上临时拉取 skill。

当前 CI 覆盖 Ubuntu 的 Python 3.10 / 3.13 与 macOS 的 Python 3.13；native Windows 尚未验证。Invocation metadata、packaging 与 filesystem transaction 可以确定性校验，但真实 implicit routing 仍可能随 Codex client、model、prompt 与 repo context 变化。这正是 RC 想收集 behavior feedback 的部分。

### 更新

回到 clone 的 repo：

```bash
git pull --ff-only
./install.sh
```

当前 installer 每次运行都会形成一个可回滚层，即使 payload 没有变化。只在 `git pull --ff-only` 实际拿到新 pack 后重新安装，不要把无变化 reinstall 当成日常检查；也不要直接热改已安装副本。

### 卸载或回滚一层

```bash
./uninstall.sh
```

卸载器会恢复安装前被替换的同名 skills；如果你手改过已安装副本，它会先把修改保存到 snapshot，而不是静默删除。

## 怎么用

日常直接说任务：

```text
修复移动端输入时消息气泡上移的问题，找到根因后直接实现并验证。
```

设计上，router 会把它识别为 debug 工作并按需读取 `debug.md`。你不需要先写 `$soft-debug`，也不需要指定所谓 Quick / Deliberate / Deep mode；如果实际 routing 不符合这个 expectation，请提交 behavior feedback。

明确 feature request 默认仍是完整的 requested usable outcome：

```text
按照这份产品说明实现批量导入，保留多文件、失败重试、进度和历史记录，并跑相关测试。
```

“简单”限制实现复杂度，不会把已经明确的需求偷换成 MVP、scaffold、placeholder 或只有 happy path 的局部 tranche。

当你想强制某个方法时，再显式点名：

```text
$soft-review 审查当前 dirty diff，只报告可操作的 P0–P2 findings。
```

```text
$soft-tdd 为这个 stale cursor bug 建立严格 red-green 回归证据。
```

```text
$soft-spec-chain 依据这份 approved spec 建立完整 implementation plan；当前 tranche 不得替代完整 scope。
```

```text
$license-boundary 按这个 repo 的实际复用目标和 rights lineage 选择并落实 license。
```

## 不是每个 skill 都要经常用

这 15 个 skills 不是一排等权按钮。更准确的理解是五层：

| 层 | Skills | 什么时候需要关心 |
|---|---|---|
| 默认入口 | `softpowers` | 日常 repo work；通常只说自然语言 |
| 独立 specialist | `license-boundary` | 选择、添加、审计或迁移 repo license；可单独安装并用自然语言触发 |
| 精确控制 | `soft-debug`, `soft-review`, `soft-verify`, `soft-execute`, `soft-tdd` | 你明确想固定 diagnosis、review、verification、execution 或 red-green 方法时 |
| 特定情境 | `soft-brainstorm`, `soft-plan`, `soft-receive-review`, `soft-finish`, `soft-spec-chain`, `soft-worktree`, `soft-parallel` | 开放设计、多步 handoff、外部 review、大型 approved spec、隔离 workspace 或 bounded delegation 真正有价值时 |
| Maintainer evidence | `soft-eval` | 明确要跑 behavior canary、release evidence 或调查 routing/workflow behavior 时 |

完整 pack 保留这些 leaf skills，是为了让显式控制、eval 和少见但高价值的工程情境都有稳定入口。13 个 `soft-*` leaf 全部是 explicit-only；`license-boundary` 只在 concrete licensing need 上具备 implicit eligibility。没有必要为了“都装了”而刻意调用任何 skill。

当前 installer 仍按一个事务安装完整 pack。`license-boundary` 另有直接 repo-path 安装方式，因此不需要为了这一项扩大 pack installer 的 selective-profile、rollback 与 uninstall 状态空间。

## Softpowers 的行为原则

`v0.2` 的核心是：

> implicit discovery, non-mandatory execution

- Router 负责 routing，但不宣布自己被激活，也不向用户表演内部分类。
- 小任务读取 0 个 reference，直接实现并做 focused verification。
- Bug、review、迁移等任务先读 0–1 个 primary reference；只有阶段真实变化或新证据出现时才读取下一份。
- 没有当前用途的 fallback、state、hash、重复检查和第二轮 acceptance 不进入默认路径。
- 产品介绍、tutorial、截图、示例、log 与 review 按用户 intent 和 source authority 使用，而不是各造一个 workflow。
- Outcome、hard constraints 与 proposed mechanism 分开理解；除非用户明确锁定 mechanism，否则先用 repo/runtime evidence、当前 platform capabilities 与 authoritative sources 挑战其假设，再选择满足完整 outcome 的最短 supported path。
- 跨 owner、transport 或 persistent-state 的 patch cascade 会触发 architecture reset；局部 patch 通过和 sunk cost 都不能替选中的 topology 背书。
- 严格 red-green 优先用于 bug、领域规则、状态机、parser、契约、迁移、并发和安全敏感行为；样式、copy 和简单 wiring 不强制低价值 unit test。
- Review 默认一轮，不制造 findings，也不自动创建重复 reviewer loops。
- Verification 按 blast radius 选择 focused / adjacent / broad evidence。
- 配置存在、当前路径被 exercise、同 task repair 与 later comparable improvement 是不同强度的 claims；这条边界不要求 score、ledger、后台审计或额外 reviewer。
- Worktree、design doc、commit、push、PR、merge 与 destructive cleanup 都不会仅仅因为某个方法存在而自动发生。

`soft-parallel` 采用 bounded Worker Lanes contract：Requester / Coordinator / Task Worker / optional Helper。每个 worker 收到紧凑的 `Outcome / Scope / Context / Authority / Return`，主线程保留用户沟通、权限边界、整合与最终判断。

## 可执行 behavior eval

`0.3.0-rc2` 新增 explicit-only `soft-eval`。它把现有 behavior principles 变成一条可运行、可恢复、可检查的 maintainer evidence lane，但不会让普通 repo task 自动花 model quota。

Source checkout 中先跑不调用 model 的 gate：

```bash
python3 -S evals/run_behavior_evals.py list
python3 -S evals/run_behavior_evals.py selftest
```

当前 bundled canaries 是：

- `tiny-copy`：小 copy change，限制 plan、subagent 与 command overhead；
- `stale-cursor`：修复 consistency invariant 并执行 regression test；
- `spec-chain`：把 approved spec 完整转换为 implementation plan，不能用局部 tranche 冒充 full scope。

只有明确需要 live evidence 时才运行 Codex：

```bash
python3 -S evals/run_behavior_evals.py run \
  --case tiny-copy \
  --subject-id current-cli-environment \
  --model <exact-model-id>
```

每次 attempt 把 prompt、case contract、raw JSONL、stderr、final message、Git diff、metadata 和 deterministic verification 原子写入 `.softpowers-evals/runs/`。使用同一个 `--run-id` 加 `--resume` 可以从未完成的 case boundary 恢复；只有 case/prompt/fixture digests、runner identity、resolved Codex executable/version、model、timeout 与 workspace-retention setting 全部仍一致时，已完成 attempt 才会被复用。

Subject identity 必须如实描述当前 CLI 实际加载的 skills。Codex 会同时发现同名 repo-level 与 user-level skill，因此存在 identity collision 时，不要声称 candidate 被单独隔离。Runner 的第一版支持 matched prompt/fixture/model/sandbox/repeat 和明确 `subject-id`，但不把未经隔离的两次运行包装成可信 A/B。

## 运行时结构

```text
softpowers/
├── SKILL.md                   # implicit engineering router
├── agents/openai.yaml
└── references/
    ├── brainstorm.md
    ├── spec-chain.md
    ├── plan.md
    ├── execute.md
    ├── debug.md
    ├── tdd.md
    ├── review.md
    ├── receive-review.md
    ├── verify.md
    ├── eval.md
    ├── worktree.md
    ├── parallel.md
    └── finish.md

license-boundary/              # self-contained implicit specialist
├── SKILL.md
└── agents/openai.yaml

soft-debug/                    # explicit shortcut
soft-review/                   # explicit shortcut
soft-eval/                     # explicit eval method + bundled runner/cases/schemas
...                            # 共 13 个 explicit `soft-*` leaf skills
```

正常路径：

```text
用户描述任务
  → softpowers 隐式匹配
  → 小任务直接处理，读取 0 references
  → 专门任务按需读取一份 playbook
  → 后续只有阶段真实变化才读取下一份
```

Router 不尝试“调用”另一个 skill。`references/` 是它自己的 progressive-disclosure 资源，因此没有悬空的 skill-to-skill dependency。

## 安装与恢复细节

安装目标按这个顺序解析：

1. `--dest /path/to/skills`
2. `SOFTPOWERS_SKILLS_DIR`（兼容 `AGENTS_SKILLS_DIR`）
3. `${CODEX_HOME}/skills`
4. 若 `~/.agents/skills` 或 legacy `~/.codex/skills` 中已有 Softpowers，在原位置升级
5. Softpowers 对全新安装默认选择 Codex USER skill root：`~/.agents/skills`
6. 若只有 legacy `~/.codex/skills` 已存在，则继续使用它

如果两个 root 都已经存在 Softpowers，安装器会拒绝猜测并要求显式 `--dest`。当前 USER skill root 与其他 scope 见 [OpenAI Codex skill documentation](https://developers.openai.com/codex/build-skills#where-codex-loads-local-skills)。

安装器会：

1. 校验 `PACK_MANIFEST.json` 中 15 个 skills、13 个 router references、文件大小与 SHA-256；
2. 在目标 root 内 staging 并再次校验；
3. 只替换 Softpowers 的 15 个目录，保留其他 skills；
4. 备份同名旧 skill；
5. 中途失败时 rollback；
6. 写入 install manifest 与 current pointer；
7. 记录每个安装目录 digest，供安全卸载。

从 `v0.1.x` 升级时，直接运行当前 `./install.sh` 即可。第一次运行 v0.2 的 `./uninstall.sh` 会恢复升级前的 legacy skills 与 manifest pointer；若还要继续删除恢复出的 v0.1.x layer，请 checkout 对应 v0.1.x source 并使用当时的 uninstaller。当前 v0.2 uninstaller 会拒绝把 12-skill legacy manifest 当成 13-skill v0.2 manifest。Current-schema manifest stack 要求 LIFO，不会跳层删除。

## 反馈

Softpowers 还是 RC。我们尤其想知道真实任务中的 activation、完整性与 overhead，而不是只收抽象 feature wish。

- [提交 behavior feedback](https://github.com/IndelibleVivi/softpowers/issues/new?template=behavior-feedback.yml)：该不该触发、route 对不对、有没有绕圈或漏 outcome。
- [报告 install / uninstall bug](https://github.com/IndelibleVivi/softpowers/issues/new?template=installer-bug.yml)：目标目录、rollback、manifest 或跨平台问题。
- 想直接改代码或方法：先读 [CONTRIBUTING.md](CONTRIBUTING.md)。

一份高质量 feedback 最好包含：

- Softpowers version 或 commit；
- Codex surface（desktop / CLI / IDE）与基本环境；
- 已脱敏的原始 prompt；
- 你期望发生什么、实际发生什么；
- 是否触发、读取了哪些 reference（如果看得到）；
- 最终 outcome 是否完整，以及有没有多余 plan、test、hash、tool call 或 subagent。

请先删掉 repo secrets、tokens、私有路径、聊天、账号信息与不能公开的 source/output。Issue 是公开的。

## Maintainer workflow

14 份方法正文只维护一份：

```text
methods/*.md
```

发布脚本从这些 canonical sources 同时生成：

- `skills/softpowers/references/*.md`（13 个工程 router references）
- 14 个 standalone leaf `SKILL.md`，包括可独立安装的 `license-boundary`

Eval runner、schemas 与 cases 的 canonical sources 在 `evals/`；同一生成步骤把它们投影进 `skills/soft-eval/`，供安装后的 skill 直接使用。

不要直接修改 generated skill copies。

普通用户可运行标准库 self-test：

```bash
python3 scripts/selftest.py
```

Maintainer release gate 需要 PyYAML：

```bash
python3 -m pip install PyYAML
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
python3 scripts/validate.py --exact skills
python3 scripts/generate_pack_manifest.py --check
python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py evals/*.py
bash -n install.sh uninstall.sh
```

修改 `methods/` 后先 regenerate：

```bash
python3 scripts/build_skills.py
python3 scripts/validate.py --exact skills
python3 scripts/generate_pack_manifest.py
python3 scripts/selftest.py
```

Behavioral probes 与 eval seed set 见 [BEHAVIORAL_PROBES.md](BEHAVIORAL_PROBES.md) 和 [evals/activation-prompts.csv](evals/activation-prompts.csv)。不要为了通过 eval 把 router 扩成无边界的万能匹配器。

`scripts/audit_public_tree.py` 会 fail closed，并检查 tracked/candidate public files 中的 private namespaces、symlink、personal absolute paths、常见 secret patterns、environment files 与 macOS junk。它证明的是当前 public tree，不会把 Git history 描述成从未含过任何 local material；release 仍应从 clean tagged checkout 构建。

## 设计来源、创作与 license

Softpowers 是独立重写，理念上受 Jesse Vincent / obra 的 [`superpowers`](https://github.com/obra/superpowers) 启发，但没有复制其强制 bootstrap、固定完整流水线或逐 task 双 review 机制。Worker Lanes contract 参考了 Luluane 与 Astrean-Codex 的 [`astrean-worker-lanes`](https://github.com/LuluaneS/astrean-worker-lanes)。`rc5` 还把 QoderAI [`better-harness`](https://github.com/QoderAI/better-harness) 的 evidence-state distinction 当作批判性参考，但不安装、调用、依赖或吸收其 audit workflow、scores、agents、reports 与 repair ledger。

具体 attribution 与第三方边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

Created by Faye & Cove. Faye
([@IndelibleVivi](https://github.com/IndelibleVivi)) maintains the project and
is the legal licensor for project-original material she controls. External
contributors license their own contributions under the applicable target-file
license.

从 `0.3.0-rc1` 起，functional materials 使用
[Sustainable Use License v1.0](LICENSE)，原创 documentation 使用
[CC BY-NC-SA 4.0](LICENSE-DOCUMENTATION.md)。这是 source-available /
fair-code 分发，不是 OSI open source。SUL-1.0 允许 internal business use，
但不允许为了收费或商业目的向他人分发或提供 covered functional materials；
required licensing 与 copyright notices 不得移除或遮蔽。

逐路径适用范围与第三方例外见 [LICENSING.md](LICENSING.md)，旧 MIT
版本边界见 [LICENSE-HISTORY.md](LICENSE-HISTORY.md)。
