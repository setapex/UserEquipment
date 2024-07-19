from django.urls import path

from front.views import EquipmentTemplateView, EquipmentFormView, UserEquipmentFormView, ProfileTemplateView

urlpatterns = [
    path('equipment/', EquipmentTemplateView.as_view(), name='equipment_list'),
    path('equipment/add/', EquipmentFormView.as_view(), name='post_equipment'),
    path('equipment/pair/', UserEquipmentFormView.as_view(), name='user_equipment'),
    path('profile/', ProfileTemplateView.as_view(), name='profile_user'),
]
