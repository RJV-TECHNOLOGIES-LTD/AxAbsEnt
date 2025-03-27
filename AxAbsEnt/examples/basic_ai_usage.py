from AxAbsEnt.ai_system.core_agent import SuperSQLAI

ai = SuperSQLAI()
print("Available Domains:", ai.perceive("AxAbsEnt/architecture"))
result = ai.invoke("quantum_cognition", "analyze")
print("Analysis Result:", result)
