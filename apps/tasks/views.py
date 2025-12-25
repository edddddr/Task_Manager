import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apps.system.models.activity_log import ActivityLog
from apps.tasks.services import TaskService
from common.decorators import ajax_login_required
from common.permissions import can_delete_task, can_edit_task, is_admin, is_manager

from .models.task import Task
from apps.projects.models.project import Project




@ajax_login_required
@csrf_exempt
def task_list_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "GET":                       
        tasks = Task.objects.for_user(request.user).for_project(project)
        return JsonResponse(
            {
                "status": "success",
                "tasks": [task.to_dict() for task in tasks],
            },
            status=200
        )

    elif request.method == "POST":

        try:
            data = json.loads(request.body)
            task = TaskService.create_task(user =request.user, project=project, data=data)
        
        except PermissionError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=403)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


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
    task = get_object_or_404(Task.objects.for_user(request.user), id=task_id)

    if request.method == "GET":
        return JsonResponse(
            {"status": "success", "task": task.to_dict()},
            status=200
        )

    elif request.method in ["PUT", "PATCH"]:

        data = json.loads(request.body)
        task.update_task(task=task, user=request.user, data=data)

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


@ajax_login_required
def task_activity(request, task_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    task = get_object_or_404(Task, id=task_id)
    logs = ActivityLog.objects.filter(task=task).order_by("-created_at")
    data = [log.to_dict() for log in logs]
    return JsonResponse({"status": "success", "activity": data}, safe=False, status=200)