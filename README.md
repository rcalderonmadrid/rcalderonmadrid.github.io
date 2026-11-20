# Web personal · Rocío Calderón Madrid

Web académica hecha con [Quarto](https://quarto.org) y publicada gratis en GitHub Pages.
Diseño: plantilla *trestles*, colores grafito + turquesa, con modo claro/oscuro.

## Estructura

```
├── _quarto.yml              ← menú, enlaces de redes, pie de página
├── index.qmd                ← Home
├── experience.qmd           ← Professional Experience (+ Education, Awards)
├── projects/                ← Projects: index.qmd (galería) + una página por proyecto
├── publications.qmd         ← Publications (se rellena sola desde los .bib)
├── publications/
│   ├── articles.bib         ← artículos revisados por pares
│   ├── conferences.bib      ← congresos
│   └── outreach.bib         ← divulgación
├── mentoring.qmd            ← Mentoring (tesis dirigidas)
├── news.qmd                 ← News (lista automática de las noticias)
├── news/                    ← una noticia = un archivo .qmd (_template.qmd es la plantilla)
├── skills.qmd               ← Skills
├── files/CV_Rocio_Calderon.pdf  ← el CV que se abre en la pestaña "CV"
├── images/                  ← foto de perfil, imágenes de proyectos, favicon
├── styles/                  ← colores (light.scss / dark.scss) y estilos (custom.css)
├── scripts/build_publications.py  ← genera las listas de publicaciones
└── .github/workflows/publish.yml  ← publica la web automáticamente
```

## 1. Instalar (una sola vez)

1. **Quarto**: <https://quarto.org/docs/get-started/>
2. **VS Code** con la extensión **Quarto**.
3. **Git** (en Mac: `xcode-select --install` en la Terminal) y una cuenta en GitHub.

## 2. Ver la web en tu ordenador

Abre la carpeta en VS Code y, en la terminal de VS Code:

```bash
quarto preview
```

Se abre en el navegador y se actualiza cada vez que guardas un archivo.

## 3. Subirla a GitHub (una sola vez)

1. En GitHub crea un repositorio **público** llamado `TU-USUARIO.github.io` (vacío, sin README).
2. En la terminal, dentro de la carpeta:

   ```bash
   git init
   git add .
   git commit -m "Primera versión de la web"
   git branch -M main
   git remote add origin https://github.com/TU-USUARIO/TU-USUARIO.github.io.git
   git push -u origin main
   quarto publish gh-pages
   ```

3. En GitHub: **Settings → Pages → Source: Deploy from a branch → Branch: `gh-pages` / root → Save**.
4. En **Settings → Actions → General → Workflow permissions** marca **Read and write permissions**.

Tu web estará en `https://TU-USUARIO.github.io`.

## 4. El día a día

Edita → guarda → en VS Code, panel **Source Control**: escribe un mensaje, **Commit** y **Sync/Push**.
GitHub vuelve a publicar la web sola en 1–2 minutos (lo ves en la pestaña **Actions**).

| Quiero… | Qué hago |
|---|---|
| Añadir un artículo | Pegar su entrada BibTeX en `publications/articles.bib` (o exportar desde Zotero y sustituir el archivo) |
| Añadir un botón PDF/código/datos | En la entrada BibTeX: `pdf = {files/archivo.pdf}`, `code = {https://...}`, `data = {https://...}` |
| Añadir un congreso | Copiar una entrada de `publications/conferences.bib` |
| Añadir un puesto | Copiar un bloque `timeline-item` en `experience.qmd` |
| Añadir un proyecto | Copiar un `.qmd` de `projects/`, cambiar su imagen y añadirlo a la lista de `projects/index.qmd` |
| Actualizar el CV | Sustituir `files/CV_Rocio_Calderon.pdf` (mismo nombre) |
| Añadir una noticia, prensa o vídeo | Copiar `news/_template.qmd` con un nombre nuevo (p. ej. `news/2025-03-entrevista-radio.qmd`) y rellenarlo. Aparece sola en *News* y en *Latest news* de Home |
| Insertar un vídeo de YouTube | En una noticia: `{{< video https://www.youtube.com/watch?v=ID >}}` |
| Añadir una tesis dirigida | Copiar un bloque `<div class="mentee">` en `mentoring.qmd` |
| Cambiar colores | `styles/light.scss` y `styles/dark.scss` (variables al principio) |

## 5. Pendiente de completar ✅

Busca `TODO` en VS Code (Cmd+Shift+F) para encontrar todos los huecos.

- [ ] Tu foto: sustituir `images/profile.jpg` (cuadrada, mínimo 600×600 px)
- [x] Usuario de **GitHub** (rcalderonmadrid) en `_quarto.yml`
- [x] Usuario de **Bluesky** (rcalderonmadrid.bsky.social) en `_quarto.yml`
- [ ] `site-url` en `_quarto.yml`
- [ ] Tu CV en PDF en `files/`
- [ ] Años de titulaciones, título de la tesis y directores (`experience.qmd`)
- [ ] Año de inicio de MOMENTUM y periodo postdoctoral 2015–2018 en Córdoba (`experience.qmd`)
- [ ] Premios y reconocimientos (`experience.qmd`)
- [ ] Imágenes reales de cada proyecto (`images/projects/`, formato 1200×750 aprox.) y textos de MOMENTUM y Water use
- [ ] DOIs de los artículos que solo tienen enlace a la editorial (Remote Sensing of Environment, ISPRS, MDPI)
- [ ] Sustituir los ejemplos de `mentoring.qmd` por tus estudiantes reales
- [ ] Añadir noticias de prensa y vídeos en `news/` (y comprobar la fecha de la noticia del artículo de ERL)
- [ ] PDFs de los artículos de divulgación (los tenías en Wix) → guardarlos en `files/` y añadir `pdf = {...}`
