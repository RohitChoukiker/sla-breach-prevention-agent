def calculate_breach_probability(urgency, similar_count):

    urgency_weight = {
        "low": 0.2,
        "medium": 0.5,
        "high": 0.7,
        "critical": 0.9
    }

    base = urgency_weight.get(urgency, 0.3)
    history = min(similar_count * 0.05, 0.3)

    return min(base + history, 1.0)


def calculate_priority(prob):

    if prob >= 0.85:
        return "P1"
    elif prob >= 0.65:
        return "P2"
    elif prob >= 0.45:
        return "P3"
    return "P4"
