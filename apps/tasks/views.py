import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from core.decorators import ajax_login_required
from core.permissions import can_delete_task, can_edit_task, is_admin, is_manager

from .models import Task
from apps.projects.models import Project




@ajax_login_required
@csrf_exempt
def task_list_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "GET":
        tasks = Task.objects.for_project(project).with_assignee()
        return JsonResponse(
            {
                "status": "success",
                "tasks": [task.to_dict() for task in tasks],
            },
            status=200
        )

    elif request.method == "POST":
        if not is_admin(request.user) or not is_manager(request.user): # confirm the crater is weather the admin or manager
            return JsonResponse({"message": "Permission denied"}, status=403)
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
        if not can_edit_task(request.user, task):
             return JsonResponse({"message": "Permission denied"}, status=403)

        body = json.loads(request.body)
        task.update_task(body)

        return JsonResponse(
            {"status": "success", "task": task.to_dict()},
            status=200
        )

    elif request.method == "DELETE":
        if not can_delete_task(request.user, task):
            return JsonResponse({"message": "Permission denied"}, status=403)
        task.delete()
        return JsonResponse(
            {"status": "success", "message": "Task deleted"},
            status=200
        )

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])



# from django.contrib.auth import get_user_model

# User = get_user_model()

# assigned_to = User.objects.get(id=body["assigned_to"])