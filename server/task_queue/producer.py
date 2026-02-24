from rq import Queue
from .redis_client import redis_conn

# Create named queue
ticket_queue = Queue(
    "ticket_queue",
    connection=redis_conn,
    default_timeout=300
)

def publish_ticket_event(ticket_id: str):
   
    job = ticket_queue.enqueue(

        ticket_id,
        job_timeout=600,
        result_ttl=3600
    )
    return job.id
