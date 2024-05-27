from django.urls import path

from .views import *

urlpatterns = [
    path('equipment/', get_equipment, name='equipment_list'),
    path('equipment/add/', post_equipment, name='post_equipment'),
    path('equipment/pair/', user_equipment, name='user_equipment'),
    path('profile/', profile_user, name='profile_user'),
    path('login/',login)
]
