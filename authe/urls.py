from django.urls import path, re_path, include

from .views import *
from djoser import views

urlpatterns = [
    path('login/',login, name='in'),
    path('logout/', logout, name='out'),
    path('registration/', registration, name='reg'),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^', include('djoser.urls.authtoken')),
]
