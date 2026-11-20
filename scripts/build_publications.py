#!/usr/bin/env python3
"""
Builds the publication lists of the website from the .bib files.

It runs automatically before every `quarto render` / `quarto preview`
(see `pre-render` in _quarto.yml). No extra packages are needed.

  publications/preprints.bib    -> Preprints (shown first)
  publications/articles.bib     -> Peer-reviewed publications
  publications/books.bib        -> Books and book chapters
  publications/conferences.bib  -> Conference contributions
  publications/outreach.bib     -> Technical and outreach articles
  (all written to publications/_publications.md)

Entries are numbered and sorted by year (newest first).
Sections with no entries are hidden automatically.
Optional fields per entry:
  doi  -> shown as "DOI: ..." (click opens the article)
  url  -> link icon (if there is no DOI)
  pdf  -> PDF icon, e.g.  pdf = {files/pdfs/calderon2013.pdf}
          (or simply save the PDF as files/pdfs/<section>/<entry key>.pdf,
           sections: preprints, articles, books, conferences, outreach)
  code, data -> extra small links
"""
import html
import re
from pathlib import Path

# Italics in titles: mark them yourself in the .bib with <i>...</i>
# (\textit{...} and \emph{...} from Zotero also work).
# Optional: words to put in italics automatically everywhere (empty = none).
ITALIC_TERMS = []

# Labels for conference presentations (field "presentation" in conferences.bib)
PRESENTATION = {
    "oral": "Oral presentation", "op": "Oral presentation",
    "poster": "Poster", "pp": "Poster",
    "invited": "Invited talk", "ip": "Invited talk",
}

# Name(s) to highlight in bold in the author lists
HIGHLIGHT = ["Calderón, R.", "Calderón Madrid, R."]

ROOT = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT / "publications"
SECTIONS = [
    # (bib file, section title, short label for the top menu, Bootstrap icon)
    ("preprints", "Preprints", "Preprints", "bi-hourglass-split"),
    ("articles", "Peer-reviewed Publications", "Peer-reviewed", "bi-journal-text"),
    ("books", "Books and Book Chapters", "Books", "bi-book"),
    ("conferences", "Conference Contributions", "Conferences", "bi-mic"),
    ("outreach", "Technical and Outreach Articles", "Technical & Outreach", "bi-megaphone"),
]

# --- LaTeX accents that Zotero may write in .bib files ---------------------
ACCENTS = {
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú", "n": "ń", "c": "ć", "y": "ý"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù", "A": "À", "E": "È", "O": "Ò"},
    '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü", "A": "Ä", "O": "Ö", "U": "Ü"},
    "~": {"n": "ñ", "N": "Ñ", "a": "ã", "o": "õ"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"},
    "c": {"c": "ç", "C": "Ç"},
}


def delatex(s: str) -> str:
    s = s.replace("\\i", "i")
    for cmd, table in ACCENTS.items():
        for base, rep in table.items():
            for pat in (f"{{\\{cmd}{{{base}}}}}", f"{{\\{cmd}{base}}}", f"\\{cmd}{{{base}}}", f"\\{cmd}{base}"):
                s = s.replace(pat, rep)
    s = s.replace("\\&", "&").replace("--", "–").replace("\\_", "_").replace("\\%", "%")
    s = re.sub(r"\\textit\{([^{}]*)\}|\\emph\{([^{}]*)\}", lambda m: m.group(1) or m.group(2), s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def parse_bib(text: str):
    """Minimal BibTeX parser (handles nested braces and quoted values)."""
    entries, i, n = [], 0, len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text[at:])
        if not m:
            i = at + 1
            continue
        etype, key = m.group(1).lower(), m.group(2)
        if etype in ("comment", "preamble", "string"):
            i = at + 1
            continue
        j, depth = at + m.end(), 1
        fields = {}
        while j < n and depth > 0:
            fm = re.match(r"\s*([\w-]+)\s*=\s*", text[j:])
            if not fm:
                if text[j] == "}":
                    depth -= 1
                j += 1
                continue
            name = fm.group(1).lower()
            j += fm.end()
            if text[j] == "{":
                d, k = 1, j + 1
                while k < n and d:
                    d += {"{": 1, "}": -1}.get(text[k], 0)
                    k += 1
                value, j = text[j + 1:k - 1], k
            elif text[j] == '"':
                k = text.index('"', j + 1)
                value, j = text[j + 1:k], k + 1
            else:
                vm = re.match(r"[^,}]+", text[j:])
                value, j = vm.group(0).strip(), j + vm.end()
            fields[name] = value
            sep = re.match(r"\s*,?", text[j:])
            j += sep.end()
            if j < n and text[j] == "}":
                depth = 0
                j += 1
        fields["_type"], fields["_key"] = etype, key
        entries.append(fields)
        i = j
    return entries


def fmt_author(a: str) -> str:
    a = delatex(a)
    if "," in a:
        last, first = [p.strip() for p in a.split(",", 1)]
    else:
        parts = a.split()
        last, first = parts[-1], " ".join(parts[:-1])
    initials = " ".join(
        "-".join(p[0] + "." for p in w.split("-") if p) for w in first.replace(".", ". ").split() if w and w[0].isalpha()
    )
    return f"{last}, {initials}".strip(", ")


def fmt_authors(raw: str, presenter: str = "") -> str:
    names = [("et al." if a.strip().lower() == "others" else fmt_author(a))
             for a in re.split(r"\s+and\s+", raw) if a.strip()]
    pres = fmt_author(presenter).replace(" ", "") if presenter.strip() else ""
    out = []
    for name in names:
        h = html.escape(name)
        if pres and name.replace(" ", "") == pres:
            h += '<sup class="presenter" title="Presenting author">*</sup>'
        if any(name.replace(" ", "") == x.replace(" ", "") for x in HIGHLIGHT):
            h = f'<span class="me">{h}</span>'
        out.append(h)
    return ", ".join(out)


def field(e, k):
    return html.escape(delatex(e.get(k, "")))


def venue(e) -> str:
    t = e["_type"]
    if t == "article":
        v = field(e, "journal")
        if e.get("volume"):
            v += f", Vol. {field(e, 'volume')}"
            if e.get("number"):
                v += f"({field(e, 'number')})"
        elif e.get("number"):
            v += f", nº {field(e, 'number')}"
        if e.get("date"):  # issue date, e.g. "Diciembre 2018"
            v += f" / {field(e, 'date')}" if e.get("number") and not e.get("volume") else f", {field(e, 'date')}"
        if e.get("pages"):
            v += f", {field(e, 'pages')}"
        return v
    if t in ("incollection", "inbook"):
        v = ""
        if e.get("editor"):
            v += f"In: {fmt_authors(e['editor'])} (Eds.), "
        v += f"<em>{fmt_title(e.get('booktitle', ''))}</em>"
        for k in ("publisher", "address"):
            if e.get(k):
                v += f". {field(e, k)}"
        if e.get("pages"):
            v += f", pp. {field(e, 'pages')}"
        return v
    if t == "book":
        parts = [field(e, k) for k in ("publisher", "address") if e.get(k)]
        if e.get("isbn"):
            parts.append(f"ISBN: {field(e, 'isbn')}")
        return ". ".join(parts)
    if t in ("misc", "unpublished", "online") or e.get("_section") == "preprints":
        server = field(e, "publisher") or field(e, "howpublished") or field(e, "journal")
        return f"Preprint{(' at ' + server) if server else ''}"
    # conferences and anything else
    parts = [fmt_title(e.get("booktitle", "")) or field(e, "publisher") or field(e, "journal")]
    parts += [field(e, k) for k in ("address", "date") if e.get(k)]
    return ", ".join(p for p in parts if p)


def links(e) -> str:
    out = []
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", e.get("doi", "").strip())
    target = f"https://doi.org/{doi}" if doi else e.get("url", "").strip()
    if doi:
        out.append(f'<span class="pub-doi">DOI: <a href="{html.escape(target)}">{html.escape(doi)}</a></span>')
    icons = []
    if target and not doi:  # link icon only when there is no DOI
        icons.append(f'<a class="pub-icon" href="{html.escape(target)}" title="Go to the publication"><i class="bi bi-link-45deg"></i></a>')
    # PDF: "pdf" field in the .bib, or a file named after the entry key: files/pdfs/<key>.pdf
    # PDF: "pdf" field, or files/pdfs/<section>/<key>.pdf  (e.g. files/pdfs/conferences/calderon2024nasa.pdf)
    pdf = e.get("pdf", "").strip()
    if not pdf:
        for folder in (f"files/pdfs/{e['_section']}", "files/pdfs"):
            if (ROOT / folder / f"{e['_key']}.pdf").exists():
                pdf = f"{folder}/{e['_key']}.pdf"
                break
    if pdf:
        icons.append(f'<a class="pub-icon pdf" href="{html.escape(pdf)}" target="_blank" title="Open PDF"><i class="bi bi-file-earmark-pdf-fill"></i></a>')
    if e.get("code"):
        icons.append(f'<a class="pub-extra" href="{html.escape(e["code"].strip())}" title="Code"><i class="bi bi-github"></i> Code</a>')
    if e.get("data"):
        icons.append(f'<a class="pub-extra" href="{html.escape(e["data"].strip())}" title="Data"><i class="bi bi-database"></i> Data</a>')
    return " ".join(out + icons)


def fmt_title(raw: str) -> str:
    """Title with italics: \\textit{}, \\emph{}, <i>, <em> and ITALIC_TERMS."""
    t = raw
    t = re.sub(r"\\(?:textit|emph)\{((?:[^{}]|\{[^{}]*\})*)\}", lambda m: "\x01" + m.group(1) + "\x02", t)
    t = re.sub(r"\{\\(?:em|it)\s+([^{}]*)\}", lambda m: "\x01" + m.group(1) + "\x02", t)
    t = re.sub(r"<(?:i|em)>(.*?)</(?:i|em)>", lambda m: "\x01" + m.group(1) + "\x02", t, flags=re.I)
    t = html.escape(delatex(t))
    for term in ITALIC_TERMS:
        t = re.sub(r"(?<![\w\x01])(" + re.escape(term) + r")(?![\w\x02])", "\x01\\1\x02", t, flags=re.I)
    # remove nested markers created by overlapping terms
    t = re.sub(r"\x01([^\x01\x02]*)\x01([^\x02]*)\x02([^\x02]*)\x02", "\x01\\1\\2\\3\x02", t)
    t = t.replace("\x02\x01", "")  # join split italics, e.g. {\emph{Xylella}}{\emph{ fastidiosa}}
    return t.replace("\x01", "<em>").replace("\x02", "</em>")


def entry_html(e) -> str:
    year = field(e, "year") or "In press"
    title = fmt_title(e.get("title", ""))
    if e["_type"] == "book":
        title = f"<em>{title}</em>"
    v = venue(e)
    ptype = PRESENTATION.get(e.get("presentation", "").strip().lower(), e.get("presentation", "").strip())
    badge = f' <span class="pub-type">{html.escape(ptype)}</span>' if ptype else ""
    authors = fmt_authors(e.get("author", "") or e.get("editor", ""), e.get("presenter", "")).rstrip(".")
    text = f'<strong>{year}</strong>. {authors}. <span class="pub-title">{title}</span>.{badge}'
    if v:
        text += f" {v}."
    l = links(e)
    if l:
        text += f" {l}"
    text = text.replace('.</span>. <span class="pub-title">', '.</span> <span class="pub-title">')
    return f"<li>{text}</li>"


def load(name: str):
    bib = PUB_DIR / f"{name}.bib"
    text = bib.read_text(encoding="utf-8") if bib.exists() else ""
    # ignore commented lines (starting with %)
    text = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("%"))
    entries = parse_bib(text)
    for idx, e in enumerate(entries):
        e["_order"] = idx
        e["_section"] = name
    entries.sort(key=lambda e: (-int(re.sub(r"\D", "", e.get("year", "0")) or 0), e["_order"]))
    return entries


def metrics_html() -> str:
    """Citation metrics from publications/metrics.yml (simple 'key: value' lines)."""
    f = PUB_DIR / "metrics.yml"
    if not f.exists():
        return ""
    m = {}
    for line in f.read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            m[k.strip()] = v.strip()
    items = [("h_index", "h-index", "bi-graph-up-arrow"), ("citations", "Citations", "bi-quote"),
             ("documents", "Documents", "bi-files")]
    cards = "".join(
        f'<div class="metric"><i class="bi {icon}"></i><span class="metric-num">{html.escape(m[k])}</span>'
        f'<span class="metric-label">{label}</span></div>'
        for k, label, icon in items if m.get(k)
    )
    if not cards:
        return ""
    src = html.escape(m.get("source", ""))
    if m.get("url"):
        src = f'<a href="{html.escape(m["url"])}">{src}</a>'
    upd = f" · updated {html.escape(m['updated'])}" if m.get("updated") else ""
    return f'<div class="metrics">{cards}</div><p class="metrics-source">Source: {src}{upd}</p>'


def build() -> dict:
    data = {name: load(name) for name, _, _, _ in SECTIONS}
    present = [(n, t, s, i) for n, t, s, i in SECTIONS if data[n]]
    lines = ["```{=html}"]
    cards = "".join(
        f'<a class="pub-card" href="#pub-{n}"><i class="bi {i}"></i>'
        f'<span class="pub-card-num">{len(data[n])}</span><span class="pub-card-label">{s}</span></a>'
        for n, _, s, i in present
    )
    lines.append(metrics_html())
    lines.append(f'<nav class="pub-nav">{cards}</nav>')
    for name, title, _, _ in present:
        entries = data[name]
        lines.append(f'<h2 id="pub-{name}" class="pub-section">{title} <span class="pub-count">({len(entries)})</span></h2>')
        if name == "conferences" and any(e.get("presenter") for e in entries):
            lines.append('<p class="pub-legend"><sup class="presenter">*</sup> Presenting author, when different from the first author.</p>')
        if name == "conferences":
            # split by the "scope" field: national = Spanish conferences, anything else = international
            groups = [
                ("International Conferences", [e for e in entries if e.get("scope", "").strip().lower() != "national"]),
                ("Spanish Conferences", [e for e in entries if e.get("scope", "").strip().lower() == "national"]),
            ]
            for sub, items in groups:
                if not items:
                    continue
                lines.append(f'<h3 class="pub-subsection">{sub} <span class="pub-count">({len(items)})</span></h3>')
                lines.append(f'<ol class="pub-list" reversed>')
                lines += [entry_html(e) for e in items]
                lines.append("</ol>")
        else:
            lines.append(f'<ol class="pub-list" reversed>')
            lines += [entry_html(e) for e in entries]
            lines.append("</ol>")
        lines.append('<p class="pub-top"><a href="#">↑ Back to top</a></p>')
    lines += ["```", ""]
    (PUB_DIR / "_publications.md").write_text("\n".join(lines), encoding="utf-8")
    return {n: len(data[n]) for n, _, _, _ in SECTIONS}


if __name__ == "__main__":
    counts = build()
    print("Publications built:", ", ".join(f"{k}={v}" for k, v in counts.items()))
