"""
Render a list of past SciPy India conference editions.

The archive URLs are defined once in conf.py's html_context["past_editions"] as a list of
(year, url) tuples, and this directive renders them as an HTML list. I am trying to avoid
the data being duplicated between the footer template and the past-editions page at the cost
of some extra code :D
"""

from docutils import nodes
from docutils.parsers.rst import Directive


class PastEditionsListNode(nodes.General, nodes.Element):
    pass


class PastEditionsList(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = False
    option_spec = {}

    def run(self):
        return [PastEditionsListNode()]


def _resolve(app, doctree, docname):
    for node in doctree.findall(PastEditionsListNode):
        past_editions = app.config.html_context.get("past_editions", [])
        items = "".join(
            f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">'
            f"SciPy India {year}</a></li>"
            for year, url in reversed(past_editions)
        )
        html = f"<ul>{items}</ul>"
        node.replace_self(nodes.raw("", html, format="html"))


def setup(app):
    app.add_node(PastEditionsListNode)
    app.connect("doctree-resolved", _resolve)
    app.add_directive("past-editions-list", PastEditionsList)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
