# Quality report

Date: 2026-07-28

## Curriculum

- 43 distinct practical labs
- 126 estimated active hours
- 81 English pages and 81 matching Greek pages
- Every practical lab has a unique title, objective, task sequence, deliverable and reflection prompt
- Exact duplicate practical paragraphs longer than 80 characters: 0

The duration is a planning estimate, not a guaranteed completion time. It counts preparation, execution, validation, correction and documentation; passive reading is excluded.

## Responsive interface

Chromium layout checks were performed at widths of 320, 360, 390, 768, 1024 and 1440 CSS pixels.

- Top navigation stayed on one row at every tested width
- Search width at 320 px: 154 px
- Language, theme and menu controls remained visible at 320 px
- Document width never exceeded viewport width
- Search, menu, theme and language interactions passed
- Mobile practical-lesson rendering passed without horizontal overflow

## Accessibility-oriented checks

- Semantic landmarks and one primary content region
- Skip links on learning pages
- Visible keyboard focus
- Labeled search fields and icon buttons
- Controls are at least 38–44 CSS pixels in the compact navigation
- Reduced-motion support
- Text resizing controls on lesson pages
- No exact duplicate IDs
- Every image has an `alt` attribute
- Key light- and dark-theme text combinations exceed a 4.5:1 contrast ratio

This is an engineering review, not a formal WCAG conformance certification.

## Local-first boundary

- No browser terminal or terminal emulator
- No browser-based completion database
- No progress import/export UI
- Practical workspaces are created by `practice/labkit.py`
- Progress is stored by `academy.py` under the learner's home directory
- Windows, Linux and Termux launch commands are documented

## GitHub Pages

- 0 missing internal links or assets
- 0 root-absolute links
- `.nojekyll` included
- Project-subpath-safe links for `/Test/`
- Current GitHub Pages action pattern included:
  - `actions/checkout@v6`
  - `actions/configure-pages@v5`
  - `actions/upload-pages-artifact@v4`
  - `actions/deploy-pages@v4`

## Syntax and runtime checks

- `script.js`: JavaScript syntax passed
- `academy.py`: Python compilation passed
- `practice/labkit.py`: Python compilation passed
- Workspace preparation tested with `environment-inventory`
- Local completion updated the progress total from 0/126 to 2/126 hours

## Design references

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WCAG target size guidance: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- WCAG reflow guidance: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- NIST NICE Framework: https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/stable/
- GitHub Pages custom workflows: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
