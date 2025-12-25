import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from common.decorators import ajax_login_required, role_required
from common.permissions import can_edit_project, is_admin, is_manager
from .models.project import Project
from apps.projects.services import ProjectService
from apps.system.models.activity_log import ActivityLog



@ajax_login_required
@csrf_exempt 
def project_list_create(request):

    if request.method == "GET":
        projects = Project.objects.for_user(request.user).with_tasks()
        data = [project.to_dict() for project in projects] # List a projects wiht custome an instance method
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        try:
            body = json.loads(request.body)

            project =ProjectService.create_project(
                user=request.user,
                data=body
            )

            return JsonResponse(
                {"status": "success", "project": project.to_dict()},
                status=201
            )

        except PermissionError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=403)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return HttpResponseNotAllowed(["GET", "POST"])



@ajax_login_required
@csrf_exempt
def project_detail(request, project_id):
    project = get_object_or_404(Project.objects.for_user(request.user), id=project_id)

    if request.method == "GET":
        return JsonResponse(project.to_dict()) #List a project wiht custome instance method


    elif request.method in ["PUT", "PATCH"]:
        try:
            body = json.loads(request.body)
            ProjectService.update_project(
                project=project,
                user=request.user,
                data=body
            )
            return JsonResponse(
                {"status": "success", "project": project.to_dict()},
                status=200  
            )
        except Exception as e:
            return JsonResponse({"status" : "error", "message": str(e)}, status=400)

    elif request.method == "DELETE":
        if not is_admin(request.user): # confirm the crater is weather the admin or manager
            return JsonResponse({"message": "Permission denied"}, status=403)

        project.delete()

        return JsonResponse({"status" : "sucess", "message":"Project was deleted successfully"}, status=200)
    else:
        return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


@ajax_login_required
def project_activity(request, project_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    project = get_object_or_404(Project, id=project_id)
    logs = ActivityLog.objects.filter(project=project).order_by("-created_at")
    data = [log.to_dict() for log in logs]
    return JsonResponse({"status": "success", "activity": data}, safe=False, status=200)