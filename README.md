# y5n-caps-system

**Status: Active development**

*System commands for Yakoon — navigation, jobs, sessions, and more.*

This package provides the built-in commands that make up the Yakoon
user environment. Every command is an async `main()` function using
the `y5n.sdk` API.

## Commands

| Command | Module | Description |
|---------|--------|-------------|
| `cd` | `y5n.caps.system.cd` | Change workspace directory |
| `clear` | `y5n.caps.system.clear` | Clear terminal |
| `health` | `y5n.caps.system.health` | Runtime diagnostics |
| `info` | `y5n.caps.system.info` | System information |
| `ls` | `y5n.caps.system.ls` | List workspace tree |
| `man` | `y5n.caps.system.man` | Show documentation |
| `mem` | `y5n.caps.system.mem` | Memory usage |
| `pwd` | `y5n.caps.system.pwd` | Print working directory |
| `welcome` | `y5n.caps.system.welcome` | Welcome screen |
| `whoami` | `y5n.caps.system.whoami` | Current user |
| `jobs list` | `y5n.caps.system.jobs.list` | List active flows |
| `jobs fg` | `y5n.caps.system.jobs.fg` | Foreground a flow |
| `jobs bg` | `y5n.caps.system.jobs.bg` | Background a flow |
| `jobs stop` | `y5n.caps.system.jobs.stop` | Stop a flow |
| `session list` | `y5n.caps.system.session.list` | List sessions |
| `session current` | `y5n.caps.system.session.current` | Current session |
| `session attach` | `y5n.caps.system.session.attach` | Attach to session |
| `session detach` | `y5n.caps.system.session.detach` | Detach from session |
| `net list` | `y5n.caps.system.net.list` | List network connections |
| `net connect` | `y5n.caps.system.net.connect` | Connect to runtime |

## Structure

```
src/y5n/apps/system/
├── cd.py
├── clear.py
├── health.py
├── info.py
├── ls.py
├── man.py
├── mem.py
├── pwd.py
├── welcome.py
├── whoami.py
├── jobs/
│   ├── list.py
│   ├── fg.py
│   ├── bg.py
│   └── stop.py
├── session/
│   ├── list.py
│   ├── current.py
│   ├── attach.py
│   └── detach.py
└── net/
    ├── list.py
    └── connect.py
```

## Tree integration

Each command is registered in the workspace tree via a `.yak/yak.yml`
entry at the corresponding path in `structure/`. The entry's `entry.run`
capability reference points to the Python module and `main` function.

## Links

- Developer setup: [yakoon-runtime/developer](https://github.com/yakoon-runtime/developer)
- Runtime: [yakoon-runtime/runtime](https://github.com/yakoon-runtime/runtime)
