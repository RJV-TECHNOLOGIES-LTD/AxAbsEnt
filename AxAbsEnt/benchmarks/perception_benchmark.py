import time
from AxAbsEnt.ai_system.core_agent import SuperSQLAI

ai = SuperSQLAI()
start = time.time()
for _ in range(100):
    ai.perceive("AxAbsEnt/architecture")
end = time.time()
print("Perception benchmark (100x):", end - start, "seconds")
