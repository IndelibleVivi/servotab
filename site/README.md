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
npm run build
```

The build expects the full repository checkout. `src/config.ts` reads the current
candidate version from `../plugins/servotab/.codex-plugin/plugin.json` so the
website status rail and Quickstart do not maintain a second version string.

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

The canonical domain is defined in `astro.config.mjs` and `src/config.ts`. The current Servotab source and issue tracker URLs are centralized in `src/config.ts` and must stay on the same repository identity. Candidate-version copy derives from the plugin manifest rather than a website-local constant.

## Design authority

The implementation uses the approved Servotab `sᵗ` geometry and the v0 day-first identity: Paper `#FAF9F5`, Surface `#FFFFFF`, Ink `#151922`, Control blue `#315EFB`, open rails, raised controls, and bounded `tab → response → receipt → stop` motion. Reduced-motion users receive the final visual state without staged transitions.

The website documents the source-checkout repository marketplace route for the current candidate. Keep that route explicitly separate from a tagged release, OpenAI plugin directory submission or listing, and OpenAI approval.
