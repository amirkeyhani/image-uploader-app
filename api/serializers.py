from rest_framework import serializers
from uploader.models import Image, Comment, Profile

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 
                  'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
        
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        
        return user
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
        
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        # fields = '__all__'
        exclude = ['created_at']


class CommentSerializer(serializers.ModelSerializer):
    def get_user(self, obj):
        return {
            'username': obj.user.username, 
            'first_name': obj.user.first_name, 
            'last_name': obj.user.last_name
        }
    
    image = serializers.CharField(source='image.image', read_only=True)
    user = serializers.SerializerMethodField('get_user')
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['active']


class ProfileSerializer(serializers.ModelSerializer):
    def get_user(self, obj):
        return {
            'username': obj.user.username, 
            'first_name': obj.user.first_name, 
            'last_name': obj.user.last_name, 
            'email': obj.user.email
        }
    
    user = serializers.SerializerMethodField('get_user')
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['signup_confirmation', 'uuid', 'email_verified']
