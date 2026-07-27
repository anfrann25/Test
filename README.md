# HackTheBasics.gr Academy

A bilingual, local-first cybersecurity academy for Windows, Linux and Android with Termux. The website is educational; practical programs, evidence and progress remain on the learner's device.

## Curriculum

- 43 distinct practical labs
- 126 estimated active hours
- English and Greek page parity
- Windows, Linux and Termux instructions
- GitHub Pages-safe relative paths

The estimates cover preparation, execution, validation, correction and documentation. They are not a guaranteed completion time.

## Start locally

```bash
python3 academy.py serve
python3 academy.py list --practical
python3 academy.py prepare environment-inventory
python3 academy.py complete environment-inventory
python3 academy.py status
```

On Windows use `py academy.py`; in Termux use `python academy.py`.

## GitHub Pages

The included workflow publishes the repository root from the `main` branch. All links are relative and work under a project path such as `/Test/`.
