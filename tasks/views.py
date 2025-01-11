from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    
    #ViewSet for managing tasks
    #Includes filtering, sorting, and task completion functionality
    
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        #Return only tasks belonging to the current user
        return Task.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        #Toggle task completion status
        task = self.get_object()
        task.status = 'COMPLETED' if task.status == 'PENDING' else 'PENDING'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
