# Softpowers for Codex

[![Validate](https://github.com/IndelibleVivi/softpowers/actions/workflows/validate.yml/badge.svg)](https://github.com/IndelibleVivi/softpowers/actions/workflows/validate.yml)
[![License: layered](https://img.shields.io/badge/license-SUL--1.0%20%2B%20CC%20BY--NC--SA%204.0-blue.svg)](LICENSING.md)

一个 community-maintained、非 OpenAI 官方的 Codex 工程 workflow pack：让方法跟着任务走，保留真正需要的设计、调试、测试、review 与 verification，同时避免把每个小改动都拖进固定仪式。

> Quiet, proportionate engineering workflows for Codex.

当前版本：`0.3.0-rc5`（public release candidate）

## 先看结论

- 日常只需要正常描述任务，不必背 skill 名称。
- Invocation metadata 只允许 `softpowers` router 被 implicit invocation；
  其余 12 个 `soft-*` leaf skills 都是 explicit-only shortcuts，不会自己抢活。
- 12 个 leaf 是否在 UI 中显式出现，与 router 是否采用其 method 是两件事；尤其 `soft-parallel` 的自然语言路径由 implicit router 读取 reference，不能从一次 harness spawn 或 Ultra model tier 反推 leaf activation。
- 清晰、局部、可逆的小任务直接做；复杂任务才按需读取一份 playbook。
- 当工作可能改变 product meaning、programme order、trust boundaries 或 shared infrastructure 时，Softpowers 会区分 applicable authority 与 derived artifacts；agent 写出的 spec、PR、代码和绿色 CI 不能自我授权。
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
- 12 个 `soft-*` skills：explicit-only；
- 如果列表没有刷新，重启 Codex。

这是 source-distributed release candidate，还不是 plugin-directory 安装包。安装脚本只使用 Python 标准库，不会联网下载 dependency。

### Recommended companion：License Boundary

Repository license selection、audit、addition 和 forward-only relicensing
明确不属于 Softpowers router。需要这类能力时，从它自己的 standalone repo
独立安装 License Boundary：

```text
Use $skill-installer to install skills/license-boundary from
IndelibleVivi/license-boundary at v0.1.0-rc3.
```

它不依赖 `softpowers` router 或其他 leaf skills。安装后，用户可以直接说
“这个项目该选什么 license”“我不想别人拿去收费托管”“准备公开这个 fork，
哪些内容能换证”，不需要先知道 skill 名称。Skill 会先用实际使用后果给出
一个 best-fit recommendation，只保留真正影响选择的 alternatives；exact
license 与适用 scope 仍由用户确认。

Standalone [`IndelibleVivi/license-boundary`](https://github.com/IndelibleVivi/license-boundary)
同时是 authoring authority 和唯一 distribution authority。Softpowers
`v0.3.0-rc5` 与 License Boundary `v0.1.0-rc3` 已做兼容验证，但只推荐它，
不再 bundle、安装、替换、降级或更新 `license-boundary` 的 installed bytes。

当前 CI 覆盖 Ubuntu 的 Python 3.10 / 3.13 与 macOS 的 Python 3.13；native Windows 尚未验证。Invocation metadata、packaging 与 filesystem transaction 可以确定性校验，但真实 implicit routing 仍可能随 Codex client、model、prompt 与 repo context 变化。这正是 RC 想收集 behavior feedback 的部分。

### 更新

回到 clone 的 repo：

```bash
git pull --ff-only
./install.sh
```

如果 active historical layer 仍管理当前 release 已退休的目录——例如旧版
`license-boundary` 或 `soft-eval`——新的 installer 会在任何 mutation 前停止并
给出迁移提示。用当前 release 的 uninstaller 按 LIFO 退掉该旧层；若下一层仍
管理同一 retired skill 就重复一次，然后再安装：

```bash
./uninstall.sh
./install.sh
```

旧层记录的 pre-install `license-boundary` 会被恢复；manifest-owned `soft-eval`
会随旧层安全退出。Softpowers 不会接管 standalone License Boundary、Field Lab
CLI、`pattern-intake` 或 `skill-eval`。需要安装或升级 companion 时，始终使用
各自独立的 distribution surface。

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

## 不是每个 skill 都要经常用

这 13 个 skills 不是一排等权按钮。更准确的理解是三层：

| 层 | Skills | 什么时候需要关心 |
|---|---|---|
| 默认入口 | `softpowers` | 日常 repo work；通常只说自然语言 |
| 精确控制 | `soft-debug`, `soft-review`, `soft-verify`, `soft-execute`, `soft-tdd` | 你明确想固定 diagnosis、review、verification、execution 或 red-green 方法时 |
| 特定情境 | `soft-brainstorm`, `soft-plan`, `soft-receive-review`, `soft-finish`, `soft-spec-chain`, `soft-worktree`, `soft-parallel` | 开放设计、多步 handoff、外部 review、大型 approved spec、隔离 workspace 或 bounded delegation 真正有价值时 |

完整 pack 保留这些 leaf skills，是为了让显式控制和少见但高价值的工程情境都有稳定入口。12 个 `soft-*` leaf 全部是 explicit-only；普通自然语言任务由 `softpowers` router 选择并读取相应 reference，不会再产生一次可见的 leaf invocation。没有必要为了“都装了”而刻意调用任何 skill。License Boundary 与 Skill Field Lab 都是 standalone companions，不计入这 13 个目录，也不由 Softpowers transaction 管理。

## Softpowers 的行为原则

`v0.2` 的核心是：

> implicit discovery, non-mandatory execution

- Router 负责 routing，但不宣布自己被激活，也不向用户表演内部分类。
- Host/runtime 决定 subagent tools 与 concurrency 是否存在；Softpowers 只根据 task topology 决定何时值得使用以及怎样约束 lanes。Ultra、空闲 slots 或 harness 自发 dispatch 本身都不是 parallel routing evidence。
- 小任务读取 0 个 reference，直接实现并做 focused verification。
- Bug、review、迁移等任务先读 0–1 个 primary reference；只有阶段真实变化或新证据出现时才读取下一份。
- 没有当前用途的 fallback、state、hash、重复检查和第二轮 acceptance 不进入默认路径。
- 产品介绍、tutorial、截图、示例、log 与 review 按用户 intent 和 source authority 使用，而不是各造一个 workflow。
- Outcome、hard constraints 与 proposed mechanism 分开理解；除非用户明确锁定 mechanism，否则先用 repo/runtime evidence、当前 platform capabilities 与 authoritative sources 挑战其假设，再选择满足完整 outcome 的最短 supported path。
- 跨 owner、transport 或 persistent-state 的 patch cascade 会触发 architecture reset；局部 patch 通过和 sunk cost 都不能替选中的 topology 背书。
- material boundary 没有 cheap reliable reproducer 时，把缺失 seam 当作 testability problem，建立或交接最小 local surrogate / diagnostic；named host 仍是最终 acceptance，不复制 production 或扩建通用 testing programme。
- 严格 red-green 优先用于 bug、领域规则、状态机、parser、契约、迁移、并发和安全敏感行为；样式、copy 和简单 wiring 不强制低价值 unit test。
- Review 默认一轮，不制造 findings，也不自动创建重复 reviewer loops。
- Verification 按 blast radius 选择 focused / adjacent / broad evidence。
- 配置存在、当前路径被 exercise、同 task repair 与 later comparable improvement 是不同强度的 claims；这条边界不要求 score、ledger、后台审计或额外 reviewer。
- Worktree、design doc、commit、push、PR、merge 与 destructive cleanup 都不会仅仅因为某个方法存在而自动发生。

当任务出现至少两个 independent substantial lanes，或一个 noisy/long-running lane 能实质保护 coordinator attention 时，router 会在 first dispatch 前把 delegation 视为 phase change 并读取 `parallel.md`。`soft-parallel` 采用 bounded Worker Lanes contract：Requester / Coordinator / Task Worker / optional Helper。每个 worker 收到紧凑的 `Outcome / Scope / Context / Authority / Return`，主线程保留用户沟通、权限边界、整合与最终判断。若当前 host 或指令不允许 delegation，就保留相同 ownership boundary 并顺序执行，不声称发生了 parallel execution。

## Optional maintainer field lab

Softpowers 仍拥有 `tiny-copy`、`stale-cursor`、`spec-chain`、`owner-controlled-migration`、`programme-reorder-review`、`adopted-foundation-review`、`repeated-review-scope-accretion`、`missing-host-test-seam` 八个 canaries；后两项分别约束 repeated review 的 tranche scope 与缺失 host seam 的 bounded testability escalation。
但从 `0.3.0-rc5` 起不再 bundle 通用 runner、schemas 或 explicit `soft-eval`
skill。可执行 evidence machinery 已迁移到独立维护的 Skill Field Lab；它不是
Softpowers runtime dependency，也不会由 Softpowers installer 管理。

安装了 `fieldlab` CLI 的 maintainer 可以从 source checkout 运行 no-spend gate：

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest-pack fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

这三条命令不会启动 target model。任何 synthetic live attempt 都需要单独保存
plan，并显式提供 `run --live --max-invocations N`；Softpowers 不把 live model eval
设为普通 release gate。完整 authority split 与 evidence 边界见
[evals/README.md](evals/README.md)。

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
    ├── worktree.md
    ├── parallel.md
    └── finish.md

soft-debug/                    # explicit shortcut
soft-review/                   # explicit shortcut
...                            # 共 12 个 explicit `soft-*` leaf skills
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

1. 校验 `PACK_MANIFEST.json` 中 13 个 skills、12 个 router references、文件大小与 SHA-256；
2. 在目标 root 内 staging 并再次校验；
3. 只替换 Softpowers 的 13 个目录，保留其他 skills；
4. 备份同名旧 skill；
5. 中途失败时 rollback；
6. 写入 install manifest 与 current pointer；
7. 记录每个安装目录 digest，供安全卸载。

当前 uninstaller 依据每层 manifest 自己记录的 entries 做 path、backup、digest 与 duplicate 校验，因此可以安全恢复旧 12/13/14/15-skill layers，不要求历史集合等于当前 catalog。Manifest stack 仍严格要求 LIFO，不会跳层删除。新 installer 若发现 active historical layer 仍管理当前 release 已退休的 skill，会在 staging 前拒绝；先用当前 uninstaller 退掉该层，必要时重复，再安装新 pack。

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

12 份方法正文只维护一份：

```text
methods/*.md
```

发布脚本从这些 canonical sources 同时生成：

- `skills/softpowers/references/*.md`（12 个工程 router references）
- 12 个 standalone `soft-*` leaf `SKILL.md`

`evals/cases/`、activation seeds 与 project-specific evidence records 由 Softpowers
维护；通用 evaluator/runner 属于 optional standalone Field Lab，不进入 generated
skills 或 install payload。

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
python3 -m py_compile scripts/*.py
bash -n install.sh uninstall.sh
```

若本机另行安装了 Field Lab，再加跑：

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest-pack fieldlab-pack.json
fieldlab list fieldlab-pack.json
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
