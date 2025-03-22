import os
import json

class AxAbsEntCausalScheduler:
    def __init__(self, cycle2_path):
        self.cycle2_path = cycle2_path
        self.phi_map_path = os.path.join(cycle2_path, "Φmap.json")
        self.projections_path = os.path.join(cycle2_path, "projections")
        self.schedule = []

    def load_phi_map(self):
        with open(self.phi_map_path, "r") as f:
            self.schedule = json.load(f)

    def execute(self):
        print("AxAbsEnt Causal Scheduler Engine Initiated")
        for item in self.schedule:
            uid = item["UID"]
            directive = item["Directive"]
            weight = item["Weight"]
            phi = item["Φ"]
            decay = item["Decay"]
            force = item["Force"]
            if directive == "EXECUTE":
                proj_file = os.path.join(self.projections_path, f"{uid}.json")
                if os.path.exists(proj_file):
                    with open(proj_file, "r") as f:
                        chain_data = json.load(f)
                    print(f"▶ EXECUTING [{uid}] | Φ={phi} | Decay={decay} | Force={force}")
                    print(f"  ↳ Chain: {chain_data['Chain']}")
                else:
                    print(f"⚠ Projection file {uid}.json missing. Skipping.")
            else:
                print(f"⏸ RESERVED [{uid}] | Φ={phi} | Weight={weight}")

if __name__ == "__main__":
    scheduler = AxAbsEntCausalScheduler("umg/cycle2")
    scheduler.load_phi_map()
    scheduler.execute()