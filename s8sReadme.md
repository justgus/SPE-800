# SPE-800-Sensor

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

The namespace is `s8s`; the book root is [s8sManual.tex](s8sManual.tex).

- [Mission, boundary, stakeholders, and context diagram](s8sSystemContext.tex)
- [Owned questions, role assignments, and change control](s8sDevelopmentPlan.tex)
- [Requirements](s8sRequirements.tex), [architecture decisions](s8sArchitectureOverview.tex), and [traceability](s8sTraceability.tex)
- [Build and review evidence](s8sInstantiationReview.tex)

Open decisions include sensor characteristics; ADC reference/clock/handshake;
counter width/rate/rollover and timing meaning; capture coherence and association;
parallel-bus ownership and transfer framing; qualification and source-health
criteria; output semantics/schema/transport; macOS/toolchain versions; and the
embedded C++ execution allocation. No fault response, numeric limit, or product
test result is inferred from the hardware selection.

## Build and review

From the Architecture directory: `make -f s8sMakefileMacLinux pdf`.
The result is [s8sManual.pdf](s8sManual.pdf).
`python3 s8sCheckSources.py` checks active sources and traceability.
The inherited PowerShell document build remains available as
`.\s8sMakefilePowerShell.ps1 -Action pdf`; it does not imply a Windows host target.

The reusable template is separate. Separate TikZ sources are stored beneath
the names of their including chapters. Template examples and history are
retained as uncompiled provenance.

This draft is pending acceptance and explicit authorization for initial
publication on main. The specified repository is
[justgus/SPE-800-Sensor](https://github.com/justgus/SPE-800-Sensor).
Every later change uses a branch and pull request.
