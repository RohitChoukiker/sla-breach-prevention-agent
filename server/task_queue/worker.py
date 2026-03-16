import os
import sys
import multiprocessing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from module.ai_engine.ml_model import load_model


multiprocessing.set_start_method("spawn", force=True)


os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

from module.ai_engine.embedding import EmbeddingService

EmbeddingService.load_model()
print("Embedding model preloaded")

EmbeddingService.generate("warmup")
print("Embedding model warmup complete")


load_model()
print("ML model preloaded")


from rq import SimpleWorker, Queue
from task_queue.redis_client import redis_conn

queues = ["ticket_queue"]

worker = SimpleWorker(
    [Queue(q, connection=redis_conn) for q in queues],
    connection=redis_conn
)


if __name__ == "__main__":
    print("Worker starting...")
    worker.work()