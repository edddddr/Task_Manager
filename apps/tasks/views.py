import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from core.decorators import ajax_login_required

from .models import Task
from apps.projects.models import Project
from apps.users.models import User


@ajax_login_required
@csrf_exempt
def task_list_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "GET":
        tasks = project.tasks.all()
        data = [{"status" : "success"}]
        for task in tasks:
            data.append({
               
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "assigned_to": task.assigned_to.id if task.assigned_to else None,
                "due_date": task.due_date,
                "created_at": task.created_at,
                "updated_at": task.updated_at

            })
        return JsonResponse(data, safe=False, status=200)

    elif request.method == "POST":
        body = json.loads(request.body)

        assigned_to = None
        if body.get("assigned_to"):
            assigned_to = User.objects.get(id=body["assigned_to"])

        task = Task.objects.create(
            title=body["title"],
            description=body.get("description", ""),
            status=body.get("status", "todo"),
            priority=body.get("priority", "medium"),
            project=project,
            assigned_to=assigned_to,
            due_date=body.get("due_date")
        )

        return JsonResponse(
            {
            "status" : "seccess",
            "task":{
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                }
            }, 
            status=201
            )
    

    return HttpResponseNotAllowed(["GET", "POST"])


@ajax_login_required
@csrf_exempt
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "GET":
        return JsonResponse(
            {"status": "success",
            "task" :{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "project": task.project.id,
            "assigned_to": task.assigned_to.id if task.assigned_to else None,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }}, status=200)

    elif request.method in ["PUT", "PATCH"]:
        body = json.loads(request.body)

        task.title = body.get("title", task.title)
        task.description = body.get("description", task.description)
        task.status = body.get("status", task.status)
        task.priority = body.get("priority", task.priority)

        if "assigned_to" in body:
            task.assigned_to = (
                User.objects.get(id=body["assigned_to"])
                if body["assigned_to"]
                else None
            )

        task.save()

        return JsonResponse({"detail": "Task updated"})

    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({"detail": "Task deleted"})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])