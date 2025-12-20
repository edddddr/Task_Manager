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
        data = [{"status": "success"}]
        for project in projects:
            data.append({
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "created_by": project.created_by.id if project.created_by else None,
                    "members": [user.id for user in project.members.all()],
                    "created_at": project.created_at,
                    "updated_at": project.updated_at
            })
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            project = Project.objects.create(
                name=body.get("name"),
                description=body.get("description", ""),
                created_by=request.user
            )
            return JsonResponse({
                "status": "success",
                "project" : {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "created_by": project.created_by.id,
                    "members": [],
                    "created_at": project.created_at,
                    "updated_at": project.updated_at
                    }
                }, 
                status=201
            )
        except Exception as e:
            return JsonResponse({"status" : "error", "message": str(e)}, status=400)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


# Retrieve, Update, Delete Project
@ajax_login_required
@csrf_exempt
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "GET":
        data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_by": project.created_by.id if project.created_by else None,
            "members": [user.id for user in project.members.all()],
            "created_at": project.created_at,
            "updated_at": project.updated_at,
        }
        return JsonResponse(data)

    elif request.method == "PUT" or request.method == "PATCH":
        try:
            body = json.loads(request.body)
            project.name = body.get("name", project.name)
            project.description = body.get("description", project.description)
            project.save()
            return JsonResponse({
                "status" : "success",
                "project" :{
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "created_by": project.created_by.id if project.created_by else None,
                    "members": [user.id for user in project.members.all()],
                    "created_at": project.created_at,
                    "updated_at": project.updated_at
                    }
            }, status=200)
        except Exception as e:
            return JsonResponse({"status" : "error", "message": str(e)}, status=400)

    elif request.method == "DELETE":
        project.delete()
        return JsonResponse({"status" : "sucess", "message":"Project was deleted successfully"}, status=200)
    else:
        return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])
