# HackTheBasics.gr Academy

A bilingual, local-first cybersecurity academy for Windows, Linux and Android with Termux. The website explains each mission; commands, evidence and progress stay on the learner's device.

## Curriculum

- 109 distinct practical labs
- 258 estimated active hours
- 147 English pages and 147 matching Greek pages
- Ultra-compact four-block labs: start, do, save, finish
- Windows, Linux and Termux instructions
- GitHub Pages-safe relative paths

## Start locally

```bash
python3 academy.py serve
python3 academy.py list --practical
python3 academy.py prepare patch-audit
python3 academy.py check patch-audit
python3 academy.py complete patch-audit
python3 academy.py status
```

On Windows use `py academy.py`; in Termux use `python academy.py`.

## GitHub Pages

The included workflow publishes the repository root from the `main` branch. All links are relative and work under a project path such as `/Test/`.
