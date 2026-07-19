# PYINCC

PYINCC is a Software Evidence Scanner focused on inventory and evidence collection.
It is intentionally scoped to collect observable software evidence only and does not
attempt to determine, classify, or analyze the license status of commercial software.

## Build order

1. README
2. Core
3. Models
4. Registry Scanner
5. Executable Scanner
6. VersionInfo Scanner
7. Signature Scanner
8. Certificate Scanner
9. Hash Scanner
10. Installer Scanner
11. Runtime Scanner
12. Plugin Framework
13. GUI
14. Export
15. Build
16. Test
17. Bug Fix
18. Release

## Initial layout

```text
PYINCC/
├── assets/
├── docs/
├── src/
│   ├── core/
│   ├── scanner/
│   ├── plugins/
│   ├── report/
│   ├── gui/
│   ├── models/
│   └── utils/
├── tests/
└── dist/
```
