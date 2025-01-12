from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Task(models.Model):
    """Model for managing tasks"""
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['due_date', 'priority']

    def __str__(self):
        return self.title

    def clean(self):
        """Validate that due date is in the future"""
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError('Due date must be in the future')

    def save(self, *args, **kwargs):
        """Update completed_at timestamp when status changes to completed"""
        if self.status == 'COMPLETED' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status == 'PENDING':
            self.completed_at = None
        super().save(*args, **kwargs)
