# Agents Guide

Authoritative instructions for any automation or coding agent working on `farhaan.bukh.sh`.

## 1. Architecture Overview

This is a **static site with a Python build step**. Markdown content files are converted to HTML at build time using Jinja2 templates. The output lands in `dist/` which is deployed to GitHub Pages. There is **no client-side markdown rendering**.

### Key decisions
- **uv** for Python dependency management + virtualenv.
- **just** as the task runner (see `justfile`).
- **Jinja2** templates preserve the existing HTML/CSS structure exactly.
- **`content/`** directory holds all user-editable markdown (with YAML frontmatter where needed).
- **`dist/`** is the build artifact — never committed, always generated.

## 2. Repository Layout

```
.
├── .github/workflows/deploy.yml   # GitHub Pages: uv sync → build → deploy dist/
├── assets/                        # Static assets (copied verbatim into dist/)
│   ├── css/style.css
│   ├── img/avatar.png
│   ├── img/icons/                 # Pixel-art SVG icons (sword, book, scroll, etc.)
│   └── js/main.js                 # Nav toggle, inventory tray toggle, year stamp
├── content/                       # Editable markdown source files
│   ├── index.md                   # Home page data (YAML frontmatter + markdown body)
│   └── talks.md                   # Talks list (pure markdown)
├── templates/                     # Jinja2 HTML templates
│   ├── base.html                  # Shared shell (head, nav, footer)
│   ├── index.html                 # Home page (hero, inventory tray)
│   └── talks.html                 # Talks page (pre-rendered markdown)
├── build.py                       # Python build script
├── justfile                       # Task runner recipes
├── pyproject.toml                 # uv project + dependencies
├── .python-version                # Pinned Python version
├── CNAME                          # Custom domain: farhaan.bukh.sh
├── agents.md                      # This file
├── prompt.md                      # Accepted prompt log
└── README.md
```

## 3. Prerequisites

- **Python 3.12+** (pinned in `.python-version`).
- **uv** installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- **just** installed (`brew install just` / `cargo install just`).
- GitHub repo with Actions + Pages enabled.

## 4. Task Runner (justfile)

| Recipe | What it does |
|--------|-------------|
| `just setup` | Runs `uv sync` — creates venv, installs dependencies. |
| `just build` | Runs setup + `uv run python build.py` → produces `dist/`. |
| `just serve` | Builds then serves `dist/` at `http://localhost:5000`. |
| `just dev`   | Alias for build + serve. |
| `just clean` | Removes `dist/`. |
| `just check` | Basic smoke test that expected files exist in `dist/`. |

## 5. Build Pipeline Detail

`build.py` performs the following in order:

1. Clean/create `dist/` directory.
2. Parse `content/index.md` — split YAML frontmatter (via PyYAML) from markdown body (via `markdown` lib).
3. Parse `content/talks.md` — convert full markdown to HTML.
4. Load Jinja2 templates from `templates/`.
5. Render `index.html` and `talks.html` with parsed data into `dist/`.
6. Copy `assets/` → `dist/assets/` verbatim.
7. Copy `CNAME` → `dist/CNAME`.
8. Inject current year into footer context.

## 6. Deployment Workflow

1. Push to `main`.
2. GitHub Actions (`.github/workflows/deploy.yml`):
   - Checks out repo.
   - Installs uv (`astral-sh/setup-uv`).
   - Runs `just build`.
   - Uploads `dist/` as Pages artifact.
   - Deploys to GitHub Pages environment.
3. DNS `CNAME` for `farhaan.bukh.sh` → `<username>.github.io`.

## 7. Updating Content

- **Talks**: edit `content/talks.md` with standard markdown. Sections, lists, links all supported.
- **Home page**: edit `content/index.md`. YAML frontmatter controls structured data (links with `icon` field, meta, CTAs). Markdown body controls bio prose.
- **Link icons**: each link entry in `content/index.md` has an `icon` field (e.g. `book`, `scroll`, `pickaxe`). The matching SVG lives at `assets/img/icons/<icon>.svg`. Icons are scaled to ~56px in the inventory tray; keep pixel-art style (16×16 source) with `shape-rendering="crispEdges"`.
- **Avatar**: replace `assets/img/avatar.png` (keep square dimensions).
- **Palette**: adjust CSS variables at top of `assets/css/style.css`.
- **Typography**: change `data-font` attribute in `templates/base.html` and corresponding CSS selectors.

## 8. QA Checklist Before Deploy

- [ ] `just build` completes without errors.
- [ ] `just check` passes all smoke tests.
- [ ] `just serve` → visual inspection on mobile (<640px) and desktop.
- [ ] Inventory tray opens on sword-button click, closes on ✕ / ESC / backdrop click.
- [ ] Inventory tray visually matches the wooden crate (brown wood, beveled slots, 4-col desktop / 2-col mobile).
- [ ] All inventory slot icons render as pixelated SVGs with correct links (scaled to ~56px).
- [ ] `dist/talks.html` contains pre-rendered talk content (no loading spinner).
- [ ] All external links open in new tabs where intended.
- [ ] `dist/CNAME` contains `farhaan.bukh.sh`.
- [ ] No `talks.js` or `marked.min.js` references remain in generated HTML.

## 9. Common Agent Tasks

- **Add/update links**: edit the `links` list in `content/index.md`, ensure `icon` matches an SVG in `assets/img/icons/`, run `just build`. Icons display at ~56px inside the wooden inventory tray.
- **Add/update talks**: edit `content/talks.md`, run `just build`, verify `dist/talks.html`.
- **Revise home copy**: edit `content/index.md` frontmatter/body, run `just build`.
- **Tweak colors**: edit CSS variables in `assets/css/style.css`, document in `README.md`.
- **Change typography**: update `data-font` in `templates/base.html` + CSS selectors.
- **Add a new page**: create `content/new.md` + `templates/new.html`, add rendering logic to `build.py`, add nav link to `templates/base.html`.

Keep changesets small and well-documented so future agents can reason about diffs quickly.
