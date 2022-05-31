from rest_framework import serializers
from uploader.models import Uploader, Comment, Profile


class UploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uploader
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
