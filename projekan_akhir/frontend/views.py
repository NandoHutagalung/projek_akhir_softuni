from django.shortcuts import render, redirect, get_object_or_404
from meja_biliar.models import MejaBiliar 
from users.forms import UserUpdateForm
from users.models import User
from pesanan.models import Pesanan, DetailPesanan
from menu.models import Menu
from .forms import PesananForm, DetailPesananForm
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from django.http import Http404
from django.forms import modelformset_factory
from django.http import JsonResponse


def index(request):
    meja_biliars = MejaBiliar.objects.all()
    menu = Menu.objects.all()
    return render(request, 'frontend/index.html', {'meja_biliars': meja_biliars, 'menu': menu})

DetailPesananFormSet = inlineformset_factory(
    Pesanan, DetailPesanan, form=DetailPesananForm, extra=8, can_delete=True, max_num=9
)

@login_required
def add_pesanan(request):
    if request.method == 'POST':
        pesanan_form = PesananForm(request.POST)
        formset = DetailPesananFormSet(request.POST)
        
        try:
            if pesanan_form.is_valid() and formset.is_valid():
                pesanan = pesanan_form.save(commit=False)
                pesanan.user = request.user 
                pesanan.save()

                details = formset.save(commit=False)
                for detail in details:
                    detail.pesanan = pesanan
                    detail.save()

                pesanan.hitung_total_harga()  
                messages.success(request, 'Pesanan anda berhasil, mohon tunggu hubungi petugas kami!')
                return redirect('index')  
            else:
                pesanan_form_errors = pesanan_form.errors
                formset_errors = formset.errors
                messages.error(request, 'Terdapat kesalahan dalam form. Harap periksa kembali. Mungkin meja yang anda pilih saat ini sedang penuh')
                return JsonResponse({'success': False, 'errors': formset.errors})
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')  
            return JsonResponse({'success': False, 'errors': formset.errors})

    else:
        pesanan_form = PesananForm()
        formset = DetailPesananFormSet()

    return render(request, 'frontend/add_pesanan.html', {
        'pesanan_form': pesanan_form,
        'formset': formset,
    })
@login_required
def profile_update(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.id != user.id:
        raise Http404("Anda tidak memiliki izin untuk mengakses halaman ini.")
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil Anda telah diperbarui.")
            return redirect('profile_update', id=user.id)
        else:
            messages.error(request, "Harap perbaiki kesalahan di bawah ini.")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'frontend/profile_update.html', {'form': form, 'user': user})

@login_required
def list_pesanan(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.id != user.id:
        raise Http404("Anda tidak memiliki izin untuk mengakses halaman ini.")
    pesanan_list = Pesanan.objects.filter(user=user).select_related('meja', 'user')

    return render(request, 'frontend/list_pesanan.html', {'pesanan_list': pesanan_list})


@login_required
def edit_pesanan(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    if request.user.id != pesanan.user.id:
        raise Http404("Anda tidak memiliki izin untuk mengakses halaman ini.")
    if request.method == 'POST':
        pesanan_form = PesananForm(request.POST, instance=pesanan)
        formset = DetailPesananFormSet(request.POST, instance=pesanan)
        if pesanan_form.is_valid() and formset.is_valid():
            pesanan = pesanan_form.save(commit=False)
            pesanan.user = request.user 
            pesanan.save()
            details = formset.save(commit=False)
            for detail in details:
                if detail.id is None:
                    detail.pesanan = pesanan
                detail.save()
            pesanan.hitung_total_harga()
            messages.success(request, 'Pesanan berhasil diperbarui.')
            redirect('listpesananuser', id=pesanan.user.id)

        else:
            pesanan_form_errors = pesanan_form.errors
            formset_errors = formset.errors

            errors = {
                'pesanan_form_errors': pesanan_form_errors,
                'formset_errors': formset_errors
            }

            redirect('listpesananuser', id=pesanan.user.id)

    else:
        redirect('listpesananuser', id=pesanan.user.id)
        pesanan_form = PesananForm(instance=pesanan)
        formset = DetailPesananFormSet(instance=pesanan)

    return render(request, 'frontend/edit_pesanan.html', {
        'pesanan_form': pesanan_form,
        'formset': formset,
        'pesanan': pesanan,
    })
