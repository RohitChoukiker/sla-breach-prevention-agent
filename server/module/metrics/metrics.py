from prometheus_client import Counter, Histogram, Gauge


tickets_created_total = Counter(
    "tickets_created_total",
    "Total tickets created"
)

tickets_assigned_total = Counter(
    "tickets_assigned_total",
    "Total tickets assigned to agents"
)

tickets_closed_total = Counter(
    "tickets_closed_total",
    "Total tickets resolved"
)

ai_tickets_processed_total = Counter(
    "ai_tickets_processed_total",
    "Total tickets processed by AI engine"
)

ai_escalations_total = Counter(
    "ai_escalations_total",
    "Total escalations triggered by AI"
)

ai_failures_total = Counter(
    "ai_failures_total",
    "Total AI processing failures"
)



ai_processing_time_seconds = Histogram(
    "ai_processing_time_seconds",
    "Time spent processing ticket in AI engine"
)



redis_health = Gauge(
    "redis_health",
    "Redis connection status (1=healthy, 0=down)"
)

database_health = Gauge(
    "database_health",
    "Database connection status (1=healthy, 0=down)"
)