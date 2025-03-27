import pytest
from AxAbsEnt.ai_system.core_agent import SuperSQLAI

def test_domain_discovery():
    ai = SuperSQLAI()
    discovered = ai.perceive(base_path="AxAbsEnt/architecture")
    assert isinstance(discovered, list)
    assert "quantum_cognition" in discovered or len(discovered) > 0

def test_trace_structure():
    ai = SuperSQLAI()
    state = ai.state
    assert 'trace_log' in state
    assert isinstance(state['trace_log'], list)
