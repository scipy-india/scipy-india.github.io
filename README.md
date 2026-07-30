# SciPy India Website

[![Deployed on Cloudflare Pages](https://img.shields.io/badge/Cloudflare%20Pages-deployed-F38020?logo=cloudflarepages&logoColor=white)](https://scipy.in)

This is the source for the SciPy India website. The site is built with Sphinx, the PyData Sphinx Theme, MyST, and ABlog.

There are two Sphinx projects in this repository:

| Source  | Output              | Served at         |
| ------- | ------------------- | ----------------- |
| `docs/` | `_build/html`       | `scipy.in`        |
| `2026/` | `_build/html/2026`  | `scipy.in/2026`   |

`2026/` is the website for the 2026 edition of the conference.

Install the project once with:

```bash
uv sync
```

Build the websites with:

```bash
uv run sphinx-build -b html docs _build/html
uv run sphinx-build -b html 2026 _build/html/2026
```

If you want to preview the generated files locally:

```bash
python3 -m http.server 8000 -d _build/html
```

Then open `http://localhost:8000`.
