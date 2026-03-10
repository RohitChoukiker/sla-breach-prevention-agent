
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

from module.ai_engine.embedding import EmbeddingService
EmbeddingService.load_model()
print("Embedding model preloaded")
EmbeddingService.generate("warmup")
print("Embedding model warmup complete")

from rq import Worker, Queue
from redis import Redis

redis_conn = Redis(
    host="localhost",
    port=6379,
    password="mypassword",
)

queues = ["ticket_queue"]

worker = Worker([Queue(q, connection=redis_conn) for q in queues], connection=redis_conn)

if __name__ == "__main__":
    print("🚀 Worker starting...")
    worker.work(with_scheduler=True)