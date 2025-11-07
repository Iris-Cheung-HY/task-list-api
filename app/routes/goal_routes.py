from flask import Blueprint, Response, request
from app.models.goal import Goal
from app.models.task import Task
from ..routes.route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)


@bp.get("")
def get_all_goal():
    
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title.ilike(f"%{title_param}%"))
    
    goals = db.session.scalars(query.order_by(Goal.id))
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def create_task_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal.tasks:
        for task in goal.tasks:
            task.goal_id = None
            db.session.commit()

    request_body = request.get_json()
    for id in request_body["task_ids"]:
        query = db.select(Task).where(Task.id == id)
        task = db.session.scalar(query)
        task.goal_id = goal_id

    db.session.commit()

    response = goal.to_dict()
    result = {
        "id": response.get("id"),
        "task_ids": [task.id for task in goal.tasks]
    }
    return result, 200
    

@bp.get("/<goal_id>/tasks")
def get_task_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()

    result = {
        "id":response.get("id"),
        "title":response.get("title"),
        "tasks":[task.to_dict() for task in goal.tasks]
    }

    return result, 200


    



