from fastapi import FastAPI
from celery_worker import create_long_task
from pydantic import BaseModel


class Order(BaseModel):
    name: str
    count: int
# Create FastAPI app
app = FastAPI()

# Create order endpoint
@app.post('/create-task')
def create_task(item: Order):
    #create_order.delay(item.name, item.count)
    async_task = create_long_task.apply_async((item.name, item.count))

    async_task_backend = async_task.backend
    async_task_id = async_task.id
    async_res = async_task_backend.get_result(async_task_id)
    async_status = async_task_backend.get_state(async_task_id)
    async_task_backend.store_result(async_task_id, async_res, async_status)

    #task_process_notification.delay()
    return {"message": "Task created", "task_id": async_task_id}