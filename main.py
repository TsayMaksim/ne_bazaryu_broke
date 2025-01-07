from fastapi import FastAPI
from database import Base, engine
from api.project_routes import project_router
from api.task_routes import task_router
from api.user_routes import user_router

Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url="/")

app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
