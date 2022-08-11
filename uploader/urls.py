from django.urls import path

from .views import *
# from django.contrib.auth import views as authviews

urlpatterns = [
    path('', index, name='home'),
    path('uploader/', image_uploader, name='imageuploader'),
    path('profile/', profile_update, name='profile-update'),
    path('profile/<str:user>/', user_profile, name='user-profile'),
    path('like/<int:pk>/', image_like, name='image-like'),
    path('<int:pk>/', image_detail, name='image-comment'),
    
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('sent/', activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('sendemail/', email, name='send-email'),
]
