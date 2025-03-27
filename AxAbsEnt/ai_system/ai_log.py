import datetime

def log_trace(action, details):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open("ai_system/simulation_trace.log", "a") as log:
        log.write(f"[{timestamp}] ACTION: {action}\nDETAILS: {details}\n\n")
