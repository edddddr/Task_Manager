# import json
# import logging

# from django.core.cache import cache
# from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt

# from apps.projects.services import ProjectService
# from apps.system.models.activity_log import ActivityLog
# from common.decorators import ajax_login_required
# from common.permissions import is_admin

# from .models.project import Project

# logger = logging.getLogger("task_manager")


# @ajax_login_required
# @csrf_exempt
# def project_list_create(request):

#     cached_project = cache.get("projects_list")
#     if request.method == "GET":
#         if cached_project:
#             return JsonResponse(cached_project, safe=False)
#         projects = Project.objects.for_user(request.user).with_tasks()

#         data = [
#             project.to_dict() for project in projects
#         ]  # List a projects wiht custome an instance method
#         cache.set("projects_list", data, timeout=60 * 10)
#         return JsonResponse(data, safe=False)

#     elif request.method == "POST":
#         try:
#             body = json.loads(request.body)

#             project = ProjectService.create_project(user=request.user, data=body)
#             cache.delete("projects_list")

#             return JsonResponse(
#                 {"status": "success", "project": project.to_dict()}, status=201
#             )

#         except PermissionError as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=403)

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=400)

#     return HttpResponseNotAllowed(["GET", "POST"])


# @ajax_login_required
# @csrf_exempt
# def project_detail(request, project_id):
#     project = get_object_or_404(Project.objects.for_user(request.user), id=project_id)

#     if request.method == "GET":
#         return JsonResponse(
#             project.to_dict()
#         )  # List a project wiht custome instance method

#     elif request.method in ["PUT", "PATCH"]:
#         try:
#             body = json.loads(request.body)
#             ProjectService.update_project(project=project, user=request.user, data=body)
#             cache.delete("projects_list")
#             return JsonResponse(
#                 {"status": "success", "project": project.to_dict()}, status=200
#             )
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=400)

#     elif request.method == "DELETE":
#         user = request.user
#         if not is_admin(user):  # confirm the acter is weather the admin or the manager
#             return JsonResponse({"message": "Permission denied"}, status=403)
#         print("\n")
#         print("\n")
#         print("\n")
#         logger.info(
#             "project_deleted",
#             extra={
#                 "project_id": project.id,
#                 "user_id": user.id,
#             },
#         )
#         project.delete()

#         return JsonResponse(
#             {"status": "sucess", "message": "Project was deleted successfully"},
#             status=200,
#         )
#     else:
#         return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


# @ajax_login_required
# def project_activity(request, project_id):
#     if request.method != "GET":
#         return HttpResponseNotAllowed(["GET"])

#     project = get_object_or_404(Project, id=project_id)
#     logs = ActivityLog.objects.filter(project=project).order_by("-created_at")
#     data = [log.to_dict() for log in logs]
#     return JsonResponse({"status": "success", "activity": data}, safe=False, status=200)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.projects.models.project import Project
from apps.projects.serializers import ProjectSerializer
from apps.tasks.serializers import TaskSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """
        User can only see projects where they are a member.
        Soft-deleted projects excluded by default manager.
        """
        return Project.objects.filter(members=self.request.user)

    def perform_destroy(self, instance):
        """
        Soft delete instead of hard delete.
        """
        instance.delete()

    
    @action(detail=True, methods=["get", "post"], url_path="tasks")
    def tasks(self, request, pk=None, *args, **kwargs):
        """
        /projects/{project_id}/tasks
        """
        project = self.get_object()

        # Safety: membership already enforced by get_queryset
        if request.method == "GET":
            tasks = project.tasks.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = TaskSerializer(
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)

            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
