from rest_framework import serializers
from apps.projects.models.project import Project
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "members",
            "created_at",
            "updated_at",
        ]   
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Ensure creator becomes owner + member
        """
        request = self.context["request"]
        members = validated_data.pop("members", [])

        project = Project.objects.create(
            owner=request.user,
            **validated_data
        )

        project.members.add(request.user, *members)
        return project
