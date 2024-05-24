from rest_framework import serializers

from .models import *


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        exclude = ['id']


class UserEquipmentSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = UserEquipment
        fields = ['user', 'equipment']


class ProfileUserSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = UserEquipment
        fields = ['equipment']
