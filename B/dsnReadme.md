# My Fabulous Sensor Project

This folder contains a standalone working copy of ArchitectureDesignTemplate-2.33.
The confirmed project filename prefix is `dsn`. The original template is retained.

Edit `dsnManual.tex` for project metadata and `dsn*.tex` for chapter content.
Owner and organization remain placeholders; engineering content still needs tailoring.
Template version 2.33 and its attribution are retained.
Inherited support filenames (including `prologue.tex`, `abstract.tex`, and the
platform build scripts) are retained for compatibility with the template.

Build on macOS or Linux from this folder:

```sh
make -f makefileMacLinux pdf
```

The result is `dsnManual.pdf`. On Windows, run:

```powershell
.\makefilePowerShell.ps1 -Action pdf
```

See `dsnDocumentGuide.tex` for tool prerequisites and authoring guidance.
