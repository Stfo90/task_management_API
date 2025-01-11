from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from users.models import User
from .models import Task

class TaskTests(APITestCase):
    def setUp(self):
        """Create test user and authenticate"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': (timezone.now() + timedelta(days=1)).isoformat(),
            'priority': 'HIGH'
        }

    def test_create_task(self):
        """Test creating a new task"""
        url = reverse('task-list')
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_task_list(self):
        """Test retrieving task list"""
        Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_toggle_complete(self):
        """Test marking task as complete"""
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-toggle-complete', kwargs={'pk': task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'COMPLETED')