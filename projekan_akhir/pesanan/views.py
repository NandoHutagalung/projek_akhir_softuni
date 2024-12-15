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
    pesanan = get_object_or_404(Pesanan, pk=pk)
    if request.method == 'POST':
        pesanan_form = PesananForm(request.POST, instance=pesanan)
        formset = DetailPesananFormSet(request.POST, instance=pesanan)
        if pesanan_form.is_valid() and formset.is_valid():
            pesanan = pesanan_form.save(commit=False)
            pesanan.user = pesanan.user
            pesanan.save()
            details = formset.save(commit=False)
            for detail in details:
                if detail.id is None:
                    detail.pesanan = pesanan
                detail.save()
            pesanan.hitung_total_harga()
            messages.success(request, 'Pesanan berhasil diperbarui.')
            redirect('list_pesanan')

        else:
            pesanan_form_errors = pesanan_form.errors
            formset_errors = formset.errors

            errors = {
                'pesanan_form_errors': pesanan_form_errors,
                'formset_errors': formset_errors
            }

            redirect('list_pesanan')

    else:
        redirect('list_pesanan')
        pesanan_form = PesananForm(instance=pesanan)
        formset = DetailPesananFormSet(instance=pesanan)

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
