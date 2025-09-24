# SciPy India Intro Slides

This folder contains the LaTeX sources and compiled PDF for the SciPy India intro deck.

## Files

- `Main.tex` – main document

- `Config.tex` – theme/layout configuration
- `Figures/` – images used in the slides (logo, QR code)
- `SciPy-intro-slides.pdf` – compiled PDF

## How to compile

Option 1: Overleaf (Recommended)

- Upload `Main.tex`, `Config.tex`, and the `Figures/` folder.
- Set `Main.tex` as the root document.
- Compile to PDF.

Option 2: Local (TeX Live/MiKTeX)

<!-- Yet to test these out -->

## Making edits

- Update text in `Main.tex` only with content already agreed in the website/README/reviews.
- If you change footer widths or layout, edit appropriately in `Config.tex`.
- Place new images in `Figures/` and reference them relatively, e.g. `Figures/image-name.png`.

## Publishing

- Commit the updated PDF and sources in this `slides/` folder.
- The website links to the PDF at `slides/SciPy-intro-slides.pdf` from the homepage under “Slides”.
