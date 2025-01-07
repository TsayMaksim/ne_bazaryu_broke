from fastapi import APIRouter
from database.project_service import *
from api import result_message
from database.tg_service import *
from fastapi import HTTPException

project_router = APIRouter(prefix='/project', tags=['Проекты'])

@project_router.post('/create_project')
async def create_project(user_id: int, name: str, description: str = None):
    result = create_project_db(user_id=user_id, name=name, description=description)
    return result_message(result)

@project_router.get('/get_all_projects')
async def get_all_projects():
    result = get_all_projects_db()
    return result_message(result)

@project_router.get('/get_exact_project')
async def get_exact_project(project_id: int):
    result = get_exact_project_db(project_id=project_id)
    return result_message(result)

@project_router.put('/update_project')
async def update_project(project_id: int, change_info: str, new_info: str):
    result = update_project_db(project_id=project_id, change_info=change_info, new_info=new_info)
    return result_message(result)

@project_router.delete('/delete_project')
async def delete_project(project_id: int):
    result = delete_project_db(project_id=project_id)
    return result_message(result)

@project_router.post("/projects/{project_id}/notify/{user_id}")
async def send_project_notification(project_id: int, user_id: int):
    try:
        send_project_to_user(project_id, user_id)
        return {"status": "success", "message": "Уведомление о проекте отправлено."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
