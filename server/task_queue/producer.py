from rq import Queue
from .redis_client import redis_conn
from module.ai_engine.engine import AIEngine
from database import SessionLocal

ticket_queue = Queue(
    "ticket_queue",
    connection=redis_conn,
    default_timeout=300
)

def process_ticket_job(ticket_id: str):

    print(f"[Producer] Processing ticket job for ticket_id: {ticket_id}")
    db = SessionLocal()

    try:
        engine = AIEngine()
        engine.process_ticket(db, ticket_id)
        print(f"[Producer] Ticket job processed for ticket_id: {ticket_id}")
    finally:
        db.close()


def publish_ticket_event(ticket_id: str):

    print(f"[Producer] Publishing ticket event for ticket_id: {ticket_id}")
    job = ticket_queue.enqueue(
        process_ticket_job, 
        ticket_id,           
        job_timeout=600,
        result_ttl=3600
    )
    print(f"[Producer] Ticket event published. Job ID: {job.id}")
    return job.id