from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('login/',login),
    path('logout/', logout),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^', include('djoser.urls.authtoken')),
]
