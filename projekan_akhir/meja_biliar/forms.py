from django import forms
from .models import MejaBiliar

class MejaBiliarForm(forms.ModelForm):
    class Meta:
        model = MejaBiliar
        fields = ['no_meja', 'harga_siang', 'harga_malam', 'status']  
        widgets = {
            'status': forms.Select(choices=MejaBiliar.STATUS_CHOICES), 
        }
