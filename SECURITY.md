# Servotab security policy

Servotab is a skills-only Codex plugin. It has no Servotab account, backend, database, telemetry service, or network endpoint, but its package, engineering instructions, and trust-boundary guidance can still carry security consequences.

## Supported line

Security fixes target the current source candidate on `main`. Historical Softpowers revisions and earlier release-candidate lines are preserved for provenance and migration, but they do not receive the same active support commitment.

When reporting, identify the exact Servotab version or commit and the Codex surface where the behavior was observed.

## Report privately when disclosure would create risk

Use [GitHub Private Vulnerability Reporting](https://github.com/IndelibleVivi/servotab/security/advisories/new) for evidence that cannot be made public safely.

Private reports are appropriate for issues such as:

- plugin-package tampering, unexpected files, or a distribution-integrity failure;
- instructions that materially encourage unauthorized destructive actions, secret disclosure, or permission-boundary bypass;
- a reproducible route by which private repository content, credentials, account data, or private transcripts are exposed because of Servotab-owned material;
- a security-relevant activation or routing failure whose minimal reproduction would reveal sensitive source; or
- another vulnerability in Servotab-owned source, package metadata, website source, or release process.

Include the smallest evidence that establishes the issue:

1. affected version or commit;
2. Codex surface and platform;
3. impact and required preconditions;
4. sanitized reproduction steps;
5. expected and observed boundary behavior; and
6. any known workaround.

Do not include unrelated private source, full transcripts, credentials, tokens, account data, or personal absolute paths. Redact aggressively even in a private report.

The maintainer does not promise a fixed response-time SLA. Reports will be assessed against the current source and reproduced when enough safe evidence is available. Publication, credit, and remediation timing should be coordinated in the private advisory before public disclosure.

## Use public issues for public-safe defects

If the report is reproducible without sensitive material and does not create a disclosure risk, use the normal [behavior feedback](https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml) or [plugin package bug](https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml) form.

GitHub Issues are public. Never post credentials, private source, personal data, private filesystem paths, account details, local notes, or full private Codex transcripts.

## Boundaries outside this repository

Report vulnerabilities in Codex, OpenAI accounts or services, GitHub, Cloudflare, package-manager infrastructure, or another dependency to the responsible provider. A product used alongside Servotab does not become Servotab-owned merely because the workflow reached it.

Servotab's policy does not expand Codex permissions or replace repository-specific security instructions. It also does not authorize testing against systems, repositories, accounts, or data you do not own or have permission to assess.
