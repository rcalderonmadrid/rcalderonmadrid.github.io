# Personal website · Rocío Calderón Madrid

Academic portfolio built with [Quarto](https://quarto.org) and published for free on GitHub Pages:
**<https://rcalderonmadrid.github.io>**

Design: *trestles* template on the home page, charcoal + turquoise colours, dark mode by default with a toggle to switch to light mode.

---

## Website structure

Menu: **Home · Education · Experience · Projects · Publications · Mentoring · Skills · News · CV**

```
├── _quarto.yml                 ← menu, social icons, footer, website address
├── index.qmd                   ← Home (bio, interests, summary of experience and education, latest news)
├── education.qmd               ← Education (degrees, theses)
├── experience.qmd              ← Professional Experience (positions, funding, logos, awards)
├── projects/
│   ├── index.qmd               ← project gallery (the order is set here)
│   ├── momentum.qmd            ← MOMENTUM · IAS-CSIC (current)
│   ├── fusarium.qmd            ← NASA · Cornell University
│   └── xylella.qmd             ← Alfonso Martín Escudero Foundation · University of Salford
├── publications.qmd            ← Publications (built automatically from the .bib files)
├── publications/
│   ├── preprints.bib           ← Preprints
│   ├── articles.bib            ← Peer-reviewed Publications
│   ├── books.bib               ← Books and Book Chapters (hidden while empty)
│   ├── conferences.bib         ← Conference Contributions (international and Spanish)
│   ├── outreach.bib            ← Technical and Outreach Articles
│   ├── metrics.yml             ← Scopus metrics (h-index, citations, documents)
│   └── _publications.md        ← generated automatically: DO NOT edit
├── mentoring.qmd               ← Mentoring (supervised theses)
├── skills.qmd                  ← Skills
├── news.qmd                    ← News (automatic list)
├── news/                       ← one news item = one .qmd file (_template.qmd is the template)
├── files/
│   ├── CV_Rocio_Calderon.pdf   ← the CV opened by the "CV" tab
│   └── pdfs/                   ← PDFs of publications, one folder per section
├── images/                     ← profile photo, institution logos, project and news images
├── styles/                     ← colours (light.scss / dark.scss), styles (custom.css), share buttons (share.html)
├── scripts/build_publications.py   ← turns the .bib files into the Publications page
└── .github/workflows/publish.yml   ← publishes the website automatically when changes are pushed
```

---

## Working on the website

### Preview the website locally

In the VS Code terminal:

```bash
quarto preview
```

The site opens in the browser and refreshes every time you save (Cmd + S). To stop it: **Ctrl + C** in the terminal.

> Changes to the `.bib` files are **not** picked up automatically by the preview. Run
> `python3 scripts/build_publications.py` in a second terminal and reload the browser (or restart the preview).
>
> If deleted pages still appear in the preview, stop it, delete the `_site` and `.quarto` folders
> (they are rebuilt automatically) and run `quarto preview` again.

### Publish changes

1. Open the **Source Control** panel (⑂, or Cmd + Shift + G).
2. Write a short message and click **Commit**.
3. Click **Sync Changes**.

GitHub publishes the site automatically in 1–3 minutes. To check: the
[Actions](https://github.com/rcalderonmadrid/rcalderonmadrid.github.io/actions) tab → green check ✅.
Then reload the website with **Cmd + Shift + R**.

---

## Quick guide: what to edit for each task

| I want to… | What to do |
|---|---|
| **Add a journal article** | Paste its BibTeX into `publications/articles.bib` (from Zotero, the journal website or <https://www.doi2bib.org>) |
| **Add a preprint** | Paste it into `publications/preprints.bib` with `publisher = {server}`. Once published, move it to `articles.bib` |
| **Add a conference contribution** | Copy an entry in `publications/conferences.bib` |
| **Add a book or book chapter** | Remove the `%` from an example in `publications/books.bib` and fill it in |
| **Add an outreach article** | Copy an entry in `publications/outreach.bib` |
| **Add the PDF of a publication** | Save it as `files/pdfs/<section>/<key>.pdf` (see below) |
| **Update the metrics** | Change the numbers and the date in `publications/metrics.yml` |
| **Add a news item** | Copy `news/_template.qmd` with a new name (`news/2026-12-title.qmd`) and fill it in |
| **Embed a YouTube video** | In a news item: `{{< video https://www.youtube.com/watch?v=ID >}}` |
| **Add a position** | Copy a `timeline-item` block in `experience.qmd` |
| **Add a degree** | Copy a `timeline-item` block in `education.qmd` |
| **Add a student** | Copy a `mentee` block in `mentoring.qmd` |
| **Add a project** | Copy a `.qmd` file in `projects/`, put its image in `images/projects/` and add it to the list in `projects/index.qmd` |
| **Update the CV** | Replace `files/CV_Rocio_Calderon.pdf` (same name) and change the date after `?v=` in the CV link of `_quarto.yml`, so browsers load the new version instead of a cached one |
| **Change the colours** | `styles/light.scss` and `styles/dark.scss` |

### Publications: useful fields in the `.bib` files

| Field | What it does |
|---|---|
| `doi = {10.xxxx/...}` | Shows a clickable "DOI: …" that opens the article |
| `url = {https://...}` | Link icon (only if there is no DOI) |
| `code = {https://github.com/...}` | **Code** button |
| `data = {https://...}` | **Data** button (figshare, Zenodo…) |
| `pdf = {files/pdfs/...}` | PDF with a different file name (otherwise it is found by its key) |
| `presentation = {Oral}` / `{Poster}` / `{Invited}` / free text | Presentation type label (conferences) |
| `presenter = {Surname, N.}` | Asterisk \* on the presenting author, when not the first author |
| `scope = {national}` | Lists it under *Spanish Conferences* (otherwise *International*) |
| `date = {December 2018}` | Issue date (outreach) or conference dates |

- **Italics** in titles: write `<i>Xylella fastidiosa</i>`.
- **Keys**: short format `surname` + `year` + `word`, lowercase, no accents or hyphens
  (e.g. `calderon2026iobc`, `poblete2021discriminating`).

### PDFs

Save each PDF with the **key of its entry** as file name, in the folder of its section:

```
files/pdfs/preprints/     files/pdfs/articles/     files/pdfs/books/
files/pdfs/conferences/   files/pdfs/outreach/     files/pdfs/mentoring/
```

Example: `files/pdfs/conferences/calderon2024nasa.pdf`. The PDF icon appears automatically.

> Before uploading the PDF of a paper, check that the journal allows it
> (<https://openpolicyfinder.jisc.ac.uk>). If not, use the accepted manuscript.
> Try to keep each PDF under ~5 MB.

---

## To do

Search for `TODO` in VS Code (Cmd + Shift + F) to find gaps.

- [ ] Check the **MOMENTUM start year** in `experience.qmd`
- [ ] Own images for the **Fusarium** and **Xylella** projects (`images/projects/`)
- [ ] Confirm the dates and format of **RAQRS 2020** and the author order of **ICPP 2018** in `conferences.bib`
- [ ] Presentation type of **Tantoyuca 2022** in `conferences.bib`
- [ ] Issue number of **Grandes Cultivos 2018** in `outreach.bib`
- [ ] PDF of **PHYTOMA 2024** (`files/pdfs/outreach/navascortes2024phytoma.pdf`)
- [ ] Change the `Upcoming` label of the **remote sensing workshop** once it has taken place
- [ ] Update `publications/metrics.yml` every few months
