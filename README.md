# ECO 112 - Fall 2026 Website

This repository contains the public course website for ECO 112: Principles of Macroeconomics
(Fall 2026) at Augsburg University.

## Instructor
- **Matthew Braaksma**, Department of Business Economics, PhD candidate in Applied Economics
  at the University of Minnesota.

## Structure
- Built with [Quarto](https://quarto.org/) as a static website.
- Lecture slides and the syllabus are authored in sibling project folders and pulled in at build
  time (see `pre-render` in `_quarto.yml`); this repository holds the site shell, schedule, and
  supporting pages, not the original source `.qmd` files for the slide decks.
- Sidebar navigation is managed in `_quarto.yml`.
- Deployed via GitHub Pages from the `docs/` output directory.

## Notes
- External tools (Moodle, Connect) are linked in the sidebar and open in a new tab.

## License
© 2026 Matthew Braaksma. For course use only.
