# SPE-800-Sensor

Project document authors: Michael Stoddard and Chadwick Adebiyi.
The shared authorship metadata is defined by `DocumentAuthors` in
[s8sManual.tex](s8sManual.tex).

## Mission and current architecture

Determine whether a measurement can be used.

1. A sensor coupled with an ADC0804 produces an 8-bit conversion code.
2. A clock/counter provides a counter value alongside that code.
3. The conversion code and counter value are two logical parallel inputs to
   interface logic in the FT245R data path. Capture, association, and transfer
   rules are open; this description does not define two physical FT245R ports.
4. An FT245R USB-to-parallel interface carries the data to the C++ host control
   app on macOS, Windows 11, and iOS; the iOS UI uses SwiftUI.
5. The host qualifies the result and publishes code, status, and timing data to
   a downstream consumer. The qualification rules and publication schema are open.

This is a documentation-only stage. The earlier C++ direction for embedded
software remains; its execution target and relationship to interface logic are
not yet allocated. The selected host platforms are macOS, Windows 11, and iOS. Linux remains an additional stakeholder request in US-03. The iOS hardware-access path and SwiftUI-to-C++ integration require explicit design and device evidence.

## Stakeholders

| Stakeholder | Need |
| --- | --- |
| Operator | See reading value, validity, availability, and age. |
| Acquisition-Developer | Continue acquisition while earlier samples are processed. |
| Field-Engineer | Use the subsystem across the field platforms in US-03; coverage remains pending. |
| Mission-Integrator | Interpret sample and status contracts and replace compatible endpoints. |

Michael Stoddard and Chadwick Adebiyi co-own document and technical content.
Michael Stoddard remains Verification/Validation Owner. The organization is Stevens Institute. Dr. Darian Muresan remains the
acceptance authority.

## Authoritative sources and open decisions

The namespace is `s8s`; the authoritative LaTeX root is [s8sManual.tex](s8sManual.tex).

- [Mission, boundary, stakeholders, and context diagram](s8sSystemContext.tex)
- [Owned questions, role assignments, and change control](s8sDevelopmentPlan.tex)
- [Requirements](s8sRequirements.tex), [architecture decisions](s8sArchitectureOverview.tex), and [traceability](s8sTraceability.tex)
- [Build and review evidence](s8sInstantiationReview.tex)

Open decisions include sensor characteristics; ADC reference/clock/handshake;
counter width/rate/rollover and timing meaning; capture coherence and association;
parallel-bus ownership and transfer framing; qualification and source-health
criteria; output semantics/schema/transport; the macOS, Windows 11, and iOS platform/toolchain matrices, iOS SwiftUI-to-C++ integration and acquisition access; and the
embedded C++ execution allocation. No fault response, numeric limit, or product
test result is inferred from the hardware selection.

## Build and review

From the Architecture directory: `make -f s8sMakefileMacLinux pdf`.
The result is [s8sArchitecture.pdf](s8sArchitecture.pdf), the integrated draft System Requirements and Architecture Specification. Full requirements and architecture are in the main body; tests, verification, validation, traceability, evidence, and history are appendices. Authoring and AI guides remain repository sources outside the PDF.
`python3 s8sCheckSources.py` checks active sources and traceability.
The inherited PowerShell document build remains available as
`.\s8sMakefilePowerShell.ps1 -Action pdf`; it builds the document and does not verify the control app on Windows 11 or any other target.

The reusable template is separate. Separate TikZ sources are stored beneath
the names of their including chapters. Template examples and history are
retained as uncompiled provenance.

This draft is pending technical acceptance. Changes to the architecture use
a branch and pull request in [justgus/SPE-800](https://github.com/justgus/SPE-800).
