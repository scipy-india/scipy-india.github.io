# SciPy India Website

[![Netlify Status](https://api.netlify.com/api/v1/badges/f1669f7b-e261-4a1a-aa5e-fd3db25f6833/deploy-status)](https://app.netlify.com/projects/scipy-india/deploys)

This is the source for the SciPy India website. The site is built with Sphinx, the PyData Sphinx Theme, MyST, and ABlog.

Install the project once with:

```bash
uv sync
```

Build the site with:

```bash
uv run sphinx-build -b html docs _build/html
```

If you want to preview the generated files locally:

```bash
python3 -m http.server 8000 -d _build/html
```

Then open `http://localhost:8000`.
