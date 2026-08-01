# Device compatibility

| Capability | Windows | Linux | Android + Termux | Website only |
|---|---|---|---|---|
| English and Greek lessons | Yes | Yes | Yes | Yes |
| 149-lab, 338-hour practical track | Yes | Yes | Yes, with documented alternatives | Explanations only |
| Local `academy.py` progress | Yes | Yes | Yes | No |
| Workspace generator | `py local-tools/academy.py prepare LAB_ID` | `python3 local-tools/academy.py prepare LAB_ID` | `python local-tools/academy.py prepare LAB_ID` | No |
| Python automation labs | Native Python or WSL | Native Python | Termux Python | No |
| Shell and file labs | PowerShell or WSL | Native shell | Termux shell | No |
| x86-64 bundled binaries | WSL compatibility varies | x86-64 Linux only | Usually unavailable on ARM | No |
| Virtual-machine work | Supported | Supported where virtualization exists | Use a separate PC or safe alternative | No |
| Local academy server | `py local-tools/academy.py serve` | `python3 local-tools/academy.py serve` | `python local-tools/academy.py serve` | GitHub Pages |

## Boundary

The website is an educational interface. It does not simulate a terminal, execute commands, access local files or save practical progress. Programs, sample data, evidence and completion records stay on the learner's device.

The local server binds to `127.0.0.1` by default, so it is visible only to the current device unless the learner deliberately changes the host option.
