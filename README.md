# Softpowers Pack

给 Codex 使用的风险分级工程 skills。它保留 Superpowers 中真正有价值的骨架：设计收敛、计划、证据驱动调试、TDD、代码审阅、验证、worktree、并行代理和分支收口；同时让方法服务于任务，而不把每次改动拖进固定仪式。

当前版本：`0.2.0-rc1`

## v0.2 的核心变化

v0.1.x 把 12 个 skills 全部锁为 explicit-only。安装很安全，但用户必须记住并手动输入 `$soft-debug`、`$soft-review` 等名称；`$softpowers` 也无法真正加载其他锁住的 skills。

v0.2 改成：

> implicit discovery, non-mandatory execution

- 只有 `softpowers` router 设置为 `allow_implicit_invocation: true`。
- 11 个 leaf skills 继续 `allow_implicit_invocation: false`，作为显式快捷入口。
- Router 内部拥有 11 份 `references/*.md` playbooks，并按任务阶段读取。
- 清晰、局部、可逆的小任务读取 **0 个 reference**，直接实现并做 focused verification。
- Bug、review、迁移等任务先读 0–1 个 primary reference；只有阶段真实变化或新证据出现时才加载下一份。
- Router 不宣布自己被激活，也不向用户表演 Quick / Deliberate / Deep 分类。
- 用户说正常语言即可。routing 是 Codex 的责任。

## 运行时结构

```text
softpowers/
├── SKILL.md                   # 唯一 implicit router，约 550 words
├── agents/openai.yaml
└── references/
    ├── brainstorm.md
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
...                            # 共 11 个 leaf skills
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

## 方法与门槛

| 方法 | 进入条件 |
|---|---|
| Brainstorm | 产品、交互或架构仍有真正影响实现的开放决策 |
| Plan | 需求已大致确定，工作需要多步排序或跨 session handoff |
| Execute | 已有计划，或需求明确但需要多个 coherent slices |
| Debug | Bug、失败测试、回归、构建失败、异常行为或性能退化 |
| TDD | 失败测试能澄清行为契约或防止高价值回归 |
| Review | 审 diff、commit、branch、PR 或实现结果 |
| Receive Review | 外部 review 意见需要核实、接受、调整、拒绝或延期 |
| Verify | 需要证明 bug 已修、要求已满足、测试通过或 branch ready |
| Worktree | dirty state、风险、时长或并行写入让隔离真正有价值 |
| Parallel | 至少两个有分量、上下文有界、无关键顺序依赖的独立工作域 |
| Finish | commit、push、PR、merge、branch/worktree cleanup 或最终集成决策 |

硬门槛仍然存在：

- 严格 red-green 优先用于 bug、领域规则、状态机、parser、契约、迁移、并发和安全敏感行为。
- 样式、copy、简单 wiring、配置和生成物不强制低价值 unit test。
- Subagent 默认最多 3 个，无嵌套；主线程始终负责整合和验证。
- Review 默认一轮，不制造 findings，不自动创建 spec reviewer + quality reviewer 双循环。
- Verification 按 focused / adjacent / broad 分级。
- worktree、design doc、commit、push、PR、merge 和 destructive cleanup 都不会因方法论自动发生；user request 与适用的 repository/global instructions 仍优先。

## Canonical source

11 份方法正文只维护一份：

```text
methods/*.md
```

发布脚本从这些文件同时生成：

- `skills/softpowers/references/*.md`
- 11 个 standalone leaf `SKILL.md`

因此 router references 与 `$soft-debug` 等显式入口不会逐渐漂移。

```bash
python3 scripts/build_skills.py
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
```

## 安装

用户安装只需要 Python 3 标准库，不需要 PyYAML，也不会联网安装依赖。

解压后：

```bash
cd softpowers-pack-v0.2.0-rc1
./install.sh
```

目标目录解析顺序：

1. `--dest /path/to/skills`
2. `SOFTPOWERS_SKILLS_DIR`（兼容 `AGENTS_SKILLS_DIR`）
3. `${CODEX_HOME}/skills`
4. 若 `~/.agents/skills` 或 `~/.codex/skills` 中已有 Softpowers，原地升级该安装
5. 新安装默认使用当前官方 user skill root：`~/.agents/skills`
6. 若只有 legacy `~/.codex/skills` 已存在，则继续使用它

如果两个 root 都存在 Softpowers，安装器会拒绝猜测并要求显式 `--dest`。

### 从 v0.1.2 升级

直接运行 v0.2 安装器即可。它会识别现有 v0.1.x root，在同一位置事务升级：

- v0.1.2 的 12 个目录会进入 timestamped backup；
- v0.2 成为新的 manifest stack 顶层；
- 运行一次 v0.2 的 `./uninstall.sh` 会完整恢复 v0.1.2 和旧 pointer；
- 再运行一次旧层卸载，才会移除 v0.1.2。

不要直接热改已安装副本。安装文件有 manifest digests；用新 release 覆盖，回滚路径才完整。

### 安装安全行为

安装器会：

1. 用标准库读取 `PACK_MANIFEST.json`；
2. 校验 12 个 skills、11 个 router references、文件大小和 SHA-256；
3. 在目标 root 内 staging 并再次校验；
4. 只替换 Softpowers 的 12 个目录，允许其他 skills 共存；
5. 备份同名旧 skill；
6. 中途失败时 rollback；
7. 成功后写 install manifest 和 current pointer；
8. 记录每个安装目录 digest，供安全卸载。

安装后运行：

```text
/skills
```

`softpowers` 应为 implicit；11 个 leaf skills 可见但 explicit-only。客户端未刷新时重启 Codex。

## 使用

日常无需记技能名：

```text
修复移动端输入时消息气泡上移的问题，找到根因后直接实现并验证。
```

Router 应自行读取 `debug.md`；猫猫无需写 `$soft-debug`。

显式入口仍可用于测试、强制方法或精确控制：

```text
$soft-review 审查当前 dirty diff，只报告可操作的 P0–P2 findings。
```

```text
$soft-tdd 为这个 stale cursor bug 建立严格 red-green 回归证据。
```

```text
$soft-parallel 只读调查三个确定互不相关的测试组，主线程负责整合。
```

## 卸载与恢复

```bash
./uninstall.sh
```

卸载器会：

- 删除当前安装层；
- 恢复该层安装前的同名 skills；
- 不触碰无关 skills；
- 将安装后被手改的 skill 保存到 `.softpowers-uninstall-snapshots/`；
- 仅允许 LIFO 卸载，旧 manifest 请求会在 mutation 前拒绝。

也可显式指定：

```bash
./uninstall.sh --dest /path/to/skills
./uninstall.sh --manifest /path/to/current-manifest.json
```

## 校验

普通用户可直接运行：

```bash
python3 scripts/selftest.py
```

覆盖：

- router-only implicit activation metadata；
- methods → references / leaves 同步；
- 35 个安装 payload 文件的 size 与 digest；
- 无 site-packages 的安装/卸载；
- 新 `~/.agents/skills` root 与 legacy `~/.codex/skills` 原地升级；
- 无关 skills 共存；
- backup/restore、manifest stack、non-LIFO rejection；
- 用户修改保全；
- partial install rollback。

Maintainer release gate 需要 PyYAML：

```bash
python3 -m pip install PyYAML
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
python3 scripts/validate.py --exact skills
python3 scripts/generate_pack_manifest.py --check
python3 scripts/selftest.py
```

修改 `methods/` 后：

```bash
python3 scripts/build_skills.py
python3 scripts/validate.py --exact skills
python3 scripts/generate_pack_manifest.py
python3 scripts/selftest.py
```

## RC 观察重点

`0.2.0-rc1` 主要验证 activation 与 progressive disclosure。真实任务里观察：

- 该触发时是否触发；
- 解释概念、简单找文件、闲聊时是否保持沉默；
- 小改动是否读取 0 references；
- 第一次具体行动前是否只读 0–2 份必要材料；
- 是否出现重复读取、全生命周期预加载、无意义 plan/TDD/worktree/subagent；
- result 与 fresh verification 是否更可靠；
- token 与命令 thrashing 是否下降。

样例见 `BEHAVIORAL_PROBES.md` 与 `evals/activation-prompts.csv`。

## 设计来源

本项目是独立重写，理念上受 Jesse Vincent / obra 的 `superpowers` 启发。原项目采用 MIT License。Softpowers 没有复制其强制 bootstrap、固定完整流水线或逐 task 双 review 机制。

详见 `THIRD_PARTY_NOTICES.md`。
