from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Pesanan, DetailPesanan
from .forms import PesananForm, DetailPesananForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404


from menu.models import Menu



@login_required
def list_pesanan(request):
    pesanan_list = Pesanan.objects.all().select_related('meja', 'user')
    return render(request, 'pesanan/list_pesanan.html', {'pesanan_list': pesanan_list})

# Membuat formset untuk DetailPesanan
DetailPesananFormSet = inlineformset_factory(
    Pesanan, DetailPesanan, form=DetailPesananForm, extra=10, can_delete=True, max_num=10
)

@login_required
def add_pesanan(request):
    if request.method == 'POST':
        # Memproses form utama (Pesanan)
        pesanan_form = PesananForm(request.POST)
        formset = DetailPesananFormSet(request.POST)

        if pesanan_form.is_valid() and formset.is_valid():
            pesanan = pesanan_form.save(commit=False)
            pesanan.user = request.user 
            pesanan.save()
            details = formset.save(commit=False)
            for detail in details:
                detail.pesanan = pesanan  # Menghubungkan DetailPesanan dengan Pesanan
                detail.save()

            # Menghitung total harga setelah detail pesanan disimpan
            pesanan.hitung_total_harga()

            return redirect('list_pesanan')  # Redirect ke halaman list pesanan
    else:
        pesanan_form = PesananForm()
        formset = DetailPesananFormSet()

    return render(request, 'pesanan/add_pesanan.html', {
        'pesanan_form': pesanan_form,
        'formset': formset,
    })

@login_required
def edit_pesanan(request, pk):
    # Ambil pesanan berdasarkan pk
    pesanan = get_object_or_404(Pesanan, pk=pk)

    # Buat formset untuk DetailPesanan, dengan extra form kosong untuk menambah detail baru
    DetailPesananFormSet = modelformset_factory(DetailPesanan, form=DetailPesananForm, extra=5, can_delete=True)

    if request.method == "POST":
        # Ambil form dan formset dari data POST
        pesanan_form = PesananForm(request.POST, instance=pesanan)
        formset = DetailPesananFormSet(request.POST, queryset=pesanan.detail_pesanan.all())

        if pesanan_form.is_valid() and formset.is_valid():
            # Simpan perubahan pada form pesanan
            pesanan_form.save()

            # Proses penyimpanan detail pesanan
            for form in formset:
                if form.cleaned_data:
                    detail = form.save(commit=False)

                    if form.cleaned_data.get('DELETE'):  # Jika ditandai untuk dihapus
                        detail.delete()
                    else:
                        # Menyimpan detail pesanan dan menghubungkannya ke pesanan
                        if not detail.pesanan:  # Jika belum terhubung ke pesanan
                            detail.pesanan = pesanan
                        detail.save()

            # Menyimpan relasi Many-to-Many (jika perlu)
            pesanan.detail_pesanan.set([form.instance for form in formset if form.cleaned_data])

            # Menampilkan pesan sukses
            messages.success(request, "Pesanan berhasil diperbarui!")
            return redirect('list_pesanan')  # Redirect ke halaman list pesanan

        else:
            messages.error(request, "Terdapat kesalahan dalam form. Silakan coba lagi.")
            print(pesanan_form.errors)
            print(formset.errors)

    else:
        pesanan_form = PesananForm(instance=pesanan)
        formset = DetailPesananFormSet(queryset=pesanan.detail_pesanan.all())

    return render(request, 'pesanan/edit_pesanan.html', {
        'pesanan_form': pesanan_form,
        'formset': formset,
        'pesanan': pesanan,
    })
@login_required
def delete_pesanan(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    pesanan.batal_pesanan()
    return redirect('list_pesanan')
