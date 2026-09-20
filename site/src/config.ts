import pluginManifest from "../../plugins/servotab/.codex-plugin/plugin.json";

export const SITE = {
  name: "Servotab",
  wordmark: "servotab",
  origin: "https://servotab.com",
  version: pluginManifest.version,
  // Observed publication, independent of the source manifest version.
  publishedVersion: "0.6.3",
  description:
    "A Codex plugin for planning, implementation, debugging, code review, and verification. Keep clear changes direct and match engineering methods to the work.",
} as const;

// Keep the public source and issue tracker on the same repository identity.
export const PROJECT_LINKS = {
  source: "https://github.com/IndelibleVivi/servotab",
  pluginDirectory:
    "https://chatgpt.com/plugins/plugins_6a952d7c729c819196646fda7ec9ad94",
  issues: "https://github.com/IndelibleVivi/servotab/issues",
  behaviorReport:
    "https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml",
  packageBug:
    "https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml",
  securityPolicy:
    "https://github.com/IndelibleVivi/servotab/blob/HEAD/SECURITY.md",
  securityReport:
    "https://github.com/IndelibleVivi/servotab/security/advisories/new",
} as const;

export const RELATED_PROJECTS = {
  mcpBoundary: "https://indeliblevivi.github.io/mcp-boundary/",
  workerRouting: "https://indeliblevivi.github.io/codex-worker-routing/",
} as const;

export const repoFile = (path: string) =>
  `${PROJECT_LINKS.source}/blob/HEAD/${path}`;
