
AUDIT_LOGS = []

def log_audit_event(event_type, user_id, description):
    entry = {
        "event_type": event_type,
        "user_id": user_id,
        "description": description
    }
    AUDIT_LOGS.append(entry)
    print(f"AUDIT LOG | {event_type} | User: {user_id} | {description}")

def get_audit_logs():
    return list(AUDIT_LOGS)

