from flask import Blueprint, Response, request
import requests
from app.models.task import Task
from datetime import datetime
from ..routes.route_utilities import validate_model, create_model
from ..db import db
import os

bp = Blueprint("tasks_bp",  __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

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
    
    sort_order = request.args.get("sort")
    if sort_order == "asc":
        tasks = db.session.scalars(query.order_by(Task.title.asc()))
    elif sort_order == "desc":
        tasks = db.session.scalars(query.order_by(Task.title.desc()))
    else:
        tasks = db.session.scalars(query.order_by(Task.id))
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.patch("/<task_id>/mark_complete")
def update_completed_at_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.utcnow()

    headers={"Authorization": os.environ.get('SLACKAUTHORIZATION')}
    data = {"channel": "slack-api-testing",
            "text": f"Someone just completed {task.title}"}

    response=requests.post("https://slack.com/api/chat.postMessage",
                        headers=headers,
                        json=data)

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def update_completed_at_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.compelted_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

