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
        return JsonResponse(
            {
                "status": "success",
                "tasks": [task.to_dict() for task in tasks],
            },
            status=200
        )

    elif request.method == "POST":
        body = json.loads(request.body)
        task = Task.create_task(project=project, data=body)

        return JsonResponse(
            {
                "status": "success",
                "task": task.to_dict(),
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
            {"status": "success", "task": task.to_dict()},
            status=200
        )

    elif request.method in ["PUT", "PATCH"]:
        body = json.loads(request.body)
        task.update_task(body)

        return JsonResponse(
            {"status": "success", "task": task.to_dict()},
            status=200
        )

    elif request.method == "DELETE":
        task.delete()
        return JsonResponse(
            {"status": "success", "message": "Task deleted"},
            status=200
        )

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])
