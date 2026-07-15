# App Architecture Reference

Use this when building local browsing, static frontend data, or GitHub Pages deployment.

## Goals

- Browse SQLite networks and GEXF metadata locally.
- Generate static JSON assets for GitHub Pages.
- Keep Pages deployment independent of Python server runtime.
- Let research artifacts remain the source of truth.

## Local Backend

Provide a small Python standard-library HTTP server:

- `GET /api/inventory`
- `GET /api/databases`
- `GET /api/database/{name}/summary`
- `GET /api/database/{name}/persons`
- `GET /api/database/{name}/relationships`
- `GET /api/graphs`
- `GET /api/person-profiles`
- static files from `docs/`

Use read-only SQLite connections. Never mutate research databases from the server.

## Static Frontend

Generate `docs/assets/data/*.json` from local artifacts:

- `inventory.json`
- `databases.json`
- `graphs.json`
- `person_profiles.json`
- `reports.json`

Frontend requirements:

- Load static JSON on GitHub Pages.
- Search/filter databases, reports, person profiles.
- Link to reports and graph files.
- Show database summaries produced at build time.
- Avoid requiring a live backend on Pages.

## GitHub Pages

Use GitHub Actions to:

1. checkout repo
2. run static data build script
3. upload `docs/` as Pages artifact
4. deploy to Pages

The workflow should not run expensive web research. It only publishes existing artifacts.

