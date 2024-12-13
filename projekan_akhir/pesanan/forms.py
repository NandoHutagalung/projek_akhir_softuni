from django import forms
from .models import Pesanan, DetailPesanan

class PesananForm(forms.ModelForm): 
    class Meta:
        model = Pesanan
        fields = ['user', 'meja', 'durasi_meja']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Menambahkan kelas Bootstrap untuk setiap field
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['meja'].widget.attrs.update({'class': 'form-select'})
        self.fields['durasi_meja'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan Durasi Pemesanan'})

class DetailPesananForm(forms.ModelForm):
    class Meta:
        model = DetailPesanan
        fields = ['menu', 'jumlah']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Menambahkan kelas Bootstrap pada setiap field
        self.fields['menu'].widget.attrs.update({'class': 'form-select'})
        self.fields['jumlah'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan jumlah'})
