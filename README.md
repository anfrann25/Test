# HackTheBasics.gr — Cross-Device Bilingual Edition

A static English/Greek cybersecurity course designed for:

- Windows with PowerShell, Python and optional WSL
- Native Linux
- Android with Termux
- Browser-only study on phones, tablets and computers

## Start the website

### Windows

Double-click `start-site.bat`, or run:

```powershell
py serve.py
```

### Linux

```bash
./start-site.sh
```

### Android / Termux

```bash
pkg install python
./start-termux.sh
```

Open `http://127.0.0.1:8000`.

## Added learning features

- 36 matched English and Greek lessons
- Dedicated Windows, Linux and Termux setup routes
- Safe simulated browser terminal
- Cross-platform command reference
- Cybersecurity glossary
- Persistent language and theme buttons
- Mobile sidebar and desktop navigation
- Reading size and width controls
- Per-lesson progress tracking
- Progress export/import between devices
- PWA installation and offline cache
- Device compatibility labels and ARM warnings
- Keyboard focus, skip link and reduced-motion support

## Important compatibility note

The preserved compiled Linux challenge binaries target x86-64 Linux. They may run on native x86-64 Linux or a suitable WSL environment, but not normally on ARM Android devices. Termux learners should use the browser simulator, Python exercises and portable shell lessons for those sections.

## Safety

Use security tools only on systems you own or have explicit written permission to test. Run unfamiliar binaries in a disposable virtual machine or container.
