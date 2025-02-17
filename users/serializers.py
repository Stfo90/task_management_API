from rest_framework import serializers
from tasks.serializers import TaskSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    #Serializer for user registration and details
    password = serializers.CharField(write_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'created_at')
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
