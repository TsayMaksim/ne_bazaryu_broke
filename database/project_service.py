from database import get_db
from database.models import Project

def create_project_db(user_id, name, description=None):
    db = next(get_db())
    new_project = Project(owner_id=user_id, name=name, description=description)
    db.add(new_project)
    db.commit()
    return True

def get_user_projects_db(user_id):
    db = next(get_db())
    projects = db.query(Project).filter_by(owner_id=user_id).all()
    return projects

def get_exact_project_db(project_id):
    db = next(get_db())
    exact_project = db.query(Project).filter_by(id=project_id).first()
    return exact_project

def get_all_projects_db():
    db = next(get_db())
    all_projects = db.query(Project).all()
    return all_projects

def update_project_db(project_id, change_info, new_info):
    db = next(get_db())
    update_project = db.query(Project).filter_by(id=project_id).first()
    if update_project:
        if hasattr(update_project, change_info):
            setattr(update_project, change_info, new_info)
            db.commit()
            return True
    return False

def delete_project_db(project_id):
    db = next(get_db())
    delete_project = db.query(Project).filter_by(id=project_id).first()
    if delete_project:
        db.delete(delete_project)
        db.commit()
        return True
    return False
