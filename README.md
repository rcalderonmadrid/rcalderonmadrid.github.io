# Web personal · Rocío Calderón Madrid

Portfolio académico hecho con [Quarto](https://quarto.org) y publicado gratis en GitHub Pages:
**<https://rcalderonmadrid.github.io>**

Diseño: plantilla *trestles* en Inicio, colores grafito + turquesa, modo oscuro por defecto con botón para cambiar a claro.

---

## Estructura de la web

Menú: **Home · Education · Experience · Projects · Publications · Mentoring · Skills · News · CV**

```
├── _quarto.yml                 ← menú, iconos de redes, pie de página, dirección de la web
├── index.qmd                   ← Home (bio, intereses, experiencia y formación resumidas, últimas noticias)
├── education.qmd               ← Education (titulaciones, tesis)
├── experience.qmd              ← Professional Experience (puestos, financiación, logos, premios)
├── projects/
│   ├── index.qmd               ← galería de proyectos (el orden se define aquí)
│   ├── momentum.qmd            ← MOMENTUM · IAS-CSIC (actual)
│   ├── fusarium.qmd            ← NASA · Cornell University
│   └── xylella.qmd             ← Fundación Alfonso Martín Escudero · University of Salford
├── publications.qmd            ← Publications (se genera sola desde los .bib)
├── publications/
│   ├── preprints.bib           ← Preprints
│   ├── articles.bib            ← Peer-reviewed Publications
│   ├── books.bib               ← Books and Book Chapters (oculta mientras esté vacía)
│   ├── conferences.bib         ← Conference Contributions (internacionales y nacionales)
│   ├── outreach.bib            ← Technical and Outreach Articles
│   ├── metrics.yml             ← métricas de Scopus (h-index, citas, documentos)
│   └── _publications.md        ← generado automáticamente: NO editar
├── mentoring.qmd               ← Mentoring (tesis dirigidas)
├── skills.qmd                  ← Skills
├── news.qmd                    ← News (lista automática)
├── news/                       ← una noticia = un archivo .qmd (_template.qmd es la plantilla)
├── files/
│   ├── CV_Rocio_Calderon.pdf   ← el CV que abre la pestaña "CV"
│   └── pdfs/                   ← PDFs de publicaciones, una carpeta por sección
├── images/                     ← foto de perfil, logos de instituciones, proyectos y noticias
├── styles/                     ← colores (light.scss / dark.scss), estilos (custom.css), botones de compartir (share.html)
├── scripts/build_publications.py   ← convierte los .bib en la página de publicaciones
└── .github/workflows/publish.yml   ← publica la web automáticamente al subir cambios
```

---

## Trabajar con la web

### Ver la web en tu ordenador

En la terminal de VS Code:

```bash
quarto preview
```

Se abre en el navegador y se actualiza al guardar (Cmd + S). Para pararlo: **Ctrl + C** en la terminal.

> Los cambios en los `.bib` **no** se ven solos en el preview. Ejecuta en otra terminal
> `python3 scripts/build_publications.py` y recarga el navegador (o reinicia el preview).

### Publicar los cambios

1. Panel **Source Control** (⑂, o Cmd + Shift + G).
2. Escribe un mensaje corto y pulsa **Commit**.
3. Pulsa **Sync Changes**.

GitHub publica la web sola en 1–3 minutos. Para comprobarlo: pestaña
[Actions](https://github.com/rcalderonmadrid/rcalderonmadrid.github.io/actions) → check verde ✅.
Después recarga la web con **Cmd + Shift + R**.

---

## Guía rápida: qué tocar para cada cosa

| Quiero… | Qué hago |
|---|---|
| **Añadir un artículo** | Pegar su BibTeX en `publications/articles.bib` (desde Zotero, la web de la revista o <https://www.doi2bib.org>) |
| **Añadir un preprint** | Pegarlo en `publications/preprints.bib` con `publisher = {servidor}`. Al publicarse, moverlo a `articles.bib` |
| **Añadir un congreso** | Copiar una entrada de `publications/conferences.bib` |
| **Añadir un libro o capítulo** | Quitar los `%` de un ejemplo de `publications/books.bib` y rellenarlo |
| **Añadir divulgación** | Copiar una entrada de `publications/outreach.bib` |
| **Añadir el PDF de una publicación** | Guardarlo en `files/pdfs/<sección>/<clave>.pdf` (ver abajo) |
| **Actualizar las métricas** | Cambiar los números y la fecha en `publications/metrics.yml` |
| **Añadir una noticia** | Copiar `news/_template.qmd` con un nombre nuevo (`news/2026-12-titulo.qmd`) y rellenarlo |
| **Insertar un vídeo de YouTube** | En una noticia: `{{< video https://www.youtube.com/watch?v=ID >}}` |
| **Añadir un puesto** | Copiar un bloque `timeline-item` en `experience.qmd` |
| **Añadir una titulación** | Copiar un bloque `timeline-item` en `education.qmd` |
| **Añadir un estudiante** | Copiar un bloque `mentee` en `mentoring.qmd` |
| **Añadir un proyecto** | Copiar un `.qmd` de `projects/`, poner su imagen en `images/projects/` y añadirlo a la lista de `projects/index.qmd` |
| **Actualizar el CV** | Sustituir `files/CV_Rocio_Calderon.pdf` (mismo nombre) |
| **Cambiar colores** | `styles/light.scss` y `styles/dark.scss` |

### Publicaciones: campos útiles en los `.bib`

| Campo | Para qué sirve |
|---|---|
| `doi = {10.xxxx/...}` | Muestra "DOI: …" clicable que abre el artículo |
| `url = {https://...}` | Icono de enlace (solo si no hay DOI) |
| `code = {https://github.com/...}` | Botón **Code** |
| `data = {https://...}` | Botón **Data** (figshare, Zenodo…) |
| `pdf = {files/pdfs/...}` | PDF con otro nombre (si no, se busca por la clave) |
| `presentation = {Oral}` / `{Poster}` / `{Invited}` / texto libre | Etiqueta del tipo de presentación (congresos) |
| `presenter = {Apellido, N.}` | Asterisco \* en quien presentó, si no es el primer autor |
| `scope = {national}` | Lo pone en *Spanish Conferences* (si no, *International*) |
| `date = {Diciembre 2018}` | Fecha del número (divulgación) o del congreso |

- **Cursiva** en títulos: escribe `<i>Xylella fastidiosa</i>`.
- **Claves**: formato corto `apellido` + `año` + `palabra` en minúsculas, sin tildes ni guiones
  (p. ej. `calderon2026iobc`, `poblete2021discriminating`).

### PDFs

Guárdalos con la **clave de la entrada** como nombre, en la carpeta de su sección:

```
files/pdfs/preprints/     files/pdfs/articles/     files/pdfs/books/
files/pdfs/conferences/   files/pdfs/outreach/     files/pdfs/mentoring/
```

Ejemplo: `files/pdfs/conferences/calderon2024nasa.pdf`. El icono de PDF aparece solo.

> Antes de colgar el PDF de un artículo, comprueba que la revista lo permite
> (<https://openpolicyfinder.jisc.ac.uk>). Si no, usa el manuscrito aceptado.
> Intenta que cada PDF pese menos de ~5 MB.

---

## Pendiente

Busca `TODO` en VS Code (Cmd + Shift + F) para encontrar huecos.

- [ ] Sustituir el **CV provisional** de `files/CV_Rocio_Calderon.pdf` por el CV real
- [ ] Revisar el **año de inicio de MOMENTUM** en `experience.qmd`
- [ ] Imagen propia para los proyectos de **Fusarium** y **Xylella** (`images/projects/`)
- [ ] Confirmar fecha y formato de **RAQRS 2020** y el orden de autores de **ICPP 2018** en `conferences.bib`
- [ ] Tipo de presentación de **Tantoyuca 2022** en `conferences.bib`
- [ ] Número de **Grandes Cultivos 2018** en `outreach.bib`
- [ ] PDF de **PHYTOMA 2024** (`files/pdfs/outreach/navascortes2024phytoma.pdf`)
- [ ] Cambiar la etiqueta `Upcoming` del **workshop de teledetección** cuando haya pasado
- [ ] Actualizar `publications/metrics.yml` cada pocos meses
