import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_login_required
from django.views.decorators.http import require_POST
from apps.users.models import User


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    role = data.get("role")

    if not username or not email or not password or not first_name or not last_name:
        return JsonResponse(
            {'status': 'error', 'message': 'You missed one of the fields'}, status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"status" : "error", "message": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role
    )

    return JsonResponse({
        "status" : "success",
        'user' : {
            "id": user.id,
            "username": user.username,
            "email": user.email, 
            "role": user.role,
            }
            }, 
            status=201
        )




@csrf_exempt
@require_POST
def login_view(request):

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)

    login(request, user)

    return JsonResponse({'status': 'success', 'message': 'Logged in successfully'})



@ajax_login_required
@require_POST
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})


# @ajax_login_required
@csrf_exempt
def user_list(request):
    users = User.objects.all().values(
        "id", "username", "email", "first_name", "last_name", "role"
    )
    return JsonResponse(list(users), safe=False)
