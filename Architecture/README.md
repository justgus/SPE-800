# SPE-800-Sensor

Project document authors: Michael Stoddard and Chadwick Adebiyi.

Course materials and the 8-bit sensor-system architecture project for SPE-800.

The mission is to determine whether a measurement can be used. The current
architecture combines an ADC0804 8-bit conversion code with a clock/counter
value, transfers the associated data through an FT245R USB-to-parallel data
path to a primarily C++ control app on macOS, Windows 11, and iOS, and publishes qualified code, status,
and timing data to a downstream consumer. Capture, association, qualification,
and publication contracts remain to be specified. The iOS UI uses SwiftUI; its integration with the C++ core and its acquisition connection remain open design decisions. Michael Stoddard and Chadwick Adebiyi co-own document and technical content.

- [Project overview, stakeholders, open decisions, and build instructions](s8sReadme.md)
- [Architecture source](s8sManual.tex)
- [System Requirements and Architecture Specification](s8sArchitecture.pdf)

[ArchitectureDesignTemplate-2.33](../ArchitectureDesignTemplate-2.33/) holds the reusable template. Project-specific work belongs in this directory. This stage covers documentation only. The confirmed file namespace is `s8s`.

For each change, branch from the latest `main`, push the branch, and open
a pull request against `main` for review.
