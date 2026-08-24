# Internal-first reuse gate from `search-first`

Status: `DECIDED`
Decision: `ADAPT`

## Source

- Repository: `affaan-m/ECC`
- Component: `skills/search-first`
- Pinned ref: `06c5e118c4d3e6c3b7f9445f973a2194c82de193`
- License: MIT
- Reviewed files: `skills/search-first/SKILL.md`, `.codex-plugin/plugin.json`, `README.md`
- Review date: `2026-08-19`

## Discovery context

A community recommendation grouped `search-first` with `grill-me` as a must-install and encouraged serious forks of both source repositories. The review separated the narrow skill mechanism from ECC's much larger harness operating system.

## Distilled pattern

Before writing generic machinery for a common problem, search in an ordered way for an existing supported solution. Check which search channels are actually available, define the needed behavior and project constraints, inspect candidates, then close the research with an engineering decision: adopt, extend, compose, or build.

Search begins with the current repository and installed dependency surface. Missing registries, GitHub access, MCP catalogs, or local skill directories constrain the claim and must be reported honestly. “Nothing suitable exists” is not supported when relevant channels were unavailable or skipped.

## Local signal

No repeated Softpowers failure is currently recorded for this exact gate. `Soft Execute` already checks whether requested behavior exists differently, limits additional search to questions that can change implementation or confidence, and prefers one supported path. `Soft Brainstorm` already verifies whether a new integration, transport, fallback, or abstraction is actually necessary.

The narrower possible gap is that Softpowers does not state an explicit reuse order across repository code, installed dependencies, supported platform surfaces, and external implementations. It also does not name unavailable-channel honesty as a dedicated claim boundary.

## Existing coverage

- `methods/execute.md` checks for existing implementation and asks whether each added search or check can change the implementation or confidence.
- `methods/brainstorm.md` verifies the assumption behind new integrations, transports, fallbacks, and abstractions before designing them.
- The router already keeps clear local work direct and rejects speculative dependencies or second paths without a present caller.
- Softpowers is intentionally smaller than ECC and does not need ECC's agents, hooks, memory, rules, MCP configuration, or broad lifecycle to preserve this kernel.

## Decision hypothesis

- Accepted kernel: repository and installed-dependency search first; explicit search-channel availability; honest coverage claims; adopt / extend / compose / build as research closure; license, maintenance, dependency cost, compatibility, and current callers as candidate criteria.
- Excluded machinery: a universal multi-channel research stage before every feature; hard-coded Claude, MCP, registry, or package recommendations; package or MCP search before inspecting local code; adopting a dependency because it is popular or permissively licensed alone; a second implicit research router; installing or forking the full ECC harness for this one behavior.
- Landing plane: eval / maintainer first; possible narrow clarification in `execute.md` or `brainstorm.md` only after a reproduced gap.
- Smallest useful delta: retain this candidate and design one shadow probe. Do not change runtime methods, install ECC, add a standalone `search-first` leaf, or start a live target-agent run in this intake.

## Probe

- Fixture or task: add a JSON Schema validation helper to a repository that already contains Ajv in the lockfile, an existing schema loader, and a nearby validation caller.
- Candidate behavior: inspect repository code and installed dependencies first; reuse or thinly adapt the existing path; stop without searching MCP or GitHub once the local evidence settles the choice.
- Baseline/control: implement a highly domain-specific invariant with no plausible generic package boundary; do not launch a package scavenger hunt merely because the task contains the word “validation.”
- Deterministic assertions: no new validation dependency; the existing loader remains the source of truth; unavailable external channels are not described as searched; the control task does not add irrelevant dependency research.
- Semantic judgment: the chosen reuse boundary remains simpler than a new abstraction and still satisfies the complete requested outcome.
- Falsifier: current Softpowers already reaches the same result consistently, or an explicit search gate increases low-value browsing and dependency tourism.

## Verification if applied

- Search existing dogfood for dependency, helper, parser, validator, and integration decisions.
- Start with one local-reuse positive case and one domain-specific negative control.
- Evaluate final architecture and dependency delta before counting search breadth.
- Use Skill Field Lab only when the behavior claim remains unresolved; no live run is authorized by this record.

## Result

`ADAPT` at the intake and probe plane. The source contains a sound engineering habit and useful claim discipline, but it does not justify importing ECC's broader operating system or creating a mandatory research stage.

No runtime wording, new skill, installer change, dependency, full-repository fork, or live evaluation is approved in this record.

Reopen when Softpowers duplicates existing repository machinery, introduces an avoidable dependency, overclaims search coverage, or when the upstream skill materially changes its ordering or evaluation contract.
