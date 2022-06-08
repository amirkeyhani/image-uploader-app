from django.urls import path
from .views import *
from rest_framework import views

urlpatterns = [
    path('uploader-list/', UploaderList.as_view(), name="uploader-list"),
   	path('uploader-detail/<int:pk>/', UploaderDetail.as_view(), name="uploader-detail"),
   	path('uploader-create/', UploaderCreate.as_view(), name="uploader-create"),
   	path('uploader-update/<int:pk>/', UploaderUpdate.as_view(), name="uploader-update"),
    path('uploader-patch/<int:pk>/', UploaderUpdate.as_view(), name="uploader-patch"),
   	path('uploader-delete/<int:pk>/', UploaderDelete.as_view(), name="uploader-delete"),
    
    path('comment-list/', CommentList.as_view(), name="comment-list"),
   	path('comment-detail/<int:pk>/', CommentDetail.as_view(), name="comment-detail"),
   	path('comment-create/', CommentCreate.as_view(), name="comment-create"),
   	path('comment-update/<int:pk>/', CommentUpdate.as_view(), name="comment-update"),
    path('comment-patch/<int:pk>/', CommentUpdate.as_view(), name="comment-patch"),
   	path('comment-delete/<int:pk>/', CommentDelete.as_view(), name="comment-delete"),
    
    path('profile-list/', ProfileList.as_view(), name="profile-list"),
   	path('profile-detail/<int:pk>/', ProfileDetail.as_view(), name="profile-detail"),
   	path('profile-create/', ProfileCreate.as_view(), name="profile-create"),
   	path('profile-update/<int:pk>/', ProfileUpdate.as_view(), name="profile-update"),
    path('profile-patch/<int:pk>/', ProfileUpdate.as_view(), name="profile-patch"),
   	path('profile-delete/<int:pk>/', ProfileDelete.as_view(), name="profile-delete"),
    
    path('user/', UserAPI.as_view()),
    path('signup/', SignupAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    # path('logout/', ),
]