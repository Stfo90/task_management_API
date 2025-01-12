from rest_framework.decorators import api_view
from rest_framework.response import Response

# Option 1: If you want to return a JSON response (API style)
@api_view(['GET'])
def home_view(request):
    return Response({
        "message": "Welcome to the Task Manager API",
        "endpoints": {
            "admin": "/admin/",
            "api": {
                "register": "/api/users/register/",
                "login": "/api/token/",
                "tasks": "/api/tasks/",
                "profile": "/api/users/me/"
            },
            "web": {
                "login": "/login/",
                "logout": "/logout/"
            }
        }
    })
