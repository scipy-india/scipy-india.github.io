"""
A Sphinx extension to render a grid of blog posts on the blog index page.

We override ABlog's default grid body template to include an extra description field,
which we populate from the blog posts' frontmatter metadata.

This extension defines a custom directive `blog-post-grid`, which can be used in the blog
index page to render the grid of blog posts. The directive is implemented using a custom
node `BlogPostGridNode`, which is resolved during the `doctree-resolved` event to render
the HTML for the grid using a custom template `blog_post_grid_body.html`.

Maybe we can contribute this back to ABlog at some point if we think it's generally useful!
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from ablog import anchor


class BlogPostGridNode(nodes.General, nodes.Element):
    pass


class BlogPostGrid(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = False
    option_spec = {}

    def run(self):
        return [BlogPostGridNode()]


def _resolve(app, doctree, docname):
    from ablog.blog import Blog

    for node in doctree.findall(BlogPostGridNode):
        blog = Blog(app)
        collection = sorted(blog.posts._posts.values(), reverse=True)
        post_descriptions = {
            post.docname: app.env.metadata.get(post.docname, {}).get("description", "")
            for post in collection
        }
        context = {
            "ablog": blog,
            "fa": blog.fontawesome,
            "pathto": lambda target, mode=0: app.builder.get_relative_uri(
                docname, target
            ),
            "anchor": anchor,
            "collection": collection,
            "post_descriptions": post_descriptions,
            "pagename": docname,
            "_": lambda x: x,
        }
        html = app.builder.templates.render("blog_post_grid_body.html", context)
        node.replace_self(nodes.raw("", html, format="html"))


def setup(app):
    app.add_node(BlogPostGridNode)
    app.connect("doctree-resolved", _resolve)
    app.add_directive("blog-post-grid", BlogPostGrid)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
