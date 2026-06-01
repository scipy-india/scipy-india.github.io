import sys
import os

# Path for our custom Sphinx extensions
sys.path.insert(0, os.path.abspath("sphinxext"))


def convert_to_markdown(text):
    """Convert inline markdown to HTML for use in Jinja templates"""
    from markdown_it import MarkdownIt

    rendered = MarkdownIt().render(text).strip()
    if rendered.startswith("<p>") and rendered.endswith("</p>"):
        return rendered[3:-4]
    return rendered

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
    "blog_post_grid",
    "past_editions_list",
]

html_context = {
    "past_editions": [
        (2009, "https://web.archive.org/web/20251016230532/https://scipy.in/2009"),
        (2010, "https://web.archive.org/web/20251016212905/https://scipy.in/scipyin/2010/"),
        (2011, "https://web.archive.org/web/20250806175159/https://scipy.in/scipyin/2011/"),
        (2012, "https://web.archive.org/web/20260316083619/https://scipy.in/2012"),
        (2013, "https://web.archive.org/web/20250806185218/https://scipy.in/2013/"),
        (2014, "https://web.archive.org/web/20250820081400/https://scipy.in/2014"),
        (2015, "https://web.archive.org/web/20250716160805/https://scipy.in/2015"),
        (2016, "https://web.archive.org/web/20250903154429/http://scipy.in/2016"),
        (2017, "https://web.archive.org/web/20260208082549/https://scipy.in/2017"),
        (2018, "https://web.archive.org/web/20251207222647/https://scipy.in/2018"),
        (2019, "https://web.archive.org/web/20260125032611/https://scipy.in/2019"),
        (2020, "https://web.archive.org/web/20250903153752/https://scipy.in/2020"),
        (2021, "https://web.archive.org/web/20260316083156/scipy.in/2021"),
    ],
    "partners": [
        {
            "url": "https://www.python.org/psf",
            "logo": "_static/partner-logos/psf.svg",
            "logo_alt": "Python Software Foundation",
            "logo_style": "width: 264px; height: 100px",
            "description": convert_to_markdown(
                "SciPy India is an [official community partner](https://www.python.org/psf/community-partners/)"
                " of the Python Software Foundation."
            ),
        },
        {
            "url": "https://fossunited.org/c/scipy-india",
            "logo_light": "_static/partner-logos/fossunited-dark.svg",
            "logo_dark": "_static/partner-logos/fossunited-light.svg",
            "logo_alt": "FOSS United Foundation",
            "logo_style": "height: 100px",
            "description": convert_to_markdown(
                "We are incubated and supported by [the FOSS United Foundation](https://fossunited.org),"
                " a Section 8 non-profit organisation that aims to promote and strengthen the Free and Open"
                " Source Software (FOSS) ecosystem in India."
            ),
        },
        {
            "full_width": True,
            "logos": [
                {
                    "src": "_static/partner-logos/fossee.svg",
                    "alt": "FOSSEE",
                    "href": "https://fossee.in",
                    "style": "width: 200px",
                },
                {
                    "src": "_static/partner-logos/iitb.svg",
                    "alt": "IIT Bombay",
                    "href": "https://www.iitb.ac.in",
                    "style": "width: 200px",
                },
            ],
            "description": convert_to_markdown(
                "The [FOSSEE project](https://fossee.in) at the Indian Institute of Technology, Bombay offers"
                " hosting for our website domain."
                " [The Indian Institute of Technology, Bombay](https://www.iitb.ac.in) previously hosted"
                " several editions of the conference from 2009 to 2021."
            ),
        },
    ],
}

html_static_path = ["_static"]
# Files in _extra/ are copied after the build and overwrite any generated files
# with the same name. _extra/blog.html replaces ABlog's "All Posts" page with a
# redirect to blog/index.html to keep a single canonical blog listing page.
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
    "about": [],
    "past-editions": [],
    "coc": [],
    "blog": [],
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

# Add post descriptions to the blog post grid context, because
# ABlog doesn't do this by default.
def _add_post_descriptions(app, _pagename, _templatename, context, _doctree):
    from ablog.blog import Blog

    blog = Blog(app)
    context["post_descriptions"] = {
        post.docname: app.env.metadata.get(post.docname, {}).get("description", "")
        for post in blog.posts
    }


def setup(app):
    app.connect("html-page-context", _add_post_descriptions)
