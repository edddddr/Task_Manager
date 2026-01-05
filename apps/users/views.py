# import json
# import logging

# from django.contrib.auth import authenticate, login, logout
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST

# from apps.users.models import User
# from common.decorators import ajax_login_required

# # from ratelimit.decorators import ratlimiter pip v3.11

# logger = logging.getLogger(__name__)

# # logger.info("docker_logging_test")


# @csrf_exempt
# def register(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST required"}, status=405)

#     data = json.loads(request.body)

#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")
#     first_name = data.get("first_name")
#     last_name = data.get("last_name")
#     role = data.get("role")

#     if (
#         not username
#         or not email
#         or not password
#         or not first_name
#         or not last_name
#         or not role
#     ):
#         return JsonResponse(
#             {"status": "error", "message": "You missed one of the fields"}, status=400
#         )

#     if User.objects.filter(username=username).exists():
#         return JsonResponse(
#             {"status": "error", "message": "Username already exists"}, status=400
#         )

#     user = User.objects.create_user(
#         username=username,
#         email=email,
#         password=password,
#         first_name=first_name,
#         last_name=last_name,
#         role=role,
#     )

#     return JsonResponse(
#         {
#             "status": "success",
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "role": user.role,
#             },
#         },
#         status=201,
#     )


# # @ratelimit(key="ip", rate="5/m", block=True) pip v3.11
# @csrf_exempt
# @require_POST
# def login_view(request):

#     data = json.loads(request.body)
#     ip = request.META.get("REMOTE_ADDR")

#     username = data.get("username")
#     password = data.get("password")
#     print("working - - -")

#     user = authenticate(request, username=username, password=password)
#     if user is None:
#         print("No user")
#         logger.warning(
#             "login_failed",
#             extra={
#                 "username": username,
#                 "ip": ip,
#             },
#         )
#         return JsonResponse(
#             {"status": "error", "message": "Invalid credentials"}, status=401
#         )

#     login(request, user)
#     logger.info(
#         "user_login",
#         extra={
#             "user_id": user.id,
#             "ip": ip,
#         },
#     )

#     return JsonResponse({"status": "success", "message": "Logged in successfully"})


# @csrf_exempt
# @ajax_login_required
# @require_POST
# def logout_view(request, user_id):
#     logout(request)
#     logger.info(
#         "user_login",
#         extra={
#             "user_id": user_id,
#             "ip": request.META.get("REMOTE_ADDR"),
#         },
#     )
#     return JsonResponse({"status": "success", "message": "Logged out successfully"})


# @csrf_exempt
# # @ajax_login_required
# def user_list(request):
#     users = User.objects.all().values(
#         "id", "username", "email", "first_name", "last_name", "role"
#     )
#     return JsonResponse(list(users), safe=False)



from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
