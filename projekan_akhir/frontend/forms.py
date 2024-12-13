from django import forms
from menu.models import Menu
from pesanan.models import Pesanan, DetailPesanan

class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['meja', 'durasi_meja']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        self.fields['meja'].widget.attrs.update({'class': 'form-select'})
        self.fields['durasi_meja'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan Durasi Pemesanan'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user 
        if commit:
            instance.save()
        return instance


class DetailPesananForm(forms.ModelForm):
    class Meta:
        model = DetailPesanan
        fields = ['menu', 'jumlah']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu'].widget.attrs.update({'class': 'form-select'})
        self.fields['jumlah'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan jumlah'})
