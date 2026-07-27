# Device Compatibility

| Course feature | Windows | Linux | Android + Termux | Browser only |
|---|---|---|---|---|
| Theory lessons | Yes | Yes | Yes | Yes |
| Language/theme switch | Yes | Yes | Yes | Yes |
| Browser command lab | Yes | Yes | Yes | Yes |
| Python exercises | Native Python or WSL | Native Python | Termux Python | Reading only |
| Portable shell tasks | WSL recommended | Native | Most tasks | Simulator |
| x86-64 challenge binaries | WSL compatibility varies | Yes on x86-64 | Usually no on ARM | No |
| VirtualBox labs | Yes | Yes where supported | No | No |
| Offline PWA | Yes | Yes | Yes | Requires first HTTP load |

Do not expose `serve.py` to an untrusted network. Its default address is `127.0.0.1`, which is accessible only from the current device.
