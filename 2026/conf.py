"""
Sphinx configuration for the SciPy India 2026 conference website.

Usage:

Build both sites, and build the main website first:

    uv run sphinx-build -b html docs _build/html
    uv run sphinx-build -b html 2026 _build/html/2026
"""

import os

project = "SciPy India 2026"
html_title = "SciPy India 2026"
copyright = "2026, the SciPy India team"
author = "The SciPy India team"

html_baseurl = "https://scipy.in/2026/"

# Cloudflare Pages handling
site_baseurl = html_baseurl
_cf_url = os.environ.get("CF_PAGES_URL")
if _cf_url and os.environ.get("CF_PAGES_BRANCH") != "main":
    site_baseurl = f"{_cf_url.rstrip('/')}/2026/"

html_theme = "pydata_sphinx_theme"

extensions = [
    "myst_parser",
    "ablog",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinxext.opengraph",
]

# Link previews
ogp_site_url = site_baseurl
ogp_site_name = "SciPy India 2026 Conference"
ogp_type = "website"
# N.B. these need to be PNG (raster) instead of vector because the
# SciPy logo SVG loses the snake during conversion for social cards.
# The card has two logo slots, top right and bottom right, and
# filling both draws the logo twice. There is no way to switch one
# off. An unset image_mini falls back to the Eye of Horus
# which I don't like.
ogp_social_cards = {
    "image": "_static/logo.png",
    "image_mini": "_static/_social-card-blank.png",
    "line_color": "#2b55a1",
}

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
    "site_baseurl": site_baseurl,
    "conference_nav": [
        {"label": "Programme", "page": "programme"},
        {
            "label": "Attend",
            "children": [
                ("register", "Register"),
                ("venue", "Venue and travel"),
                ("jobs", "Jobs"),
                ("faq", "Frequently asked questions (FAQ)"),
            ],
        },
        {"label": "Call for proposals", "page": "cfp"},
        {"label": "Sponsor us", "page": "sponsor"},
        {
            "label": "About",
            "children": [
                ("news/index", "News"),
                ("team", "Team"),
                ("volunteer", "Volunteer"),
                ("coc", "Code of Conduct"),
            ],
            "links": [
                ("https://scipy.in/past-editions", "Past editions"),
                ("https://scipy.in", "scipy.in"),
            ],
        },
    ],
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]
html_show_sourcelink = False

html_sidebars = {
    "index": [],
    "programme": [],
    "cfp": [],
    "jobs": [],
    "register": [],
    "venue": [],
    "sponsor": [],
    "faq": [],
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
            "url": "https://zulip.scipy.in",
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


# sphinx-design's button-link directive has no option for a target
# attribute for a link (how shocking?!) TODO: contribute to add this
# to sphinx-design
def _buttons_open_in_new_tab(app, doctree, docname):
    from docutils import nodes

    for node in doctree.findall(nodes.reference):
        if "sci-new-tab" in node.get("classes", []):
            node["target"] = "_blank"


# sphinxext-opengraph derives its description by walking the body of the page.
# I want to use the html_meta.description for the social card caption instead.
# TODO: this uses sphinxext-opengraph internals, figure out what to do about it...
def _prefer_html_meta_description():
    import sphinxext.opengraph as opengraph
    from docutils import nodes

    if getattr(opengraph.get_description, "_uses_html_meta", False):
        return

    walk_the_page_body = opengraph.get_description

    def get_description(doctree, description_length, known_titles=frozenset()):
        for node in doctree.findall(nodes.Element):
            if node.tagname == "meta" and node.get("name") == "description":
                description = node.get("content", "").strip()
                if description:
                    return description
        return walk_the_page_body(doctree, description_length, known_titles)

    get_description._uses_html_meta = True
    opengraph.get_description = get_description


def setup(app):
    app.connect("doctree-resolved", _buttons_open_in_new_tab)
    _prefer_html_meta_description()
