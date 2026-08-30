export const SITE = {
  name: "Servotab",
  wordmark: "servotab",
  origin: "https://servotab.com",
  description:
    "Adaptive engineering methods for planning, implementation, debugging, review, and verification in Codex.",
} as const;

// Update these two values together when the GitHub cutover is complete.
export const PROJECT_LINKS = {
  source: "https://github.com/IndelibleVivi/softpowers",
  issues: "https://github.com/IndelibleVivi/softpowers/issues",
} as const;

export const repoFile = (path: string) =>
  `${PROJECT_LINKS.source}/blob/HEAD/${path}`;
