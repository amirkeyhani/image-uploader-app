from django.urls import path
from .views import *

urlpatterns = [
    path('images/', ImageList.as_view(), name="image-list"),
   	path('images/<int:pk>/detail', ImageDetail.as_view(), name="image-detail"),
   	path('images', ImageCreate.as_view(), name="image-create"),
   	path('images/<int:pk>/', ImageUpdate.as_view(), name="image-update"),
   	path('images/<int:pk>/', ImageDelete.as_view(), name="image-delete"),
    
    path('comments/', CommentList.as_view(), name="comment-list"),
   	path('comments/<int:pk>/detail', CommentDetail.as_view(), name="comment-detail"),
   	path('comments', CommentCreate.as_view(), name="comment-create"),
   	path('comments/<int:pk>/', CommentUpdate.as_view(), name="comment-update"),
   	path('comments/<int:pk>/', CommentDelete.as_view(), name="comment-delete"),
    
    path('profiles/', ProfileList.as_view(), name="profile-list"),
   	path('profiles/<int:pk>/detail', ProfileDetail.as_view(), name="profile-detail"),
   	path('profiles', ProfileCreate.as_view(), name="profile-create"),
   	path('profiles/<int:pk>/', ProfileUpdate.as_view(), name="profile-update"),
   	path('profiles/<int:pk>/', ProfileDelete.as_view(), name="profile-delete"),
    
    path('users/', UserAPI.as_view()),
    path('signup/', SignupAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
]