from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import EmpaquesUser, Bodega, TIPOS_USUARIO_CHOICES


class BodegaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.__str__()


class EmpaquesUserCreationForm(UserCreationForm):

    bodega = BodegaChoiceField(queryset=Bodega.objects.all(), required=True)
    tipo = forms.ChoiceField(choices=TIPOS_USUARIO_CHOICES)

    class Meta(UserCreationForm):
        model = EmpaquesUser
        fields = [
            'username',
            'bodega',
            'tipo',
        ]


class EmpaquesUserChangeForm(UserChangeForm):

    bodega = BodegaChoiceField(queryset=Bodega.objects.all(), required=True)
    tipo = forms.ChoiceField(choices=TIPOS_USUARIO_CHOICES)


    class Meta(UserChangeForm):
        model = EmpaquesUser
        fields = [
            'username',
            'bodega',
            'tipo',
        ]