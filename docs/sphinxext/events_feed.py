"""
A Sphinx extension that builds a site-wide Atom feed from blog posts and events.

ABlog generates a blog-only feed at ``blog/atom.xml`` (driven by ``docs/blog/*.md``
posts). Our events (``docs/events/**``) are plain pages, so they never reach that
feed. We want a single feed that announces both, without changing what the website
shows: the blog grid, sidebar, and archives stay blog-only.

So this extension leaves ``blog/atom.xml`` untouched as the internal blog feed, and on
``build-finished`` derives a combined site feed at the site root ``atom.xml``: it reads
ABlog's generated blog feed, builds an Atom ``<entry>`` for each eligible event, and
writes the merged result to ``atom.xml``. The blog-only feed is never advertised; pages
point to the site feed instead (see ``_use_site_feed_link`` below).

Convention: an event page is in the feed when it has a ``date`` in its frontmatter.
Set ``feed: false`` to keep one out. Use that on event stubs that mirror a blog
post (so the event doesn't show twice) and on placeholder pages whose date is TBA.

Each event entry carries ``<published>`` set to the event date, and ``<updated>``
clamped to the build time so an upcoming event never lands a future timestamp in the
feed. Entries are sorted by ``<updated>``, which keeps past events in date order and
pins an upcoming event to the top until it happens.
"""

import datetime
import os
from xml.etree import ElementTree as ET

import yaml

ATOM = "http://www.w3.org/2005/Atom"


def _q(tag):
    return f"{{{ATOM}}}{tag}"


def _read_frontmatter(path):
    """Return the YAML frontmatter of a markdown file as a dict (empty if none)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else {}


def _as_date(value):
    """Coerce a frontmatter date value to a datetime.date, or None."""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value.strip()[:10])
        except ValueError:
            return None
    return None


def _entry_updated(entry):
    """Parse an entry's <updated> text into a datetime for sorting."""
    el = entry.find(_q("updated"))
    try:
        return datetime.datetime.fromisoformat(el.text)
    except (AttributeError, ValueError):
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


def _entry_sort_key(entry):
    """Sort by <updated>, then <id>, so ties (e.g. upcoming events clamped to the
    build time) stay in a stable, reproducible order across builds."""
    return (_entry_updated(entry), entry.findtext(_q("id")) or "")


def _use_site_feed_link(app, pagename, templatename, context, doctree):
    """Point pages at the site feed instead of ABlog's blog-only feed.

    ABlog's ``page.html`` renders the ``<link rel="alternate">`` from ``feed_path``,
    which defaults to ``blog/atom.xml``. Blanking it suppresses that link; our
    ``layout.html`` adds the site-wide ``atom.xml`` link in its place, so every page
    advertises exactly one feed. Registered to run after ABlog's context handler.
    """
    context["feed_path"] = ""
    context["feed_title"] = ""


def _build_site_feed(app, exception):
    if exception is not None or app.builder.format != "html":
        return

    blog_path = app.config.blog_path
    baseurl = app.config.blog_baseurl.rstrip("/")
    blog_feed = os.path.join(app.outdir, blog_path, "atom.xml")
    site_feed = os.path.join(app.outdir, "atom.xml")
    if not os.path.exists(blog_feed):
        return

    # IST midnight, matching how ABlog stamps blog entries.
    ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(datetime.timezone.utc)

    # found_docs is a set, so sort it for a deterministic build order.
    new_entries = []
    for docname in sorted(app.env.found_docs):
        if not docname.startswith("events/") or docname == "events/index":
            continue

        fm = _read_frontmatter(app.env.doc2path(docname))
        if fm.get("feed") is False:
            continue

        date = _as_date(fm.get("date"))
        if date is None:
            continue

        title_node = app.env.titles.get(docname)
        title = title_node.astext() if title_node else docname
        summary = fm.get("description") or fm.get("summary") or title
        # Use the builder's target URI so links track Sphinx URL config
        # (html_file_suffix, directory-style URLs) instead of a hardcoded .html.
        url = f"{baseurl}/{app.builder.get_target_uri(docname)}"
        published = datetime.datetime.combine(date, datetime.time(0, 0, tzinfo=ist))
        # <updated> means "entry last modified", so never let an upcoming event put a
        # future timestamp in the feed. The event date lives in <published>.
        updated = min(published, now)

        entry = ET.Element(_q("entry"))
        ET.SubElement(entry, _q("id")).text = url
        ET.SubElement(entry, _q("title")).text = title
        ET.SubElement(entry, _q("published")).text = published.isoformat()
        ET.SubElement(entry, _q("updated")).text = updated.isoformat()
        ET.SubElement(entry, _q("link")).set("href", url)
        ET.SubElement(entry, _q("summary")).text = summary
        new_entries.append(entry)

    ET.register_namespace("", ATOM)
    # Read ABlog's blog feed, but write the combined result to atom.xml so the
    # blog-only feed stays intact.
    tree = ET.parse(blog_feed)
    root = tree.getroot()

    # Present the root feed as the SciPy India site feed, not "SciPy India Blog":
    # retitle it and repoint the self link at atom.xml.
    title_el = root.find(_q("title"))
    if title_el is not None:
        title_el.text = app.config.project
    for link in root.findall(_q("link")):
        if link.get("rel") == "self":
            link.set("href", f"{baseurl}/atom.xml")

    # Skip events already in the feed, so a partial rebuild can't duplicate entries.
    existing = root.findall(_q("entry"))
    existing_ids = {e.findtext(_q("id")) for e in existing}
    new_entries = [e for e in new_entries if e.findtext(_q("id")) not in existing_ids]

    # Interleave events with blog posts by date. We leave the feed-level <updated>
    # alone: ABlog sets it to the build time, which is the correct "feed last built"
    # semantic (an upcoming event's date would otherwise push it into the future).
    entries = existing + new_entries
    for entry in existing:
        root.remove(entry)
    entries.sort(key=_entry_sort_key, reverse=True)
    for entry in entries:
        root.append(entry)

    tree.write(site_feed, encoding="UTF-8", xml_declaration=True)


def setup(app):
    # Priority 900 so this runs after ABlog's html-page-context handler (which sets
    # feed_path) and can override it.
    app.connect("html-page-context", _use_site_feed_link, priority=900)
    app.connect("build-finished", _build_site_feed)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
