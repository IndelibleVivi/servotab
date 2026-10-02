# Plan 策略升级实施计划

状态：源码候选与首轮有界行为对照已完成；全规格行为验收未完成。
规格：[Plan strategy v0.1](../specs/plan-strategy.md)。用户已委托开发该能力；附件讨论提供设计依据，不独立授权外部动作。
源码基线：`128cd20777d3660c50449cb653f207ddab893c78`；一个隐式 router、十二个显式 leaf。
维护责任：协调者维护本入口和当前实现；原 runtime worker 已停止并关闭，未留下源码变更。首轮八个独立语义审查责任均已返回并收回。

## 目标与当前路线

覆盖 REQ-01–12。先连接 router → Plan → Execute，复用 spec-chain 覆盖，同时准备能拒绝错误结果的场景。持久化沿用 Markdown 和现有责任，不新增 parser、hook、daemon、DAG 或第二进度源。

投入集中在目标清楚时仍能识别策略选择，以及恢复时核对实际状态。代表性成果包含触发、行动、实际结果和恢复依据；标题、字数或包检查不证明模型行为。

源码、生成包、fixture、文档和无模型检查已完成。2026-10-02 已获本轮 live 对照预算：最多12次 target +8次独立语义审查；用户在调用前将模型改为 `gpt-6.1-sol`，effort 保持 `xhigh`。安装、发布和部署独立。没有产品或验收 delta。

## 完整覆盖

| 需求 | 交付 | 验证场景 | 状态 |
|---|---|---|---|
| REQ-01 | router / catalog / Plan 策略触发 | C01–04、C10 | implemented；候选四次语义场景有 Plan 读取动作；非普遍激活证明 |
| REQ-02 | 继承目标、核实提议、权限 | C02、C06–07、C10–11 | implemented；共享假设四次与恢复四次的局部判断有证据 |
| REQ-03 | 质量投入、判断依赖、条件化细节 | C02–05、C12、C14 | implemented；共享边界时序已观察，领域投入尚未完整验证 |
| REQ-04 | 早期代表性成果与完整范围 | C03–05 | implemented；四次共享假设保留三种输出与编辑前 CLI 观察 |
| REQ-05 | 局部重排、成熟路径直行、探索退出 | C03–04、C07、C10 | implemented；初始假设修正已观察，真实 mid-run 变化仍未验证 |
| REQ-06 | 主动持久化、复用、位置与可见范围 | C06、C09、C13 | implemented；已有记录复用已观察，缺失记录与新建仍未验证 |
| REQ-07 | 明确任务入口、状态、覆盖、单写者 | C08–09、C11、C13 | implemented；四次显式入口/无关 lane 保持；并发压力未验证 |
| REQ-08 | 读取、更新、恢复、关闭与后继 | C07–10、C13 | implemented；候选两次恢复 accepted；替代/取消仍未验证 |
| REQ-09 | 领域协作与质量条件 | C05、C12、C14 | implemented；领域协作仍待真实成果 |
| REQ-10 | 安静执行、权限和 native 工具 | C01、C06、C12、C14 | implemented；微改直行、solo shell 与外部边界有有限证据 |
| REQ-11 | canonical/generated 与文档一致 | 完整源/包 gate 与双语说明 | verified（本地源码与包） |
| REQ-12 | 场景、负控、恢复、对照、真实使用 | [场景与预算](../../evals/plan-strategy.md)；fixture controls 已通过 | 部分完成；12 target +8 reviews 已完成，矩阵缺口与独立普通任务仍在 |

阶段 A：完整 runtime 路径（REQ-01–11）。阶段 B：fixture、文档与无模型 gate，依赖 A 最终产物。阶段 C：有预算的行为对照与恢复验证，依据结果修正 A/B。源码与首轮对照完成不代表全规格行为接受。

## 材料取舍

完整阅读 spec 385 行与讨论 768 行。采用自动策略判断、正向质量投入、真实判断依赖、条件化计划、主动持久化、明确任务归属、单写者、恢复与关闭。GUI/CLI 与素材例子保留为代表性原则，不新增 GUI 产品；早期切片不缩减最终范围。

外部方法中的交接决定、living document、明确任务绑定、阶段依赖作为设计理由；本次未独立核验其当前实现，不新增外部事实背书或复制代码。独立插件、固定阶段审批、按工具次数落盘、全局 active pointer、统一协议不采用，需求由现有方法承担。hooks / locator helper 留待真实压力，不在本次范围。Soundings / FC 提供可选领域贡献，无安装依赖。

## 观察与当前接续

基线与 spec 一致，开始时工作区干净。runtime lane 超时且确认停止，无分配文件变更；协调者接回该责任，原分工与完整目标保留。这次能力变化只改变执行者，没有重开产品讨论或缩减范围。

源码已连接 Plan / router / Execute，并完成 Spec Chain、Delegate、Finish 的必要接缝。Plan 的质量投入、条件化策略、早期可判断成果、读取/更新/恢复/关闭合同已落地。Design 与 Verify 的现有职责仍适用，无需为版本机械扩写。一个 router、十二个 leaves、70 个 package files 和既有版本不变。

确定性证据：canonical/generated sync、13-skill validation、manifest freshness、packaging selftest、82 Python tests 通过；Field Lab validate/selftest/list 覆盖28 cases，零 target 调用。三个新增场景和15个 adversarial controls 区分代码结果、写入范围与仍需语义审查的判断。一次针对错误 cursor 的测试变体意外形成循环，已改成有限且会被现有行为 oracle 拒绝的反例；通过不依赖超时。旧 first-path 标题检查在重写后失败，保留有用标题后重新生成并通过，不把字符串检查当行为证据。

README 双语、AGENTS、站点源码与 evidence 文档已同步。站点9 tests/build通过；实现阶段 Methods/Docs 在1280px与390px无横向溢出，已检查的渲染可读，console 无 error/warning；证据状态文字更新后重新通过 install/test/build，未重复渲染检查；既有间接 dependency `devalue` 的 npm audit advisory 留为独立事实，本次无 dependency 改动。Oracle 咨询未发送，因专用浏览器需要登录/验证；无独立 Oracle 意见可用，不影响本地审查与既有验证。

首轮 [有界行为对照](../../evals/plan-strategy.md) 已完成：12次 target、8次独立语义审查，全部请求 `gpt-6.1-sol` / `xhigh`，无重试。12次确定性检查全通过；receipt-bound acceptance 为候选6/6、基线5/6。基线恢复 repeat1 未读取模糊发布 receipt，最终遗漏历史发布状态仍未知，故拒绝。其他三次恢复保留这一边界；候选 repeat2 曾暂写 not published，之后在最终检查前纠正。共享假设四次均在编辑前观察真实 CLI 失败并修复同一 collector，不把基线成功计作新版提升。

现有 acceptance checker 的硬编码 lab ID 拒绝了独立命名 study；新增显式 `--lab-id`，默认仍为 servotab，case/prompt、artifact integrity 与独立 review 全部保留。原 receipts 未改、target 未重跑；19个 focused checker tests 通过。Reviewer 原始输出保留，只有机器字段格式被映射为 Field Lab 要求，不改判断。源码包未随证据收尾变更。

本组候选/基线总 shell commands 为69/64，累计 target-process seconds 为905.193/823.655，故没有效率提升结论。每case仅两次、同host重叠运行、同模型非盲审且无独立host control，不作普遍因果推论。后续覆盖真实 mid-run 变化、准确/缺失记录、替代/取消与代表性体验及独立普通工程任务；新的 live 调用需要另有预算。原始 trace 留在公共树外。

## 关闭与后继

源码与本轮授权对照完成，全规格未关闭；无替代计划。REQ-01–10 的 runtime 合同已实现并有上述有限行为证据，REQ-11 获本地源/包证据，REQ-12 仍有未覆盖的真实行为接受条件。2026-10-03 已按用户授权从 clean `cd03673` 安装本机候选：70个 package files 与源码逐字节一致，installed/enabled；fresh-process discovery 发现新版 router。版本标签仍为0.6.5，内容已区别于 tagged release。当前长对话的上下文刷新与安装后的真实任务行为未验证，未合并、发布或部署。恢复时先核对本任务 diff、当前实现与证据，不按表中状态重放动作。正式使用说明在 README 和方法文档，本计划不替代操作手册。
