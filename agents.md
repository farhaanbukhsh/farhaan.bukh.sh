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
│   ├── img/favicon.png
│   ├── img/icons/                 # Pixel-art SVG icons (sword, book, scroll, etc.)
│   │                              # Also backdrop decorations: flower, tnt, axe,
│   │                              # grass-block, creeper, potion, heart, star
│   ├── js/main.js                 # Nav toggle, inventory tray toggle, year stamp
│   └── resume.pdf                 # Resume PDF (copied verbatim into dist/)
├── content/                       # Editable markdown source files
│   ├── index.md                   # Home page data (YAML frontmatter + markdown body)
│   └── talks.md                   # Talks list (pure markdown)
├── templates/                     # Jinja2 HTML templates
│   ├── base.html                  # Shared shell (head, nav, footer, backdrop items)
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
- **Home page**: edit `content/index.md`. YAML frontmatter controls structured data (links with `icon` field). Markdown body controls bio prose. Note: hero CTAs and meta badges were removed; hero is a single stacked column with centered avatar + status chip above the headline.
- **Link icons**: each link entry in `content/index.md` has an `icon` field (e.g. `book`, `scroll`, `pickaxe`). The matching SVG lives at `assets/img/icons/<icon>.svg`. Icons are scaled to ~56px in the inventory tray; keep pixel-art style (16×16 source) with `shape-rendering="crispEdges"`.
- **Avatar**: replace `assets/img/avatar.png` (keep square dimensions).
- **Resume**: replace `assets/resume.pdf`. It is referenced in `templates/base.html`, `templates/talks.html`, and `content/index.md` as `assets/resume.pdf`. Copied verbatim into `dist/assets/` by the build.
- **Palette**: adjust CSS variables at top of `assets/css/style.css`.
- **Backdrop items**: 18 decorative Minecraft pixel-art SVGs are scattered across the page via `.backdrop-items` in `templates/base.html`. Each `<img>` uses a `.backdrop-item--N` class positioned/rotated via CSS custom properties in `assets/css/style.css`. To add/remove items: edit the HTML list in `base.html` and the corresponding `.backdrop-item--N` CSS rule. Items are fixed-position, opacity 0.35 with saturated/brightened filter, with a gentle float animation. 9 of 18 are hidden on mobile (<640px).
- **Inventory button (chocolate bar)**: The "Open Inventory" button is styled as a Minecraft chocolate bar. Dark chocolate body (`#1c1008`) with grid-square pattern, white paper/foil strip (`::before`) across the middle extending beyond edges, pink wrapper (`::after`) covering the bottom 55% with concentric pink/white banding. The whole button wobbles via `@keyframes choco-bob` (±2° rotation, 6px float, 2.5s). On hover: animation pauses, wrapper and foil slide down ~14–18px (stay visible, don't disappear). Label ("Open Inventory") sits on the chocolate face in normal flow. No sword icon — removed.
- **Typography**: change `data-font` attribute in `templates/base.html` and corresponding CSS selectors.

## 8. QA Checklist Before Deploy

- [ ] `just build` completes without errors.
- [ ] `just check` passes all smoke tests.
- [ ] `just serve` → visual inspection on mobile (<640px) and desktop.
- [ ] Inventory tray opens on chocolate-bar button click, closes on ✕ / ESC / backdrop click.
- [ ] Inventory tray visually matches the wooden crate (brown wood, beveled slots, 4-col desktop / 2-col mobile).
- [ ] All inventory slot icons render as pixelated SVGs with correct links (scaled to ~56px).
- [ ] Hero layout: single column, avatar + status centered above headline and paragraph; no CTAs or meta badges.
- [ ] `dist/talks.html` contains pre-rendered talk content (no loading spinner).
- [ ] All external links open in new tabs where intended.
- [ ] `dist/CNAME` contains `farhaan.bukh.sh`.
- [ ] Backdrop items visible as floating Minecraft icons (opacity 0.35, saturated colours) behind content; non-interactive (`pointer-events: none`).
- [ ] Chocolate bar button wobbles, label on brown face, wrapper/foil peek down on hover (don't disappear).
- [ ] No `talks.js` or `marked.min.js` references remain in generated HTML.

## 9. Common Agent Tasks

- **Add/update links**: edit the `links` list in `content/index.md`, ensure `icon` matches an SVG in `assets/img/icons/`, run `just build`. Icons display at ~56px inside the wooden inventory tray.
- **Add/update talks**: edit `content/talks.md`, run `just build`, verify `dist/talks.html`.
- **Revise home copy**: edit `content/index.md` frontmatter/body, run `just build`.
- **Tweak colors**: edit CSS variables in `assets/css/style.css`, document in `README.md`.
- **Change typography**: update `data-font` in `templates/base.html` + CSS selectors.
- **Add a new page**: create `content/new.md` + `templates/new.html`, add rendering logic to `build.py`, add nav link to `templates/base.html`.

Keep changesets small and well-documented so future agents can reason about diffs quickly.
