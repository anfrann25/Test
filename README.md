# HackTheBasics.gr — Local-First Bilingual Academy

HackTheBasics is a static English/Greek cybersecurity academy for Windows, Linux and Android with Termux.

The project deliberately separates **education** from **execution**:

- The website explains concepts, commands, examples, compatibility and safety.
- The website never runs a terminal or accesses local files.
- Practical commands, Python programs and challenge files run in the learner's own terminal.
- `academy.py` detects the current device and stores progress locally in that user's profile.

## Start the academy program

### Windows

Double-click:

```text
run-academy.bat
```

Or run in PowerShell:

```powershell
py academy.py
```

### Linux

```bash
chmod +x run-academy.sh
./run-academy.sh
```

### Android / Termux

```bash
pkg install python
chmod +x run-academy.sh
./run-academy.sh
```

The interactive program can:

- detect Windows, Linux or Termux
- start the educational website locally
- list all 36 bilingual lessons
- show device-specific local practice paths
- mark lessons complete or reopen them
- store progress in `~/.hackthebasics/progress.json`

Useful direct commands:

```bash
python3 academy.py status
python3 academy.py lessons
python3 academy.py serve
python3 academy.py complete LESSON_ID
python3 academy.py paths
```

On Windows, replace `python3` with `py` when appropriate.

## Website features

- 36 English lessons and 36 matching Greek lessons
- blue/white light theme and blue/black dark theme
- logo on the left, global lesson search in the top bar, menu on the far right
- responsive right-side academy menu
- persistent language and theme choices
- reading size and width controls
- command-copy buttons for use in a real local terminal
- Windows, Linux and Termux setup routes
- cross-platform command reference and glossary
- device compatibility notes and ARM warnings
- keyboard focus, skip links and reduced-motion support
- local serving and optional offline cache

## Practice directories

```text
labs/linux/linux_challenges
labs/python/python_challenges
labs/web/web-challenges
tools/htb-cli
```

The included compiled Linux challenge binaries target x86-64. They may work on compatible native Linux or WSL, but not normally on ARM Android phones. Termux learners can use the theory, Python challenges and portable shell tasks.

## Safety

Use security tools only on systems you own or have explicit permission to test. Run unfamiliar binaries or deliberately vulnerable software in a disposable virtual machine or container.

## GitHub Pages

The static website remains compatible with a GitHub Pages project URL such as:

```text
https://anfrann25.github.io/Test/
```

The repository includes `.nojekyll` and `.github/workflows/pages.yml`. In the repository settings, select **Pages → Source → GitHub Actions** once.

GitHub Pages hosts only the educational website. Learners download or clone the project to use `academy.py`, labs and terminal programs locally.
