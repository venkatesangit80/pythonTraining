from celery import Celery

celery = Celery(
    "executor",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

meta = {"request_id": "1234", "source": "executor"}
data = {"resource_id": "vm-567", "metrics": ["cpu.usage", "mem.usage"]}

# Example: calling get_ccr_kind_tasks
res = celery.send_task(
    "vrops_tasks.get_ccr_kind_tasks",  # exact name from worker
    args=[meta, data]
)
