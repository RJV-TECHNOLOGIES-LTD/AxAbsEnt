name: "🐞 Bug Report"
description: Report a system bug, runtime failure, simulation anomaly, or ontological inconsistency
title: "[BUG] Short but specific summary of the fault"
labels: ["bug", "triage", "investigation"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## 🧠 AxAbsEnt Bug Report Form

        This form is for reproducible issues affecting:
        - Simulation accuracy
        - Tensor output consistency
        - Ontological compliance (CEFT, FDT, SDI, SRI)
        - API failures
        - Frontend rendering
        - Documentation mismatches

  - type: input
    id: summary
    attributes:
      label: Bug Summary
      description: What exactly went wrong, and what should have happened?
      placeholder: "Curvature entropy tensor returns null under high SDI. Expected CEFT tensor object."
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Provide exact commands, simulation configs, or inputs.
      placeholder: |
        1. Run: python run_simulations.py --config config/chain_resonance.json
        2. Observe entropy collapse failure at SDI > 0.75
      render: bash
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Output
      description: What should have happened if the system worked correctly?
      placeholder: "Tensor decomposition should return CEFTResolvedTensor object with ΔS > 0"
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Observed Output / Logs
      description: What actually happened? Include traceback or output logs.
      placeholder: |
        Traceback:
        File "forces/extract.py", line 64
          raise EntropyCollapseError("Negative entropy signature")
      render: shell
    validations:
      required: true

  - type: dropdown
    id: affected_module
    attributes:
      label: Which subsystem is affected?
      multiple: true
      options:
        - Core (src/core/)
        - Forces (src/forces/)
        - Simulation Engine (src/simulation/)
        - Visualization (src/visualization/)
        - Mathematics (src/mathematics/)
        - API Backend (api/)
        - Frontend UI (web/)
        - Notebooks (notebooks/)
        - Experimental Predictions (src/experimental/)
        - Documentation
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: Runtime Environment
      description: OS, Python version, GPU, container, and cluster setup if applicable.
      placeholder: "Ubuntu 22.04, Python 3.11, A100 80GB, Docker (gpu-v1.4), Kubernetes"
    validations:
      required: true

  - type: checkboxes
    id: ontology
    attributes:
      label: Did this bug violate any theoretical constraints?
      description: Mark any that were affected by this issue.
      options:
        - label: ❌ CEFT – Curvature Entropy tensors malformed
        - label: ❌ FDT – Force Differentiation Tensor logic failed
        - label: ❌ SDI – Symmetry decay inconsistency
        - label: ❌ SRI – Selection resonance index collapse
        - label: ❌ Tensor projection across absolutes broken
        - label: ❌ Category-theory constraint (e.g., invalid functor mapping)

  - type: textarea
    id: fix_hint
    attributes:
      label: (Optional) Hypothesis or proposed fix
      description: Suggest where the fault originates or how to patch it.
      placeholder: "Likely undefined curvature condition in force_extraction.py:L87. Suggest entropy threshold check."

  - type: checkboxes
    id: confirmation
    attributes:
      label: Resolution Criteria
      description: Check all that must be true for this bug to be considered resolved.
      options:
        - label: Simulation runs to completion under identical conditions
        - label: Tensor output type and shape are valid
        - label: Entropy projection matches expected ΔS
        - label: API endpoint returns valid 200 JSON
        - label: Frontend visualization renders without corruption
        - label: Unit test passes or is added for this case
