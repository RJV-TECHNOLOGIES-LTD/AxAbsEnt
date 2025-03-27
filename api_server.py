from fastapi import FastAPI
from AxAbsEnt.ai_system.core_agent import SuperSQLAI

app = FastAPI()
ai = SuperSQLAI()

@app.get("/domains")
def get_domains():
    return {"domains": ai.perceive(base_path="AxAbsEnt/architecture")}

@app.get("/invoke/{domain}/{method}")
def invoke_method(domain: str, method: str):
    return ai.invoke(domain, method)
