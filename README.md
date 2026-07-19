# PYINCC

Software Evidence Scanner for Windows

---

## Overview

PYINCC is a desktop application that inventories installed software and collects technical evidence available from Windows and application metadata.

The application is designed for software inventory, internal asset management and compliance support.

PYINCC does not modify software, activate licenses or bypass protection mechanisms.

---

## Features

- Scan installed software
- Collect Registry information
- Read executable metadata
- Verify digital signatures
- Collect certificate information
- Calculate file hashes
- Detect installer type
- Export CSV and Excel reports
- Offline operation
- Local-only data storage

---

## Privacy

PYINCC stores scan results only on the local computer.

The application does not upload scan results.

The application does not collect personal documents.

No telemetry.

No cloud synchronization.

---

## Architecture

Core

- Registry Scanner
- Executable Scanner
- VersionInfo Scanner
- Signature Scanner
- Certificate Scanner
- Hash Scanner
- Installer Scanner

Plugins

- Microsoft
- Adobe
- Autodesk
- WinRAR
- Foxit
- VMware

GUI

- Dashboard
- Inventory
- Evidence
- Reports
- Settings
- About

---

## Build

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python -m src.main
```

Build

```bash
pyinstaller build.spec
```

---

## Project Status

Architecture: Frozen

Development: In Progress

License: MIT

Copyright © 2026 PYINCC

Support

pyinccsupport@gmail.com
