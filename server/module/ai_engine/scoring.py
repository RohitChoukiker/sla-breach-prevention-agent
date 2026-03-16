def calculate_breach_probability(priority, similar_count):

    priority_weight = {
        "low": 0.1,
        "medium": 0.4,
        "high": 0.7,
        "critical": 0.95
    }

    base = priority_weight.get(priority, 0.3)

    history_signal = min(similar_count * 0.05, 0.30)

    probability = base + history_signal

    return min(probability, 1.0)


def combine_scores(rule_prob, ml_prob):

    if ml_prob is None:
        return rule_prob

    # safer risk strategy
    return max(rule_prob, ml_prob)


def calculate_priority(prob):

    if prob >= 0.85:
        return "P1"
    elif prob >= 0.65:
        return "P2"
    elif prob >= 0.45:
        return "P3"
    else:
        return "P4"