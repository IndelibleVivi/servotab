export const SITE = {
  name: "Servotab",
  wordmark: "servotab",
  origin: "https://servotab.com",
  description:
    "Adaptive engineering methods for planning, implementation, debugging, review, and verification in Codex.",
} as const;

// Keep the public source and issue tracker on the same repository identity.
export const PROJECT_LINKS = {
  source: "https://github.com/IndelibleVivi/servotab",
  issues: "https://github.com/IndelibleVivi/servotab/issues",
  behaviorReport:
    "https://github.com/IndelibleVivi/servotab/issues/new?template=behavior-feedback.yml",
  packageBug:
    "https://github.com/IndelibleVivi/servotab/issues/new?template=plugin-package-bug.yml",
} as const;

export const repoFile = (path: string) =>
  `${PROJECT_LINKS.source}/blob/HEAD/${path}`;
