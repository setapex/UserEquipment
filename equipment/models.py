from django.contrib.auth.models import User
from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    inventory_number = models.IntegerField()
    nomenclature_number = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

class UserEquipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'equipment')
        #constraints = (
            #models.UniqueTogetherConstraint(
                #fields=('user', 'equipment'),
                #name='user_equipment_unique'
            #),
        #)

    def __str__(self):
        return f'{self.user.username} - {self.equipment.name}'
