from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    #Serializer for Task model
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'completed_at')

    def validate_due_date(self, value):
        #Validate that due date is in the future
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future")
        return value
