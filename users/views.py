from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    #ViewSet for user registration and management
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Allow anyone to register
        Require authentication for other actions
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's details
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)