# farhaan.bukh.sh — task runner
# Requires: just (https://github.com/casey/just), uv

set dotenv-load := false

# Default recipe: build the site
default: build

# Install Python dependencies via uv
setup:
    uv sync

# Run the Python build script → produces dist/
build: setup
    uv run python build.py

# Serve dist/ locally for preview
serve: build
    @echo "Serving dist/ at http://localhost:5000"
    uv run python -m http.server 5000 --directory dist

# Remove generated output
clean:
    rm -rf dist

# Build + serve in one step
dev: build serve

# Lint / validate (placeholder — expand as needed)
check:
    @echo "Running basic checks…"
    @test -f dist/index.html  && echo "✓ dist/index.html exists" || echo "✗ dist/index.html missing"
    @test -f dist/talks.html  && echo "✓ dist/talks.html exists" || echo "✗ dist/talks.html missing"
    @test -f dist/CNAME       && echo "✓ dist/CNAME exists"      || echo "✗ dist/CNAME missing"
    @test -d dist/assets      && echo "✓ dist/assets/ exists"    || echo "✗ dist/assets/ missing"
