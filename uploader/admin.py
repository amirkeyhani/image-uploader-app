from django.contrib import admin
from .models import Image, Profile, Comment

# Register your models here.
admin.site.site_header = 'Image Uploader administration'
admin.site.index_title = 'Image_uploader-app administration'
admin.site.site_title = 'Django site admin'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'user', 'profile', 'created_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image']
    # list_display_links = ['user']
    list_editable = ('user',)
    list_filter = ['user']
    search_fields = ['user', 'image']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'image', 'commented_at', 'active']
    list_filter = ['active', 'commented_at']
    search_fields = ['user', 'email', 'text']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
