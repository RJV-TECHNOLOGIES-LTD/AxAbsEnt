from .perception_engine import scan_domains
from .execution_engine import execute_module
from .recursion_manager import check_paradox, handle_collapse
import yaml
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), 'simulation_mind.yaml')

class SuperSQLAI:
    def __init__(self):
        with open(STATE_FILE, 'r') as f:
            self.state = yaml.safe_load(f)

    def perceive(self, base_path='../architecture'):
        self.state['active_domains'] = scan_domains(base_path)
        self._save_state()
        return self.state['active_domains']

    def invoke(self, domain, method):
        result = execute_module(domain, method)
        self.state['last_executed'] = {domain: method}
        self.state['trace_log'].append((domain, method))
        if check_paradox(result):
            self.state['paradox_zones'].append(domain)
            result = handle_collapse(result)
        self._save_state()
        return result

    def _save_state(self):
        with open(STATE_FILE, 'w') as f:
            yaml.dump(self.state, f)
