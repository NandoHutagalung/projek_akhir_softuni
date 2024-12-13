from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from meja_biliar.models import MejaBiliar
from menu.models import Menu  # Ganti dengan nama model Menu Anda
from users.models import User 
from pesanan.models import Pesanan  # Ganti dengan nama model Pesanan Anda

@login_required
def dashboard(request):
    if request.user.role not in ['admin', 'staff']:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('user_list')  # Atau halaman lain yang sesuai
    
    try:
        # Ambil data dari masing-masing model
        meja_biliar_count = MejaBiliar.objects.count()
        menu_count = Menu.objects.count()
        user_count = User.objects.count()
        pesanan_count = Pesanan.objects.count()

        # Data yang akan ditampilkan di dashboard
        context = {
            'meja_biliar_count': meja_biliar_count,
            'menu_count': menu_count,
            'user_count': user_count,
            'pesanan_count': pesanan_count,
        }

        return render(request, 'dashboard/dashboard.html', context)

    except Exception as e:
        messages.error(request, f"An error occurred while loading the dashboard: {str(e)}")
        return redirect('user_list')  # Redirect jika ada error

