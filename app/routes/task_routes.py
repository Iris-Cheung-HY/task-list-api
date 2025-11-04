from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from ..db import db

bp = Blueprint("tasks_bp",  __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@bp.get("")
def get_all_task():
    query = db.select(Task)
    
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
    
    complete_param = request.args.get("is_completed")
    if complete_param:
        query = query.where(Task.completed_at == None)
    
    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@bp.get()

    

    
