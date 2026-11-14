# SPE-800-Sensor
Course materials and the 8-bit sensor-system architecture project for SPE-800.

The mission is to determine whether a measurement can be used. The current
architecture combines an ADC0804 8-bit conversion code with a clock/counter
value, transfers the associated data through an FT245R USB-to-parallel data
path to a C++ host application on macOS, and publishes qualified code, status,
and timing data to a downstream consumer. Capture, association, qualification,
and publication contracts remain to be specified.

- [Project overview, stakeholders, open decisions, and build instructions](s8sReadme.md)
- [Architecture source](s8sManual.tex)
- [Architecture PDF](s8sManual.pdf)

[ArchitectureDesignTemplate-2.33](../ArchitectureDesignTemplate-2.33/) holds the reusable template. Project-specific work belongs in this directory. This stage covers documentation only. The confirmed file namespace is `s8s`.

For each change, branch from the latest `main`, push the branch, and open
a pull request against `main` for review.
