from django.http import JsonResponse
from functools import wraps

def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Return your custom JSON response with a 401 (Unauthorized) status
            return JsonResponse(
                {
                 'status': 'fail', 
                 'message': 'You must be logged in to perform this action.'}, 
                status=401
            )
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"detail": "Authentication required"}, status=401)

            if request.user.role not in roles:
                return JsonResponse({"detail": "Permission denied"}, status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator