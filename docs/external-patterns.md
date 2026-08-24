# External Pattern Registry

这份 registry 记录 Softpowers 当前主动关注的外部来源、pinned ref、已选 pattern、decision 与 reopen condition。它承担增量复查入口；不构成 dependency list，也不表示代码或文本已被复制进 Softpowers。

Review date：`2026-08-19`

## Current sources

| Source | Pinned ref | License / reuse note | Current decision | Landing plane |
|---|---|---|---|---|
| `anthropics/defending-code-reference-harness` | `d3bea6b5793b5f3d59a75ebe69a58efa88383145` | Apache-2.0 | `ADAPT` applied in rc2: canaries、artifacts、atomic result/resume；`REJECT` daily full pipeline | Eval / maintainer |
| `anthropics/skills` — `skill-creator` | `f6656c1256d5a8adfa37db9110046ef20bac644c` | `skill-creator` Apache-2.0 | `ADAPT` objective assertions applied；isolated paired evals and qualitative viewer remain deferred | Eval / maintainer |
| `mattpocock/skills` — `grill-me` / `grilling` | `1bb95954ef0d06ba4d64a9c267fb75f57c614a1f` | MIT | `ADAPT` dependency-aware decision frontier into a shadow probe；`REJECT` mandatory exhaustive interviewing ([record](../evals/candidates/2026-08-19-matt-grilling-frontier.md)) | Brainstorm / eval |
| `affaan-m/ECC` — `search-first` | `06c5e118c4d3e6c3b7f9445f973a2194c82de193` | MIT | `ADAPT` internal-first reuse and search-channel honesty into a shadow probe；`REJECT` universal research stage and full-harness adoption ([record](../evals/candidates/2026-08-19-ecc-search-first.md)) | Execute / eval |
| `obra/superpowers` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | MIT | `ADAPT` distribution maturity；`REJECT` mandatory lifecycle | Packaging / docs |
| `QoderAI/better-harness` | `36c85c40ffb7596d413cc14bfbc8e66c741c182e` | MIT | `ALREADY COVERED` claim maturity core；`ADAPT` eval vocabulary only | Verify / eval |
| `humanlayer/12-factor-agents` | `d20c728368bf9c189d6d7aab704744decb6ec0cc` | Code Apache-2.0；content CC BY-SA-4.0 | `ALREADY COVERED` control principles；`ADAPT` explicit run identity and case-boundary resume applied | Architecture docs / eval |
| `SWE-agent/mini-swe-agent` | `a83fcae82d2a08f0ee0c688f9d137b3566c097f8` | MIT | `ADAPT` thin runner / linear raw JSONL trace applied | Eval implementation |
| `SWE-bench/SWE-bench` | `ca6e4e0d252f32f8762625b73575d5dee49d0a5a` | MIT | `ADAPT` fixture and subject identity metadata applied；cache/regrade remains deferred | Eval implementation |
| `UKGovernmentBEIS/inspect_ai` | `286163f12aa627af22051bd95321bc6404e237ae` | Inspect repository license applies; verify exact reused component before copying | `DEFER` framework dependency；`ADAPT` task/solver/scorer separation conceptually | Eval architecture |
| `openai/plugins` | `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` | No repository-level license file at this ref；inspect each plugin manifest before reuse | `DEFER` generated plugin projection until distribution need is real | Packaging / distribution |
| `trailofbits/overtly-malicious-skills` | `4ffbf9461ef0505f9ce76a0d3694a18ec33ea531` | No license file at this ref；security research reference only; never install | `ADAPT` adversarial audit ideas；`REJECT` executing upstream payloads | Security tests |

## Watch focus

### Anthropic defending harness

Review only material changes around:

- separation of candidate producer and clean verifier；
- durable artifacts, atomic checkpoint and resume；
- canary targets and captured example runs；
- enforced sandbox and capability boundary；
- claims grounded in executable witnesses。

Ignore ordinary expansion of its security-specific stages unless Softpowers later gains a matching high-risk use case.

### Anthropic skill-creator

Review:

- with-skill / baseline comparison design；
- trigger evaluation and variance handling；
- objective assertion vs qualitative judgment boundary；
- run artifact schema and viewer ergonomics；
- iteration without replacing user judgment。

Do not import a requirement that every subjective task be numerically graded.

### Matt Pocock skills

Review only material changes around:

- decision-tree and frontier ordering semantics；
- the split between facts the agent should inspect and decisions the user should make；
- branch-local blocking while an environmental investigation remains open；
- the relationship between the explicit `grill-me` entry point and reusable `grilling` discipline。

Retain the current rejection of mandatory exhaustive interviews, fixed question formatting, full-tree traversal for clear work, and a new wrapper-to-core invocation topology inside Softpowers.

### ECC search-first

Review only material changes around:

- repository and installed-dependency search before external discovery；
- honest claims when registries, GitHub, MCP, or local catalogs are unavailable；
- adopt / extend / compose / build closure；
- candidate evaluation that includes maintenance, compatibility, license, dependency cost, and a current caller；
- changes that make the skill less tied to one harness or hard-coded ecosystem list。

Do not treat growth elsewhere in ECC's agents, hooks, memory, rules, MCP configuration, or lifecycle as a Softpowers requirement. Retain the rejection of universal research stages and full-harness adoption for this narrow behavior.

### Superpowers

Review:

- cross-host packaging；
- marketplace metadata；
- installation and onboarding clarity；
- skill naming and documentation discoverability。

Retain the current rejection of mandatory brainstorming, worktrees, universal TDD, per-task subagents and double review.

### Better Harness

Review only changes that sharpen evidence boundaries:

- present / wired / exercised / later outcome distinctions；
- honest unobserved state；
- task-bounded evidence linkage。

Do not adopt default scoring, recurring audit reports, intervention ledgers or background monitoring.

### 12-factor-agents

Review:

- context ownership；
- control-flow ownership；
- pause/resume；
- compact error representation；
- small focused execution units。

Use these as architecture guidance. They do not become a deterministic DAG around every Codex task.

### mini-swe-agent and SWE-bench

Review:

- thin and inspectable control flow；
- linear, replayable trajectories；
- independent subprocess execution；
- fixture identity；
- reproducible environment and cache keys；
- re-grading saved outputs。

Keep Softpowers runtime host-native. The rc2 embedded runner applied the
thin-process, fixture-identity and raw-artifact kernels without importing either
framework; rc5 moved that generic machinery into standalone Skill Field Lab and
kept only the Softpowers subject cases here. Richer cache/regrade semantics
remain deferred.

### Inspect AI

Review when Softpowers needs a richer eval engine:

- task / solver / scorer separation；
- sandbox and approval abstractions；
- logs and re-scoring；
- model-graded evaluation boundaries。

A direct Inspect AI dependency stays deferred until the standalone Field Lab
runner demonstrably fails to meet current needs.

### OpenAI plugins

Review when:

- Softpowers prepares official plugin distribution；
- plugin manifest or marketplace contract changes；
- skills, agents, commands, hooks or MCP surfaces become relevant to one package。

Canonical `methods/*.md` and the Softpowers catalog remain source of truth. Plugin metadata should be generated projection.

### Trail of Bits malicious skills

Review only from source in a controlled research context. Extract scanner and packaging attack shapes into synthetic inert fixtures. Never install the upstream samples, execute their payloads, or make CI depend on them.

## Adding an emerging source

A new repository enters this registry when at least one condition holds:

- it addresses a recent real Softpowers failure；
- it contains a mechanism absent from current methods and evals；
- it provides reproducible evidence unavailable in current references；
- it changes Codex skill/plugin compatibility or distribution；
- the same pattern appears independently across multiple projects；
- it supplies a useful adversarial counterexample。

Popularity alone is insufficient.

## Updating a source

1. Resolve the current ref.
2. Compare with the stored pinned ref.
3. Inspect only the watch focus and material dependent changes.
4. Update the decision when evidence changes.
5. Create a candidate record only when a new probe or apply decision is justified.
6. Keep private traces and account-specific evidence outside the public tree.
