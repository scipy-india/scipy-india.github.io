"""
Sphinx configuration for the SciPy India 2026 conference website.

Usage:

Build both sites, and build the main website first:

    uv run sphinx-build -b html docs _build/html
    uv run sphinx-build -b html 2026 _build/html/2026
"""

project = "SciPy India 2026 conference"
html_title = "SciPy India 2026 conference"
copyright = "2026, The SciPy India team"
author = "The SciPy India team"

html_baseurl = "https://scipy.in/2026/"

html_theme = "pydata_sphinx_theme"

extensions = [
    "myst_parser",
    "ablog",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_togglebutton",
]

html_static_path = ["_static"]
_FLIPDOWN_CSS = "https://unpkg.com/flipdown@0.3.2/dist/flipdown.min.css"
_FLIPDOWN_JS = "https://unpkg.com/flipdown@0.3.2/dist/flipdown.min.js"

html_css_files = [
    (
        _FLIPDOWN_CSS,
        {
            "integrity": "sha384-tLNTw8PFWNQ932PbvEZ8hKn5NbCSqdc2/ccaGPMLMXw8AtqZuLI5jGGc7zYOqLws",
            "crossorigin": "anonymous",
        },
    ),
    "custom.css",
]
html_js_files = [
    ("team-shuffle.js", {"defer": "defer"}),
    (
        _FLIPDOWN_JS,
        {
            "defer": "defer",
            "integrity": "sha384-ccp31xTym833Bnbsii5mVCA3jaeJubpC5K7F5l6YLrY5fqSB+aTmuBVYvjjf8j2D",
            "crossorigin": "anonymous",
        },
    ),
]
templates_path = ["_templates"]

html_context = {
    "conference_nav": [
        {
            "label": "Programme",
            "children": [
                ("programme", "Programme"),
                ("schedule", "Schedule"),
            ],
        },
        {
            "label": "Attend",
            "children": [
                ("register", "Register"),
                ("venue", "Venue and travel"),
                ("financial-aid", "Financial aid"),
                ("faq", "Frequently asked questions (FAQ)"),
            ],
        },
        {"label": "Sponsor us", "page": "sponsor"},
        {
            "label": "About",
            "children": [
                ("news/index", "News"),
                ("team", "Team"),
                ("volunteer", "Volunteer"),
                ("coc", "Code of conduct"),
            ],
            "links": [("https://scipy.in", "scipy.in")],
        },
        {"label": "Past editions", "page": "https://scipy.in/past-editions"},
    ],
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]
html_show_sourcelink = False

html_sidebars = {
    "index": [],
    "programme": [],
    "schedule": [],
    "cfp": [],
    "register": [],
    "venue": [],
    "sponsor": [],
    "faq": [],
    "financial-aid": [],
    "volunteer": [],
    "coc": [],
    "team": [],
    "news/**": ["ablog/postcard.html", "ablog/recentposts.html", "ablog/tagcloud.html"],
}

myst_enable_extensions = ["colon_fence", "deflist", "attrs_inline"]

html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"

html_theme_options = {
    "logo": {
        "image_light": "_static/logo.svg",
        "image_dark": "_static/logo.svg",
        "alt_text": "SciPy India 2026 logo",
        "text": "SciPy India 2026",
    },
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "navbar_persistent": ["search-button"],
    "footer_start": ["copyright"],
    "footer_end": ["past-editions"],
    "show_prev_next": False,
    "secondary_sidebar_items": ["page-toc"],
    "icon_links": [
        {
            "name": "Email",
            "url": "mailto:info@scipy.in",
            "icon": "fa-solid fa-envelope",
            "type": "fontawesome",
        },
        {
            "name": "News feed",
            "url": "https://scipy.in/2026/news/atom.xml",
            "icon": "fa-solid fa-rss",
            "type": "fontawesome",
        },
        {
            "name": "YouTube",
            "url": "https://www.youtube.com/@scipy-india",
            "icon": "fa-brands fa-youtube",
            "type": "fontawesome",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/scipy-india",
            "icon": "fab fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Zulip",
            "url": "https://scipyindia.zulipchat.com/join/4mesdxfbbpl4titgtdzx4iwv/",
            "icon": "fa-brands fa-zulip",
            "type": "fontawesome",
        },
        {
            "name": "Bluesky",
            "url": "https://bsky.app/profile/scipy.in",
            "icon": "fa-brands fa-bluesky",
            "type": "fontawesome",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/company/scipyindia",
            "icon": "fab fa-linkedin",
            "type": "fontawesome",
        },
    ],
    "use_edit_page_button": False,
    "show_toc_level": 2,
    "navigation_with_keys": True,
    "back_to_top_button": True,
}

# ABlog settings
blog_path = "news"
blog_title = "SciPy India 2026 news"
blog_baseurl = "https://scipy.in/2026"
blog_feed_fulltext = True
blog_post_pattern = "news/*.md"
post_date_format = "%d %B %Y"
