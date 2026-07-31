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
