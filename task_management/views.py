from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def home_view(request):
    """Simple API root endpoint showing available endpoints"""
    return Response({
        'message': 'Welcome to Task Management API',
        'endpoints': {
            'users': '/api/users/',
            'tasks': '/api/tasks/',
            'auth': {
                'login': '/api/token/',
                'refresh': '/api/token/refresh/',
            }
        }
    })