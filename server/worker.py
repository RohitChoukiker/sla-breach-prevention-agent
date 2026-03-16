from database import SessionLocal
from module.ai_engine.engine import AIEngine
from models.ticket import Ticket



def process_ticket_job(ticket_id: str):

    db = SessionLocal()

    try:
        ticket = db.query(Ticket).filter(
            Ticket.id == ticket_id
        ).first()

        if not ticket:
            print("Ticket not found")
            return

        # 🔥 Prevent duplicate processing
        if ticket.processing_status == "completed":
            print("Already processed")
            return

        # 🔥 Mark as processing
        ticket.processing_status = "processing"
        db.commit()

        # Run AI Engine
        engine = AIEngine()
        engine.process_ticket(db, ticket_id)

        # 🔥 Mark as completed
        ticket.processing_status = "completed"
        db.commit()

        print(f"AI processed ticket {ticket_id}")

    except Exception as e:
        print("AI processing failed:", e)
        db.rollback()

    finally:
        db.close()
