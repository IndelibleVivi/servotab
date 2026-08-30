# Contributing to Servotab

谢谢你愿意把真实任务里的 evidence 带回来。Servotab `0.4.0-rc1` 是 plugin-native source candidate；activation miss、false positive、错误 routing、scope 丢失、package failure 和没有必要的流程，都比泛泛的“再加一个 workflow”更有价值。

## 先选择反馈类型

- [Behavior feedback](https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml)：routing、activation、complete outcome、debug/review/verification 质量或无意义 overhead；
- [Plugin package bug](https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml)：marketplace discovery、plugin validation、installation/update、activation 或 package asset；
- 其他明确 proposal 可以开普通 issue；请说明它解决的真实任务，而不只是提出一个新 method name。

## Public issue 的隐私边界

GitHub Issues 是公开的。提交前请删除：

- credentials、tokens、cookies、`.env` 与 account details；
- private repository source、客户/课程/申请材料或内部日志；
- 私人聊天、真实个人数据与不能公开的 file path；
- 与问题无关的 model output、完整 Codex transcript 或长篇 trace。

保留最小可复现 evidence。无法公开的材料不要上传；使用脱敏结构、placeholder 或小型 synthetic reproduction。

## Behavior feedback 应该包含什么

尽量提供：

1. Servotab version 或 commit；
2. Codex surface、model（如果相关）、OS 与 repo 类型；
3. 已脱敏的原始 prompt；
4. expected behavior 与 observed behavior；
5. `servotab` 是否触发，以及看得到时读取了哪些 references；
6. requested outcome 是否完整；
7. 是否出现多余 plan、reference reads、tests、hashes、tool calls、subagents 或重复 verification。

报告 delegation behavior 时，请分开记录：

- host/runtime 是否提供 subagent tools；
- router 是否读取 `delegate.md`；
- task topology 是否真的有 independent lanes；
- worker output 是否经过 coordinator verification。

Subagent event 本身不证明 `delegate` leaf 或 Servotab method 被选中。不要只按 token count 判断好坏；先看 outcome、authority 与必要边界是否被保留。

## Canonical source 与 generated package

12 个 method bodies 的 canonical source 是：

```text
methods/*.md
```

Names、descriptions、default prompts 与 activation metadata 的 canonical catalog 是：

```text
scripts/skill_catalog.py
```

`scripts/build_skills.py` 从这些 source 生成：

```text
plugins/servotab/skills/servotab/SKILL.md
plugins/servotab/skills/servotab/references/*.md
plugins/servotab/skills/{design,...,finish}/SKILL.md
plugins/servotab/skills/*/agents/openai.yaml
plugins/servotab/assets/{composer-icon.png,logo.png}
```

不要直接编辑 `plugins/servotab/skills/**` 或 curated plugin asset copy。修改 method、catalog 或 root canonical asset 后运行 generator，再检查 diff。Root `skills/`、`install.sh`、`uninstall.sh`、`scripts/install.py` 与 `scripts/uninstall.py` 已退出 current architecture；不要重新创建它们作为平行安装路径。

Plugin manifest 与 repo marketplace contract 分别位于：

```text
plugins/servotab/.codex-plugin/plugin.json
plugins/servotab/LICENSE
plugins/servotab/NOTICE.md
.agents/plugins/marketplace.json
```

Plugin-local `LICENSE` 与 `NOTICE.md` 把 functional-material terms 和 identity-asset boundary 带进 installable package；修改它们需要对应 rights evidence 与 license-surface review。`PACK_MANIFEST.json` 记录 exact derived payload identity。它由 `scripts/generate_pack_manifest.py` 生成，不能手改 digest 或 file list 来掩盖 source/generated drift。

## Method changes

- 让 method 服务于可观察的 engineering task，不为 method 自己制造 ceremony。
- 保留明确要求的完整 usable outcome；不要默认缩成 MVP、scaffold、placeholder 或局部 tranche。
- Logs、screenshots、reviews、plans 与 generated outputs 先按 current intent 和 authority 判断是 instruction、evidence 还是 inspiration。
- 只为 observed failure、明确 contract 或真实 boundary 增加 guard、fallback、hash 与 test。
- Router 保持 quiet；只有 `servotab` implicit eligible，12 个 leaves 保持 explicit-only，除非一个明确 release proposal 改变 activation topology。
- `design`、`review-feedback` 与 `delegate` 是 current semantic IDs；不要把 retired `brainstorm`、`receive-review`、`parallel` identifiers 放回 active payload。

## Field Lab 与 behavior evidence

Servotab 自己的 subject material 位于：

```text
fieldlab-pack.json
evals/cases/
evals/candidates/
evals/claims/
evals/receipts/
evals/decisions/
```

`fieldlab-pack.json` 使用 schema v2，并将 `plugins/servotab/skills` 作为 current source subject。通用 runner、schemas、process containment 与 quota gate 属于 optional standalone Skill Field Lab companion。不要把它们复制进 plugin payload，也不要让 Servotab 管理 Field Lab CLI 或 controller skills。

## Website changes

`site/` 是独立 Astro static application。它不属于 plugin payload，也不能改变 plugin installation 或 OpenAI directory status。Website copy 必须区分 source candidate、installed plugin、Cloudflare deployment、custom-domain activation 与 OpenAI publication。

本地检查：

```bash
cd site
npm ci
npm run build
```

Cloudflare settings 与 domain-level redirect ownership 见 [site/README.md](site/README.md)。不要把 account-specific IDs、local cache 或 private deployment notes 加进 public tree。

## Maintainer gate

修改 method 或 catalog 后先 regenerate：

```bash
python3 scripts/build_skills.py
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
python3 scripts/generate_pack_manifest.py
```

提交前运行 fresh deterministic gate：

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
uv run --with PyYAML==6.0.3 python3 scripts/validate.py plugins/servotab/skills
uv run --with PyYAML==6.0.3 python3 scripts/generate_pack_manifest.py --check
uv run --with PyYAML==6.0.3 python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
```

若本机另行安装了 `fieldlab`，可以加跑不启动 target model 的 subject-pack gate：

```bash
fieldlab validate fieldlab-pack.json
fieldlab selftest fieldlab-pack.json
fieldlab list fieldlab-pack.json
```

Live model eval、live plugin installation、Cloudflare deployment、GitHub rename、commit/push/release 与 OpenAI directory submission 都是不同的 action surface，不由 deterministic maintainer gate 自动触发。

## Documentation closure

改变 package identity、method IDs、canonical/generated boundary、install route、website behavior 或 release state 时，更新相应 authority surface：

- `README.md`：durable user-facing product、installation、usage 与 limitations；
- `AGENTS.md`：stable source/generated、verification 与 authorization contract；
- `docs/current-state.md`：易变的 installed / deployed / live / rename / submission 状态；
- `docs/migration-from-softpowers.md`：仍受支持的 legacy layer migration；
- `CHANGELOG.md`：实际 shipped history 与未发布 changes；
- `site/README.md` 和 site copy：网站当前可观察行为。

历史 release 与 provenance 不要改写成 Servotab 当时已经存在。过渡说明应明确旧 Softpowers identifiers 属于 historical or migration context。

## Contribution license

提交 contribution 表示你有权提交该内容，并按 [LICENSING.md](LICENSING.md) 中适用于目标 file 的 license 提供该 contribution。不要从 repository label 推导统一 terms，也不要用普通 PR 改写 third-party、external-contributor 或既有历史 rights。

如果 change 跨越多个 licensing surfaces，请在 PR 中逐项说明。任何超出 public licenses 的 commercial permission 只能由相关 rights holder 另行书面授予。

Pull request 请说明 changed contract、fresh verification、documentation impact，以及 deliberately deferred work。
