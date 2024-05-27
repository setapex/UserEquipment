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

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment')
        equipment = Equipment.objects.create(**equipment_data)
        user_equipment = UserEquipment.objects.create(equipment=equipment, **validated_data)
        return user_equipment

class ProfileUserSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = UserEquipment
        fields = ['equipment']
