"""rest_api URL Configuration

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
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api_user import views
import api_user.api

app_name = 'api_user'
router = routers.DefaultRouter()
router.register('test', api_user.api.MemberViewSet)

schema_url_patterns = [
    url(r'^api/v1/', include((router.urls, 'test'), namespace='api')),
    path('test/', views.test, name='test')
]

schema_view = get_schema_view(
    openapi.Info(
        title="API DOCS",
        default_version='v1',
        terms_of_service="https://www.google.com/policies/terms/"),
    public=True,
    permission_classes=(
        permissions.AllowAny,
    ),
    patterns=schema_url_patterns)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='swagger-redoc'),

    url(r'^api/v1/', include((router.urls, 'test'), namespace='api')),
    path('test/<str:upload_img_name>/', views.test, name='test'),
]