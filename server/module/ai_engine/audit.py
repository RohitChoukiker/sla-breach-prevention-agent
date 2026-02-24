import json
import datetime

def log_trace(state):

    entry = {
        "ticket_id": state["ticket_id"],
        "timestamp": str(datetime.datetime.utcnow()),
        "state": state
    }

    with open("ai_audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
