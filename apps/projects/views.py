from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.projects.models.project import Project
from apps.projects.pagination import ProjectPagination
from apps.projects.serializers import ProjectSerializer
from apps.tasks.serializers import TaskSerializer
from rest_framework.throttling import ScopedRateThrottle
from apps.projects.permissions.project import (
    IsProjectAdmin, 
    IsProjectMember,
)
from apps.projects.permissions.utils import get_user_role
from apps.projects.models.membership import ProjectRole
from rest_framework.exceptions import PermissionDenied



class ProjectViewSet(ModelViewSet):
    
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProjectPagination

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'projects'   

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsProjectAdmin]
        else:
            permission_classes = [IsAuthenticated, IsProjectMember]

        return [permission() for permission in permission_classes]

    

    def get_queryset(self):
        """
        User can only see projects where they are a member.
        Soft-deleted projects excluded by default manager.
        """
        return Project.objects.filter(members=self.request.user)
    
    def get_throttle_scope(self):
        if self.action == "create":
            return "create_project"
        if self.action in ["update", "partial_update"]:
            return "update_project"
        if self.action == "destroy":
            return "delete_project"
        return None

    def perform_destroy(self, instance):
        """
        Soft delete instead of hard delete.
        """
        instance.delete()

    @action(
    detail=True,
    methods=["get", "post"],
    url_path="tasks",
)
    def tasks(self, request, pk=None, **kargs):
        project = self.get_object()

        role = get_user_role(request.user, project)
        if role is None:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this project.")

        # 🔹 GET → list tasks
        if request.method == "GET":
            tasks = project.tasks.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        # 🔹 POST → create task
        if request.method == "POST":
            if role not in {ProjectRole.ADMIN, ProjectRole.EDITOR}:
                raise PermissionDenied("Insufficient role to create tasks.")

            serializer = TaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
    detail=True,
    methods=["get", "put", "patch", "delete"],
    url_path=r"tasks/(?P<task_id>[^/.]+)",
)
    def task_detail(self, request, pk=None, task_id=None, **kargs):
        project = self.get_object()
        task = project.tasks.get(id=task_id)

        role = get_user_role(request.user, project)

        if role is None:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this project.")

        # 🔹 GET → retrieve task
        if request.method == "GET":
            serializer = TaskSerializer(task)
            return Response(serializer.data)

        # 🔹 UPDATE
        if request.method in ["PUT", "PATCH"]:
            if role not in {ProjectRole.ADMIN, ProjectRole.EDITOR}:
                raise PermissionDenied("You do not have permission to update tasks.")

            serializer = TaskSerializer(
                task,
                data=request.data,
                partial=(request.method == "PATCH"),
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # 🔹 DELETE
        if request.method == "DELETE":
            if role != ProjectRole.ADMIN:
                raise PermissionDenied("You do not have permission to delete tasks.")

            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

                