from fastapi import APIRouter
from database.task_service import *
from api import result_message
from database.tg_service import *
from pydantic import BaseModel

task_router = APIRouter(prefix='/task', tags=['Задачи'])

class AssignTaskRequest(BaseModel):
    task_id: int
    user_id: int

@task_router.post("/assign")
def assign_task(data: AssignTaskRequest):
    try:
        result = assign_task_to_user(task_id=data.task_id, user_id=data.user_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Произошла ошибка: {str(e)}"
        )

@task_router.post('/create_task')
async def create_task(project_id: int, title: str, completed: bool, description: str = None, due_date: str = None):
    result = create_task_db(project_id=project_id, title=title, completed=completed, description=description, due_date=due_date)
    return result_message(result)

@task_router.get('/get_all_tasks')
async def get_all_tasks():
    result = get_all_tasks_db()
    return result_message(result)

@task_router.get('/get_exact_task')
async def get_exact_task(task_id: int):
    result = get_exact_task_db(task_id=task_id)
    return result_message(result)

@task_router.put('/update_task')
async def update_task(task_id: int, change_info: str, new_info: str):
    result = update_task_db(task_id=task_id, change_info=change_info, new_info=new_info)
    return result_message(result)

@task_router.delete('/delete_task')
async def delete_task(task_id: int):
    result = delete_task_db(task_id=task_id)
    return result_message(result)

@task_router.get('/get_project_tasks')
async def get_project_tasks(project_id: int):
    result = get_project_tasks_db(project_id=project_id)
    return result_message(result)

@task_router.post("/{task_id}/assign-users")
def assign_users(task_id: int, user_ids: list[int]):
    task = assign_users_to_task(task_id, user_ids)
    return {"message": "Пользователи успешно добавлены", "task": {"id": task.id, "title": task.title, "assignees":
        [user.id for user in task.assignees]}}

@task_router.post("/{task_id}/remove-users")
def remove_users(task_id: int, user_ids: list[int]):
    task = remove_users_from_task(task_id, user_ids)
    return {"message": "Пользователи успешно удалены", "task": {"id": task.id, "title": task.title, "assignees":
        [user.id for user in task.assignees]}}

@task_router.post("/tasks/{task_id}/notify/{user_id}")
async def send_task_notification(task_id: int, user_id: int):
    try:
        send_task_to_user(task_id, user_id)
        return {"status": "success", "message": "Уведомление о задаче отправлено."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
