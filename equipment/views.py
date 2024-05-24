from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import *
from equipment.serializers import *
from .permissions import *


class EquipmentAPIList(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = (IsAdminUser, )


class UserEquipmentAPIList(generics.ListCreateAPIView):
    queryset = UserEquipment.objects.all()
    serializer_class = UserEquipmentSerializer
    permission_classes = (IsAdminUser, )


class ProfileUserAPIList(generics.ListAPIView):
    queryset = UserEquipment.objects.all()
    serializer_class = ProfileUserSerializer
    permission_classes = (IsOwnerOrAdminReadOnly,)

    def get_queryset(self):
        user = self.kwargs['pk']
        queryset = UserEquipment.objects.filter(user_id=user)
        return queryset

