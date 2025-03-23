name: "🐞 Ontological Bug Report"
description: Report logic errors, tensor inconsistencies, simulation failures, or theory violations
title: "[BUG] Title of bug"
labels: ["bug", "critical-analysis", "investigation"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## 🧠 AxAbsEnt Unified System – Fault Reporting Protocol

        Thank you for taking the time to report a fault. This form captures reproducible bugs,
        system inconsistencies, or emergent behavior mismatches aligned with the Enhanced Mathematical Ontology of Absolute Nothingness.

  - type: input
    id: bug-summary
    attributes:
      label: Bug summary
      description: Briefly describe what failed and what should have occurred.
      placeholder: "Tensor field collapsed at SDI > 0.7; expected CEFT tensor output"
    validations:
      required: true

  - type: textarea
    id: reproduction-steps
    attributes:
      label: Reproduction steps
      description: List the exact steps, CLI commands, notebook cells, or API routes used.
      placeholder: |
        1. python run_simulations.py --config config/entropy_chain.json
        2. Observe the crash when SDI exceeds 0.7
      render: bash
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected behavior
      description: What should have occurred under correct logic?
      placeholder: "Output tensor signature should have yielded CEFTResolvedTensor with ΔS > 0"
    validations:
      required: true

  - type: textarea
    id: observed-behavior
    attributes:
      label: Observed behavior
      description: What actually occurred (logs, tracebacks, or incorrect results)?
      placeholder: |
        Traceback:
        File "decomposition.py", line 93, in decompose
          raise EntropyCollapseException("Tensor undefined")
      render: shell
    validations:
      required: true

  - type: dropdown
    id: module-affected
    attributes:
      label: Subsystem(s) affected
      multiple: true
      options:
        - src/core/
        - src/forces/
        - src/simulation/
        - src/visualization/
        - src/mathematics/
        - api/
        - web/
        - notebooks/
        - experimental/
        - documentation
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: Runtime environment
      description: Operating system, Python version, GPU model, container image, etc.
      placeholder: "Ubuntu 22.04, Python 3.11.6, A100 80GB, docker:gpu-v1.3"
    validations:
      required: true

  - type: checkboxes
    id: ontology-violation
    attributes:
      label: Ontological consistency violations
      description: Which theoretical expectations were violated?
      options:
        - label: ❌ CEFT (curvature entropy tensors invalid)
        - label: ❌ FDT (force projection failure)
        - label: ❌ SDI (non-monotonic symmetry decay)
        - label: ❌ SRI (selection resonance collapse)
        - label: ❌ Entropy ≤ 0 in positive force field
        - label: ❌ Tensor boundary mismatch across absolutes
        - label: ❌ Category/functor rule inconsistency

  - type: textarea
    id: attachments
    attributes:
      label: Attachments (tensor configs, logs, screenshots)
      description: Paste or describe any relevant files or links here.
      placeholder: "Attached: crash_trace.log, config.json, entropy_heatmap.png"

  - type: textarea
    id: fix-proposal
    attributes:
      label: Hypothesized cause or proposed fix (optional)
      description: Suggest a theory, patch, or subsystem fix path.
      placeholder: "Likely unbounded entropy under weak curvature. Add boundary condition to decomposition.py:L72"

  - type: checkboxes
    id: closing-criteria
    attributes:
      label: Resolution expectations
      description: Mark what must be achieved to consider this issue resolved.
      options:
        - label: Tensor output restored under identical entropy range
        - label: API route responds with valid signature
        - label: Notebook cell executes without crash
        - label: Visualization renders without distortion
        - label: Entropy level > 0 validated by unit test
