import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from core.decorators import ajax_login_required, role_required
from core.permissions import can_edit_project, is_admin, is_manager
from .models import Project

# List & Create Projects
@ajax_login_required
# This decoration can be used here, but in the case of getting projects for members have a permission.
# @role_required(["admin", "manager"]) 
@csrf_exempt 
def project_list_create(request):

    if request.method == "GET":
        projects = Project.objects.active().with_tasks()
        data = [project.to_dict() for project in projects] # List a projects wiht custome an instance method
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        if not is_admin(request.user) or not is_manager(request.user): # confirm the crater is weather the admin or manager
            return JsonResponse({"message": "Permission denied"}, status=403)
        try:
            body = json.loads(request.body)

            project = Project.create_project(
                name=body.get("name"),
                description=body.get("description", ""),
                creator=request.user
            ) # Create a project with custome class based method

            return JsonResponse(
                {"status": "success", "project": project.to_dict()},
                status=201
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=400
            )

    return HttpResponseNotAllowed(["GET", "POST"])



# Retrieve, Update, Delete Project
@ajax_login_required
@csrf_exempt
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "GET":
        return JsonResponse(project.to_dict()) #List a project wiht custome instance method


    elif request.method in ["PUT", "PATCH"]:
        if not can_edit_project(request.user, project): # 
            return JsonResponse({"message": "Permission denied"}, status=403)
        try:
            body = json.loads(request.body)
            project.update_project(
                name=body.get("name"),
                description=body.get("description")
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


