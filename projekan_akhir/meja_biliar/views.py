from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import MejaBiliar
from .forms import MejaBiliarForm

def is_admin_or_staff(user):
    return user.role in ['admin', 'staff']

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin_or_staff)
def meja_list(request):
    try:
        meja_biliars = MejaBiliar.objects.values('id', 'no_meja', 'harga_siang', 'harga_malam', 'status')
        return JsonResponse({'success': True, 'data': list(meja_biliars)})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@user_passes_test(is_admin_or_staff)
def index(request):
    return render(request, 'meja_biliar/meja_list.html')


@login_required
@user_passes_test(is_admin)
@csrf_exempt
def meja_create(request):
    try:
        if request.method == 'POST':
            form = MejaBiliarForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'New billiard table created successfully'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@csrf_exempt
def meja_delete(request, meja_id):
    try:
        meja = get_object_or_404(MejaBiliar, id=meja_id)
        meja.delete()
        return JsonResponse({'success': True, 'message': 'Billiard table deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@login_required
@user_passes_test(is_admin_or_staff)
@csrf_exempt
def update_status_meja(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Ambil data dari request POST
            meja_id = request.POST.get('id')
            new_status = request.POST.get('status')

            # Validasi keberadaan meja
            meja = get_object_or_404(MejaBiliar, id=meja_id)

            # Update status meja
            meja.status = new_status
            meja.save()

            # Kirim respons berhasil
            return JsonResponse({
                'success': True,
                'message': f'Status meja {meja.no_meja} berhasil diperbarui menjadi {new_status}.'
            })
        except Exception as e:
            # Kirim respons gagal jika terjadi kesalahan
            return JsonResponse({
                'success': False,
                'message': f'Gagal memperbarui status meja: {str(e)}'
            })
    else:
        # Kirim respons gagal jika metode bukan POST atau bukan AJAX
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method or not an AJAX request.'
        })

    