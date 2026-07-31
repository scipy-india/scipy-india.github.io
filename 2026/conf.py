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
html_context = {
    "conference_nav": [
        {
            "label": "Programme",
            "children": [
                ("programme", "Programme"),
                ("speakers", "Speakers"),
                ("cfp", "Call for proposals"),
            ],
        },
        {
            "label": "Attend",
            "children": [
                ("register", "Register"),
                ("venue", "Venue and travel"),
                ("financial-aid", "Financial aid"),
                ("faq", "FAQ"),
            ],
        },
        {"label": "Sponsor us", "page": "sponsor"},
        {
            "label": "About",
            "children": [
                ("news/index", "News"),
                ("team", "Team"),
                ("get-involved", "Get involved"),
                ("coc", "Code of conduct"),
            ],
            "links": [("https://scipy.in", "scipy.in")],
        },
        {"label": "Past editions", "page": "https://scipy.in/past-editions"},
    ],
}
