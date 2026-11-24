# SPE-800

Project document authors: Michael Stoddard and Chadwick Adebiyi.

Course materials and the sensor-system architecture project for SPE-800.

The mission is to determine whether a measurement can be used. The current
architecture combines an ADC0804 8-bit conversion code with a clock/counter
value, transfers the associated data through an FT245R USB-to-parallel data
path to a C++ host application on macOS, and publishes qualified code, status,
and timing data to a downstream consumer. Capture, association, qualification,
and publication contracts remain to be specified.

- [Project overview, stakeholders, open decisions, and build instructions](Architecture/s8sReadme.md)
- [Architecture source](Architecture/s8sManual.tex)
- [System Requirements and Architecture Specification](Architecture/s8sArchitecture.pdf)

`ArchitectureDesignTemplate-2.33/` holds the reusable template. Project-specific
work belongs in `Architecture/`; the template is preserved for reuse. This stage covers
documentation only. Source documents are authoritative; README summaries are
updated with architecture changes and link to those sources.

Later changes use a branch and pull request. `.gitignore` covers regenerable
intermediate files; existing tracked intermediates require separate index cleanup.
