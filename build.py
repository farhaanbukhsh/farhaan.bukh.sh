"""
build.py — Static site generator for farhaan.bukh.sh

Reads markdown content from content/, renders Jinja2 templates from templates/,
and writes final HTML + static assets to dist/.
"""

import shutil
from datetime import datetime
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
DIST_DIR = ROOT / "dist"
CNAME_FILE = ROOT / "CNAME"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body."""
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body.strip()
    return {}, text


def render_markdown(text: str) -> str:
    """Convert markdown text to HTML."""
    return markdown.markdown(text, extensions=["extra", "sane_lists"])


def clean_dist():
    """Remove and recreate dist/."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)


def copy_static():
    """Copy assets/ and CNAME into dist/."""
    shutil.copytree(ASSETS_DIR, DIST_DIR / "assets")
    if CNAME_FILE.exists():
        shutil.copy2(CNAME_FILE, DIST_DIR / "CNAME")


def build():
    print("Building site…")

    clean_dist()

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
    current_year = datetime.now().year

    # --- index.html ---
    index_raw = (CONTENT_DIR / "index.md").read_text()
    index_data, index_body = parse_frontmatter(index_raw)

    # If bio is in frontmatter, use it; otherwise fall back to body
    bio = index_data.get("bio", index_body).strip()

    index_template = env.get_template("index.html")
    index_html = index_template.render(
        year=current_year,
        title=index_data.get("title", "Farhaan Bukhsh"),
        description=index_data.get("description", ""),
        status_chip=index_data.get("status_chip", ""),
        eyebrow=index_data.get("eyebrow", ""),
        eyebrow_sub=index_data.get("eyebrow_sub", ""),
        headline=index_data.get("headline", ""),
        bio=bio,
        cta=index_data.get("cta", []),
        meta=index_data.get("meta", []),
        links_eyebrow=index_data.get("links_eyebrow", ""),
        links_heading=index_data.get("links_heading", ""),
        links_sub=index_data.get("links_sub", ""),
        links=index_data.get("links", []),
        talks_preview_eyebrow=index_data.get("talks_preview_eyebrow", ""),
        talks_preview_heading=index_data.get("talks_preview_heading", ""),
        talks_preview_sub=index_data.get("talks_preview_sub", ""),
    )
    (DIST_DIR / "index.html").write_text(index_html)
    print("  ✓ dist/index.html")

    # --- talks.html ---
    talks_raw = (CONTENT_DIR / "talks.md").read_text()
    talks_html_content = render_markdown(talks_raw)

    talks_template = env.get_template("talks.html")
    talks_html = talks_template.render(
        year=current_year,
        title="Talks · Farhaan Bukhsh",
        description="Talks and presentations by Farhaan Bukhsh.",
        talks_html=talks_html_content,
    )
    (DIST_DIR / "talks.html").write_text(talks_html)
    print("  ✓ dist/talks.html")

    # --- static assets ---
    copy_static()
    print("  ✓ dist/assets/")
    print("  ✓ dist/CNAME")

    print("Done.")


if __name__ == "__main__":
    build()
