import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from core.decorators import ajax_login_required
from .models import Project
from apps.users.models import User

# List & Create Projects
@ajax_login_required
@csrf_exempt 
def project_list_create(request):

    if request.method == "GET":
        projects = Project.objects.all()
        data = [project.to_dict() for project in projects] # List a projects wiht custome an instance method
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
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
        project.delete()
        return JsonResponse({"status" : "sucess", "message":"Project was deleted successfully"}, status=200)
    else:
        return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])
