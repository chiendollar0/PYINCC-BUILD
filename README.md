# PYINCC

Software Evidence Scanner for Windows.

PYINCC is a desktop application that inventories installed software and collects technical evidence from Windows, application metadata, installers, binaries, signatures, certificates and runtime state.

PYINCC is built with an **Enterprise Build** workflow:

> One Phase = One runnable product = Test = Freeze = Next Phase.

This repository does not track progress by individual files. Progress is tracked only by complete phases that can run, be tested and then be frozen.

---

## Product Scope

PYINCC is designed for:

- Software inventory
- Internal asset management
- Software evidence collection
- Compliance support
- Offline, local-only scanning

PYINCC does **not**:

- Modify installed software
- Activate licenses
- Bypass protection mechanisms
- Upload scan results
- Collect personal documents
- Use telemetry or cloud synchronization

---

## Build Roadmap

### Phase 1 — Foundation

**Status:** ☐ Not started

**Goal:** The application can start and present the complete desktop shell.

**Scope:**

- Project structure
- Single README
- Assets
- PyInstaller configuration
- Logging
- Config
- Main entry point
- Splash screen
- Main window
- Menu
- Toolbar
- Status bar
- Admin manifest
- Theme
- Tray
- About dialog

**Freeze criteria:**

```text
PYINCC.exe

✓ runs
✓ icon
✓ tray
✓ splash
✓ menu
✓ dashboard
✓ about
✓ settings
```

---

### Phase 2 — Scanner Engine

**Status:** ☐ Not started

**Goal:** A complete scanner engine can run from the application and return scan results.

**Scope:**

- Registry evidence
- Executable evidence
- VersionInfo evidence
- Signature evidence
- Certificate evidence
- Hash evidence
- Installer evidence
- Runtime evidence

**Deliverable:**

```text
Scanner Engine
```

**Freeze criteria:**

```text
Scan button

✓ starts scan
✓ collects evidence
✓ returns normalized results
✓ reports errors safely
```

---

### Phase 3 — Plugin Manager

**Status:** ☐ Not started

**Goal:** Product-specific plugins can enrich scanner results.

**Scope:**

- Windows
- Office
- Adobe
- Autodesk
- WinRAR
- Foxit
- VMware
- IDM

**Deliverable:**

```text
Plugin Manager
```

**Freeze criteria:**

```text
Plugin scan

✓ loads enabled plugins
✓ runs plugin checks
✓ merges plugin evidence
✓ handles plugin failures safely
```

---

### Phase 4 — UI

**Status:** ☐ Not started

**Goal:** The complete user interface supports reviewing scanner results.

**Scope:**

- Dashboard
- Inventory
- Evidence
- Report view
- Search
- Filter
- Detail panel
- Runtime view
- Progress view
- Popup notifications

**Freeze criteria:**

```text
UI review workflow

✓ displays dashboard
✓ displays inventory
✓ displays evidence
✓ supports search and filter
✓ shows details and progress
```

---

### Phase 5 — Export

**Status:** ☐ Not started

**Goal:** Users can export complete scan output.

**Scope:**

- CSV export
- Excel export
- Report summary

**Freeze criteria:**

```text
Export workflow

✓ exports CSV
✓ exports Excel
✓ creates summary report
✓ preserves evidence fields
```

---

### Phase 6 — Polish

**Status:** ☐ Not started

**Goal:** The application receives final visual and usability polish.

**Scope:**

- Icon
- Logo
- Splash
- Tray
- Dark theme
- Light theme
- Animation
- Popup
- Loading state

**Freeze criteria:**

```text
Polished desktop app

✓ consistent visual identity
✓ dark and light themes
✓ stable tray behavior
✓ polished loading and popup states
```

---

### Phase 7 — Release

**Status:** ☐ Not started

**Goal:** PYINCC is packaged and ready for release.

**Scope:**

- Bug fixes
- Optimization
- Packaging
- PyInstaller
- Installer
- Release artifacts

**Freeze criteria:**

```text
Release build

✓ packaged executable
✓ installer artifact
✓ release notes
✓ final smoke test
```

---

## Freeze Policy

After a phase is frozen, it is not reopened for new features.

A frozen phase may only be changed for:

- Bug fixes
- Crash fixes
- Incorrect logic
- Build or packaging breakages that block a later phase

New functionality must be scheduled into the current or a future phase instead of being added back into a frozen phase.

---

## Development Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m src.main
```

Build the executable:

```bash
pyinstaller build.spec
```

---

## Project Status

| Phase | Name | Status |
| --- | --- | --- |
| Phase 1 | Foundation | ☐ |
| Phase 2 | Scanner Engine | ☐ |
| Phase 3 | Plugin Manager | ☐ |
| Phase 4 | UI | ☐ |
| Phase 5 | Export | ☐ |
| Phase 6 | Polish | ☐ |
| Phase 7 | Release | ☐ |

Architecture: Frozen

Development workflow: Enterprise Build

License: MIT

Copyright © 2026 PYINCC

Support: pyinccsupport@gmail.com
