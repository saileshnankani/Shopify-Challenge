"""backend URL Configuration

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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from repository.views import image_view, success, display_images, login, create
from graphene_django.views import GraphQLView
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from repository.auth import PrivateGraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', RedirectView.as_view(url='/gallery/')),
    re_path(r'^upload/$', csrf_exempt(image_view), name = 'image_upload'), 
    re_path(r'^login', csrf_exempt(auth_views.LoginView.as_view()), {'next_page': '/gallery'}, name = 'login'), 
    re_path(r'^logout', csrf_exempt(auth_views.LogoutView.as_view()), name = 'logout'), 
    re_path(r'^signup/$', csrf_exempt(create), name = 'create'), 
    re_path(r'^gallery/$', csrf_exempt(display_images), name = 'gallery'),
    re_path(r'^graphql/$', csrf_exempt(PrivateGraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
