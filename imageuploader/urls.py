"""image_uploader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from uploader.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ImageUploader API",
        default_version="v1",
        description="A sample API for ImageUploader WebApp",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

# router = DefaultRouter()
# router.register(r'uploader', UploaderViewSet, 'uploader')
# router.register(r'comment', CommentViewSet, 'comment')
# router.register(r'profile', ProfileViewSet, 'profile')

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('uploader.urls')), 
    path('accounts/', include('allauth.urls')), 
    
    # path('api/', include(router.urls)), 
    path('api/v1/', include('api.urls')), 
    path('api-auth/', include('rest_framework.urls')), 
    
    # path('dj-rest-auth/', include('dj_rest_auth.urls')), 
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), 
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
]

if settings.DEBUG:
            urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
