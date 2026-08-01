# HackTheBasics.gr Academy

A bilingual, local-first cybersecurity academy for Windows, Linux and Android with Termux. The website explains each mission; commands, evidence and progress stay on the learner's device.

## Learning structure

- One seven-stage beginner path that shows exactly what to learn next
- 38 core practices selected from the complete library
- 149 distinct practical labs and 338 estimated active hours in total
- 188 English pages and 188 matching Greek pages
- Eight collapsed optional-practice collections covering 27 clear categories
- Ultra-compact four-block labs: start, do, save, finish
- Windows, Linux and Termux instructions
- GitHub Pages-safe relative paths

## Start locally

```bash
python3 local-tools/academy.py serve
python3 local-tools/academy.py list --practical
python3 local-tools/academy.py prepare patch-audit
python3 local-tools/academy.py check patch-audit
python3 local-tools/academy.py complete patch-audit
python3 local-tools/academy.py status
```

On Windows use `py local-tools/academy.py`; in Termux use `python local-tools/academy.py`.

## GitHub Pages

The included workflow publishes the repository root from the `main` branch. All links are relative and work under a project path such as `/Test/`.


## Repository layout

- `assets/` — CSS, JavaScript, icons and catalog data
- `pages/` — English and Greek academy pages
- `labs/` and `practice/` — local hands-on exercises
- `course-source/` — curriculum source material
- `docs/` — curriculum, compatibility and quality documentation
- `local-tools/` — optional local server and academy command-line tools
- `tools/` — supporting lab utilities
