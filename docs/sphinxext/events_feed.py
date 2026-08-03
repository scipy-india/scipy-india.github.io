"""
A Sphinx extension that builds a site-wide Atom feed from blog posts and events.

ABlog generates a blog-only feed at ``blog/atom.xml`` (driven by ``docs/blog/*.md``
posts). Our events are sections on ``docs/events/index.md``, so they never reach that
feed. We want a single feed that announces both, without changing what the website
shows: the blog grid, sidebar, and archives stay blog-only.

So this extension leaves ``blog/atom.xml`` untouched as the internal blog feed, and on
``build-finished`` derives a combined site feed at the site root ``atom.xml``: it reads
ABlog's generated blog feed, builds an Atom ``<entry>`` for each eligible event, and
writes the merged result to ``atom.xml``. The blog-only feed is never advertised; pages
point to the site feed instead (see ``_use_site_feed_link`` below).

An event is a section on ``docs/events/index.md`` with a paragraph, as a direct
child, whose text starts with the calendar emoji. The date comes from that
paragraph, reading only the text before the first bullet separator, and a date range
uses its first day. The summary is the next paragraph, and the entry links to the
section's anchor.

A section whose meta line has no parseable date is skipped, and the build logs a
warning naming the section.

A section that links to a post under ``blog_path`` is also skipped, because the post
is in the feed already. Adding a recap link to a past event replaces its event entry
with the blog entry.

Each event entry carries ``<published>`` set to the event date, and ``<updated>``
clamped to the build time so an upcoming event never lands a future timestamp in the
feed. Entries are sorted by ``<updated>``, which keeps past events in date order and
pins an upcoming event to the top until it happens.
"""

import datetime
import os
import re
from xml.etree import ElementTree as ET

from docutils import nodes
from sphinx.util import logging as sphinx_logging

logger = sphinx_logging.getLogger(__name__)

ATOM = "http://www.w3.org/2005/Atom"

# The only page scanned for event sections.
EVENTS_DOC = "events/index"

# Every event's meta line starts with this.
CALENDAR = "\N{CALENDAR}"

# Separates the date from the location on a meta line.
BULLET = "\N{BULLET}"

# A day, an optional second day for a range, a month name, and a year. The captured
# day is the first one, which is when the event starts.
DATE_RE = re.compile(
    r"(?P<day>\d{1,2})\s*(?:[-‐-―]\s*\d{1,2}\s*)?"
    r"(?P<month>[A-Za-z]{3,})\s+(?P<year>\d{4})"
)


def _q(tag):
    return f"{{{ATOM}}}{tag}"


def _parse_meta_date(text):
    """Return the start date from an event meta line, or None if there isn't one."""
    # Only the text before the first bullet, which leaves out any time range.
    match = DATE_RE.search(text.split(BULLET)[0])
    if match is None:
        return None
    for month_format in ("%b", "%B"):
        try:
            month = datetime.datetime.strptime(match["month"][:3], month_format).month
        except ValueError:
            continue
        try:
            return datetime.date(int(match["year"]), month, int(match["day"]))
        except ValueError:
            return None
    return None


def _links_to_blog(section, blog_path):
    """True when the section links to a blog post.

    Doctrees read back from the environment still hold unresolved ``pending_xref``
    nodes for internal links, so both those and plain references are checked.
    """
    prefix = f"{blog_path}/"
    # Element, because the default also yields Text nodes, which have no attributes.
    for node in section.findall(nodes.Element):
        target = node.get("reftarget") or node.get("refuri") or ""
        if not isinstance(target, str):
            continue
        normalised = target.lstrip("./")
        if normalised.startswith(prefix) or f"/{prefix}" in target:
            return True
    return False


def _iter_events(doctree):
    """Yield (section, meta paragraph, paragraphs) for every event section."""
    for section in doctree.findall(nodes.section):
        # Direct children only, so an enclosing section does not match on a meta
        # line further down the tree.
        paragraphs = [c for c in section.children if isinstance(c, nodes.paragraph)]
        meta = next(
            (p for p in paragraphs if p.astext().lstrip().startswith(CALENDAR)), None
        )
        if meta is not None:
            yield section, meta, paragraphs


def _collect_events(app, blog_path):
    """Return (date, title, anchor, summary) for each event to announce."""
    if EVENTS_DOC not in app.env.found_docs:
        return []

    collected = []
    for section, meta, paragraphs in _iter_events(app.env.get_doctree(EVENTS_DOC)):
        title_node = section.next_node(nodes.title)
        title = title_node.astext() if title_node else ""

        date = _parse_meta_date(meta.astext())
        if date is None:
            logger.warning(
                "no date found in the meta line for event %r on %s, so it is not in "
                "the feed: %r",
                title,
                EVENTS_DOC,
                meta.astext()[:80],
                location=EVENTS_DOC,
            )
            continue

        if _links_to_blog(section, blog_path):
            continue

        body = next((p for p in paragraphs if p is not meta), None)
        anchor = section["ids"][0] if section["ids"] else ""
        collected.append((date, title, anchor, body.astext() if body else title))
    return collected


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

    # Use the builder's target URI so links track Sphinx URL config
    # (html_file_suffix, directory-style URLs) instead of a hardcoded .html.
    events_url = f"{baseurl}/{app.builder.get_target_uri(EVENTS_DOC)}"

    new_entries = []
    # Sort for a deterministic build order, oldest first.
    for date, title, anchor, summary in sorted(_collect_events(app, blog_path)):
        url = f"{events_url}#{anchor}" if anchor else events_url
        published = datetime.datetime.combine(date, datetime.time(0, 0, tzinfo=ist))
        # <updated> means "entry last modified", so never let an upcoming event put a
        # future timestamp in the feed. The event date goes in <published>.
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
