# Device Compatibility

| Feature | Windows | Linux | Android + Termux | Website only |
|---|---|---|---|---|
| Educational lessons | Yes | Yes | Yes | Yes |
| English/Greek switch | Yes | Yes | Yes | Yes |
| Blue light/dark themes | Yes | Yes | Yes | Yes |
| Top navigation search | Yes | Yes | Yes | Yes |
| Local `academy.py` progress | Yes | Yes | Yes | No |
| Python exercises | Native Python or WSL | Native Python | Termux Python | Explanation only |
| Portable shell tasks | PowerShell/WSL | Native shell | Most tasks | Explanation only |
| x86-64 challenge binaries | WSL compatibility varies | Yes on x86-64 | Usually no on ARM | No |
| Virtual machine labs | Supported | Supported where available | Not normally | Explanation only |
| Local educational site | `academy.py serve` | `academy.py serve` | `academy.py serve` | GitHub Pages |

## Design boundary

The website does not provide a simulated terminal, execute commands, access local files or store practical progress. Learners run the included programs in their own terminal. The local academy program stores progress under the current user's home directory.

The local web server binds to `127.0.0.1` by default, so it is accessible only from the current device.
