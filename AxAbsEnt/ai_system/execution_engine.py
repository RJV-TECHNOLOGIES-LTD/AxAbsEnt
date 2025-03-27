import importlib.util
import os

def execute_module(domain, method):
    try:
        module_path = f'../architecture/{domain}/{domain.split("_")[0]}_engine.py'
        spec = importlib.util.spec_from_file_location("engine", module_path)
        engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine)
        func = getattr(engine, method)
        return func()
    except Exception as e:
        return {"error": str(e)}
