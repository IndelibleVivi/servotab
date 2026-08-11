# Contributing to Softpowers

谢谢你愿意把真实任务里的反馈带回来。Softpowers 目前是 public release candidate；activation miss、false positive、绕路、scope 丢失和 installer failure 都比泛泛的“再加一个 workflow”更有价值。

## 先选择反馈类型

- [Behavior feedback](https://github.com/IndelibleVivi/softpowers/issues/new?template=behavior-feedback.yml)：routing、activation、complete outcome、debug/review/verification 质量或无意义 overhead。
- [Installer bug](https://github.com/IndelibleVivi/softpowers/issues/new?template=installer-bug.yml)：install、update、uninstall、rollback、manifest 或 skill-root 解析。
- 其他明确 proposal 可以开普通 issue；请说明它解决的真实任务，而不只是新增一种方法名称。

## Public issue 的隐私边界

GitHub Issues 是公开的。提交前请删除：

- credentials、tokens、cookies、`.env` 与 account details；
- private repository source、客户/课程/申请材料或内部日志；
- 私人聊天、真实个人数据与不能公开的文件路径；
- 与问题无关的 model output 或长篇 trace。

保留最小可复现 evidence。无法公开的材料不要上传；可以用脱敏后的结构、占位值或小型 synthetic reproduction 代替。

## Behavior feedback 应该包含什么

尽量提供：

1. Softpowers version 或 commit；
2. Codex surface、model（如果相关）、OS 与 repo 类型；
3. 已脱敏的原始 prompt；
4. expected behavior 与 observed behavior；
5. 是否触发 `softpowers`，以及看得到时读取了哪些 references；
6. outcome 是否完整；
7. 是否出现多余 plan、reference reads、tests、hashes、tool calls、subagents 或重复 verification。

不要只用 token 总量判断好坏。先判断 outcome 与必要边界是否保留，再比较 overhead。

## Code 与 method changes

Canonical method source 在：

```text
methods/*.md
```

`skills/softpowers/references/*.md` 与 12 个 leaf `SKILL.md` 是 generated output。不要只改 generated copy。

Router metadata、leaf catalog 与 display strings 在：

```text
scripts/skill_catalog.py
```

修改 method 或 catalog 后运行：

```bash
python3 scripts/build_skills.py
python3 scripts/validate_sync.py
python3 scripts/generate_pack_manifest.py
python3 scripts/selftest.py
```

提交前完整 maintainer gate：

```bash
python3 scripts/build_skills.py --check
python3 scripts/validate_sync.py
python3 scripts/validate.py --exact skills
python3 scripts/generate_pack_manifest.py --check
python3 scripts/selftest.py
python3 scripts/audit_public_tree.py
python3 -m py_compile scripts/*.py
bash -n install.sh uninstall.sh
```

`scripts/validate.py` 与 manifest generation 的 exact YAML gate 需要 PyYAML；用户 install/uninstall 不需要第三方 dependency。

## Change shape

- 让 workflow 服务于可观察的工程任务，不为方法本身制造仪式。
- 保留明确要求的完整 usable outcome；不要默认缩成 MVP、scaffold 或局部 tranche。
- 只为 observed failure、明确 contract 或真实 boundary 增加 guard、fallback、hash 与 test。
- Router 保持 quiet；leaf skills 保持 explicit-only，除非一个 release proposal 明确改变 activation topology。
- Public docs、packaging 与 feedback assets 可以进 repo；`notes/`、`.local/`、`*.private.md`、private eval traces 与 account state 不应提交。`.gitignore` 只是预防误操作，不是 privacy boundary。

Pull request 请说明 changed contract、fresh verification，以及任何 deliberately deferred work。
