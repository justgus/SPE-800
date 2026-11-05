# My Fabulous Sensor Project

## Mission and current architecture

Determine whether a measurement can be used.

1. A sensor coupled with an ADC0804 produces an 8-bit conversion code.
2. A clock/counter provides a counter value alongside that code.
3. The conversion code and counter value are two logical parallel inputs to
   interface logic in the FT245R data path. Capture, association, and transfer
   rules are open; this description does not define two physical FT245R ports.
4. An FT245R USB-to-parallel interface carries the data to the C++ host control
   app on macOS.
5. The host qualifies the result and publishes code, status, and timing data to
   a downstream consumer. The qualification rules and publication schema are open.

This is a documentation-only stage. The earlier C++ direction for embedded
software remains; its execution target and relationship to interface logic are
not yet allocated. Windows and Linux are outside the current host scope.

## Stakeholders

| Stakeholder | Need |
| --- | --- |
| Operator | Understand whether the measurement can be used. |
| Integrator | Understand the meaning and format of the published result. |
| Maintainer | Know whether the source is connected and operating properly. |

Michael Stoddard is Document Owner, Technical Owner, and Verification/Validation
Owner. The organization is Stevens Institute. Dr. Darian Muresan remains the
acceptance authority.

## Authoritative sources and open decisions

The namespace is `mbs`; the book root is [mbsManual.tex](mbsManual.tex).

- [Mission, boundary, stakeholders, and context diagram](mbsSystemContext.tex)
- [Owned questions, role assignments, and change control](mbsDevelopmentPlan.tex)
- [Requirements](mbsRequirements.tex), [architecture decisions](mbsArchitectureOverview.tex), and [traceability](mbsTraceability.tex)
- [Build and review evidence](mbsInstantiationReview.tex)

Open decisions include sensor characteristics; ADC reference/clock/handshake;
counter width/rate/rollover and timing meaning; capture coherence and association;
parallel-bus ownership and transfer framing; qualification and source-health
criteria; output semantics/schema/transport; macOS/toolchain versions; and the
embedded C++ execution allocation. No fault response, numeric limit, or product
test result is inferred from the hardware selection.

## Build and review

From B: `make -f mbsMakefileMacLinux pdf`.
The result is [mbsManual.pdf](mbsManual.pdf).
`python3 mbsCheckSources.py` checks active sources and traceability.
The inherited PowerShell document build remains available as
`.\mbsMakefilePowerShell.ps1 -Action pdf`; it does not imply a Windows host target.

The initial documentation snapshot was published on main. This architectural
revision is being prepared on a branch for review; later changes use pull
requests. Keep this README current with supported changes and link to the book
rather than duplicating controlled requirements. Separate TikZ sources remain
under their including chapter names. The reusable template is separate.
Inherited examples/history and unused legacy assets are retained for provenance.

## Current revision checks

The complete document build and generalized traceability check passed. The draft
contains 13 candidate requirements, three stakeholder scenarios, planned tests,
and pending product verification/validation. PDF inspection findings and exact
page/link counts are retained in `mbsPDFInspection.json`; the review narrative is
in `mbsInstantiationReview.tex`. Qualification rules and the result contract still
require decisions; passing document checks does not establish measurement usability.
