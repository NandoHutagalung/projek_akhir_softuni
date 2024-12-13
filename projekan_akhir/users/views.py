from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from .models import User

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        else:
            form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred during registration: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'register'))


def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Validasi username dan password
            if not username:
                messages.error(request, "Username is required.")
                return redirect('login')
            if not password:
                messages.error(request, "Password is required.")
                return redirect('login')

            # Autentikasi pengguna
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name()}!")

                # Pemeriksaan role dan pengalihan halaman
                if user.role in ['admin', 'staff']:
                    return redirect('user_list')  # Halaman yang sama untuk admin dan staff
                elif user.role == 'member':
                    return redirect('index')  # Halaman khusus untuk member

                return redirect('user_list')  # Default jika role tidak dikenali

            else:
                messages.error(request, "Invalid username or password. Please try again.")

        return render(request, 'users/login.html')

    except Exception as e:
        messages.error(request, f"An error occurred during login: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'login'))
@login_required
def logout_view(request):
    try:
        # Periksa apakah pengguna memiliki peran 'admin' atau 'staff'
        if request.user.role == 'admin' or request.user.role == 'staff':
            messages.warning(request, "Berhasil logout.")
            return redirect('login')  # Redirect ke halaman login jika pengguna adalah admin/staff

        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('index')
    except Exception as e:
        messages.error(request, f"An error occurred during logout: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'login'))
@login_required
def profile_update(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil Anda telah diperbarui.")
            return redirect('profile_update', id=id)
        else:
            messages.error(request, "Harap perbaiki kesalahan di bawah ini.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'users/profile_update.html', {'form': form, 'user': user})
@login_required
def user_list(request):
    try:
        if request.user.role not in ['admin', 'staff']:
            messages.error(request, "Access denied. You must be an admin to access this page.")
            return redirect('profile_update', id=request.user.id)
        users = User.objects.all()
        return render(request, 'users/user_list.html', {'users': users})
    except Exception as e:
        messages.error(request, f"An error occurred while loading the user list: {str(e)}")
    return redirect('profile_update', id=request.user.id) 

@login_required
def user_detail(request, pk):
    try:
        if request.user.role not in ['admin', 'staff']:
            messages.error(request, "Access denied.")
            return redirect('dashboard')
        user = get_object_or_404(User, pk=pk)
        return render(request, 'users/user_detail.html', {'user': user})
    except Exception as e:
        messages.error(request, f"An error occurred while fetching the user details: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'user_list'))
    
@login_required
def create_user(request):
    try:
        if request.user.role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('profile_update')

        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                # Simpan pengguna baru
                user = form.save()
                messages.success(request, "User created successfully!")
                return redirect('user_list')  # Redirect ke halaman user_list
            else:
                # Menampilkan error berdasarkan field
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        else:
            form = UserRegistrationForm()

        return render(request, 'users/create_user.html', {'form': form})

    except Exception as e:
        messages.error(request, f"An error occurred while creating the user: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'user_list'))
def user_delete(request, id):
    try:
        # Ambil objek pengguna berdasarkan ID yang diberikan
        user = get_object_or_404(User, id=id)

        # Hapus pengguna dari database
        user.delete()

        # Kirimkan pesan sukses
        messages.success(request, f"Pengguna {user.username} telah dihapus.")
        
        # Redirect ke halaman daftar pengguna setelah berhasil menghapus
        return redirect('user_list')
    
    except Exception as e:
        # Jika terjadi kesalahan saat menghapus, tampilkan pesan error
        messages.error(request, f"Terjadi kesalahan saat menghapus pengguna: {str(e)}")
        
        # Redirect kembali ke halaman sebelumnya atau daftar pengguna
        return redirect(request.META.get('HTTP_REFERER', 'user_list'))
