# Servotab website

Production static website for `https://servotab.com`, built with Astro and intended for Cloudflare Pages.

The Cloudflare build runtime is pinned to Node `22.16.0` in `.node-version`, which satisfies Astro 7's Node `>=22.12.0` requirement. Local verification may run on a newer compatible Node release; record that runtime separately from the deployment pin.

## Local development

```bash
npm ci
npm run dev
```

Create the production output in `dist/`:

```bash
npm test
npm run build
```

`npm test` exercises the homepage method-motion state machine, including rapid
repeated activation, timer cancellation, reduced-motion preference changes,
DOM selector contracts, and accessible button/status state. The repository CI
job runs these behavior checks before the production build.

The build expects the full repository checkout. `src/config.ts` reads source
identity from `../plugins/servotab/.codex-plugin/plugin.json` and keeps separately
observed GitHub release and Directory versions explicit so a staged publication
cannot make one surface impersonate another.

Cloudflare Pages build settings:

- Root directory: `site`
- Build command: `npm ci && npm run build`
- Output directory: `dist`

The site has no backend, database, account system, analytics, or first-party tracking. Domain redirects belong to the Cloudflare account configuration and must not be added to `public/_redirects`.

Open Graph and Twitter previews use the 1200 × 630
`public/servotab-social-card.png` projection. Its editable source is
`../assets/servotab-social-card.svg`; keep source and projection together and
inspect the rendered card before changing metadata dimensions or alt text.

## Public URLs

The homepage, Docs, and Methods search/share titles describe the plugin's purpose;
the visible brand headline remains independent. `src/layouts/BaseLayout.astro`
renders each page's title, description, canonical URL, and social metadata into
static HTML. `public/sitemap.xml` lists the seven indexable canonical routes;
use trailing slashes to match the directory URLs served by Cloudflare Pages,
keep it aligned with navigation, and exclude the noindex 404 page. The sitemap is
advertised by `public/robots.txt`. Search Console verification and submission are
separate owner-controlled operations; these files do not establish indexing.
The public Google verification meta tag in `BaseLayout.astro` preserves the
owner's Search Console verification and must remain present after verification.

The canonical domain is defined in `astro.config.mjs` and `src/config.ts`.
The current Servotab source, issue tracker, and official OpenAI Plugins
Directory listing URLs are centralized in `src/config.ts`. Source identity
derives from the plugin manifest; the separately observed GitHub release and
Directory versions advance only after their own public readbacks.

## Design authority

The implementation uses the approved Servotab `sᵗ` geometry and the v0 day-first identity: Paper `#FAF9F5`, Surface `#FFFFFF`, Ink `#151922`, Control blue `#315EFB`, open rails, raised controls, and bounded `tab → response → receipt → stop` motion. Reduced-motion users receive the final visual state without staged transitions.

The website links the live official Plugins Directory listing and separately
documents the source-checkout repository marketplace route for the current
tagged release. Keep the published directory payload, a later directory update,
source-checkout installation, and any tagged GitHub release as separate states.
Directory availability does not make Servotab an official OpenAI product.

Release availability is read from GitHub Releases; a source version must not be accompanied by a permanent "no tag/release exists" claim. A website source or build change does not deploy the public domain or update the plugin directory.
