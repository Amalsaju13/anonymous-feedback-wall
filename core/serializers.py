from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import AdminUser, FeedbackGroup, Feedback

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = AdminUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = AdminUser.objects.create_user(**validated_data)
        return user


class FeedbackGroupSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = FeedbackGroup
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['id', 'submitted_at', 'ip_address', 'is_hidden']
