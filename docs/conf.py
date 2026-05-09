project = "SciPy India"
html_title = "SciPy India"
copyright = "2026, The SciPy India team"
author = "The SciPy India team"

html_theme = "pydata_sphinx_theme"

extensions = [
    "myst_parser",
    "ablog",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_togglebutton",
]

html_static_path = ["_static"]
html_extra_path = ["_extra"]
html_css_files = ["custom.css"]
html_js_files = [
    (
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@7.2.0/js/brands.min.js",
        {"defer": "defer"},
    ),
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_show_sourcelink = False

html_sidebars = {
    "index": [],
    "contact": [],
    "coc": [],
    "blog/**": [],
}

myst_enable_extensions = ["colon_fence", "deflist"]

html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"

html_theme_options = {
    "logo": {
        "image_light": "_static/logo.svg",
        "image_dark": "_static/logo.svg",
        "alt_text": "SciPy India logo",
    },
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "footer_start": ["copyright"],
    "footer_end": ["theme-version"],
    "show_prev_next": False,
    "secondary_sidebar_items": ["page-toc"],
    "icon_links": [
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
            "url": "https://bsky.app/profile/scipyindia.bsky.social",
            "icon": "fa-brands fa-bluesky",
            "type": "fontawesome",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/company/scipyindia",
            "icon": "fab fa-linkedin",
            "type": "fontawesome",
        },
        {
            "name": "Mastodon",
            "url": "https://fosstodon.org/@scipyindia",
            "icon": "fab fa-mastodon",
            "type": "fontawesome",
        },
    ],
    "use_edit_page_button": False,
    "show_toc_level": 2,
    "navigation_with_keys": True,
    "back_to_top_button": True,
}

# ABlog settings
blog_path = "blog"
blog_title = "SciPy India Blog"
blog_baseurl = "https://scipy.in"
blog_feed_fulltext = True
blog_post_pattern = "blog/*.md"
