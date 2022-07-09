from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
import os
from django.core.exceptions import ValidationError

from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
# Create your models here.


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# def email_exist(value):
#     if User.objects.filter(email=value).exists():
#         raise ValidationError('A profile with this Email Address already exists')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', validators=[
                              validate_file_extension], upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    signup_confirmation = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

#     instance.profile.save()

class Image(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(
        validators=[validate_file_extension], upload_to='images', null=False, blank=False)
    user = models.CharField(max_length=100, null=False, blank=False)
    profile = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    like = models.IntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return f'{self.name} {self.user}'

    def get_absolute_url(self):
        return reverse("image_detail", kwargs={"pk": str(self.pk)}) # args = [str(self.id)]


class Comment(models.Model):
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True, blank=False)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['commented_at']

    def __str__(self) -> str:
        return f'Comment {self.text} by {self.user} with email ID: {self.email}'
