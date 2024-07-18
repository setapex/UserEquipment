from django import forms
from django.contrib.auth.models import User


class EquipmentForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    inventory_number = forms.IntegerField(label='Inventory Number')
    nomenclature_number = forms.IntegerField(label='Nomenclature Number')


class UserEquipmentForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='User')
    name = forms.CharField(max_length=100, label='Name')
    inventory_number = forms.IntegerField(label='Inventory Number')
    nomenclature_number = forms.IntegerField(label='Nomenclature Number')