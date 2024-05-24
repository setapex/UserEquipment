from django.urls import path

from equipment.views import *

urlpatterns = [
    path('equipment/', EquipmentAPIList.as_view()),
    path('user/equipment/', UserEquipmentAPIList.as_view()),
    #path('equipment/<int:pk>/', EquipmentAPIDetailView.as_view()),
    path('profile/<int:pk>/', ProfileUserAPIList.as_view())
]
