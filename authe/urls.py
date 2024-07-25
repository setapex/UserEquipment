from django.urls import path, re_path, include

from .views import Logout, Registration, Login

urlpatterns = [
    path('login/',Login.as_view(), name='in'),
    path('logout/', Logout.as_view(), name='out'),
    path('registration/', Registration.as_view(), name='reg'),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^', include('djoser.urls.authtoken')),
]
