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

Cloudflare Pages build settings:

- Root directory: `site`
- Build command: `npm ci && npm run build`
- Output directory: `dist`

The site has no backend, database, account system, analytics, or first-party tracking. Domain redirects belong to the Cloudflare account configuration and must not be added to `public/_redirects`.

## Public URLs

The canonical domain is defined in `astro.config.mjs` and `src/config.ts`. The current source and issue tracker URLs are centralized in `src/config.ts`; update both values together after the GitHub repository cutover.

## Design authority

The implementation uses the approved Servotab `sᵗ` geometry and the v0 day-first identity: Paper `#FAF9F5`, Surface `#FFFFFF`, Ink `#151922`, Control blue `#315EFB`, open rails, raised controls, and bounded `tab → response → receipt → stop` motion. Reduced-motion users receive the final visual state without staged transitions.

Do not add an installation action or runtime invocation syntax until the public plugin package establishes those contracts. Servotab is not currently listed in the OpenAI plugin directory.
