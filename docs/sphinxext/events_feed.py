"""
A Sphinx extension to merge event pages into ABlog's generated Atom feed.

ABlog only feeds blog posts (``docs/blog/*.md``). Our events (``docs/events/**``)
are plain pages, so they never reach ``blog/atom.xml``. We want the feed to also
announce events, while the website keeps showing only blog posts in the blog grid,
sidebar, and archives.

Rather than turning events into ABlog posts (which would leak them into every
on-site listing), this extension post-processes the generated feed on
``build-finished``: it reads each event's frontmatter, builds an Atom ``<entry>``,
and appends it to ``blog/atom.xml``. The on-site display is left untouched.

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


def _merge_events_into_feed(app, exception):
    if exception is not None or app.builder.format != "html":
        return

    blog_path = app.config.blog_path
    baseurl = app.config.blog_baseurl.rstrip("/")
    feed_file = os.path.join(app.outdir, blog_path, "atom.xml")
    if not os.path.exists(feed_file):
        return

    # IST midnight, matching how ABlog stamps blog entries.
    ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(datetime.timezone.utc)

    new_entries = []
    for docname in app.env.found_docs:
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
        url = f"{baseurl}/{docname}.html"
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

    if not new_entries:
        return

    ET.register_namespace("", ATOM)
    tree = ET.parse(feed_file)
    root = tree.getroot()

    # Interleave events with blog posts by date. We leave the feed-level <updated>
    # alone: ABlog sets it to the build time, which is the correct "feed last built"
    # semantic (an upcoming event's date would otherwise push it into the future).
    entries = root.findall(_q("entry")) + new_entries
    for entry in root.findall(_q("entry")):
        root.remove(entry)
    entries.sort(key=_entry_updated, reverse=True)
    for entry in entries:
        root.append(entry)

    tree.write(feed_file, encoding="UTF-8", xml_declaration=True)


def setup(app):
    app.connect("build-finished", _merge_events_into_feed)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
