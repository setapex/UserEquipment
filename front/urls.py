from django.urls import path

from .views import EquipmentListView, EquipmentCreateView, UserEquipmentCreateView, ProfileListView

urlpatterns = [
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/add/', EquipmentCreateView.as_view(), name='post_equipment'),
    path('equipment/pair/', UserEquipmentCreateView.as_view(), name='user_equipment'),
    path('profile/', ProfileListView.as_view(), name='profile_user'),
]
