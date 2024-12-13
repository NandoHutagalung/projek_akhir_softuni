from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import MejaBiliar
from .forms import MejaBiliarStatusForm, MejaBiliarForm

# Check if the user is admin or staff
def is_admin_or_staff(user):
    return user.role in ['admin', 'staff']

# Check if the user is admin
def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin_or_staff)
def meja_list(request):
    try:
        meja_biliars = MejaBiliar.objects.all()
        return render(request, 'meja_biliar/meja_list.html', {'meja_biliars': meja_biliars})
    except Exception as e:
        messages.error(request, f"An error occurred while loading the billiard tables list: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect to previous page or home

@login_required
@user_passes_test(is_admin_or_staff)
def meja_detail(request, meja_id):
    try:
        meja = get_object_or_404(MejaBiliar, id=meja_id)

        if request.method == 'POST':
            form = MejaBiliarStatusForm(request.POST, instance=meja)
            if form.is_valid():
                form.save()
                messages.success(request, "Meja status updated successfully!")
                return redirect('meja_list')  # Redirect to the meja list page after success
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error in {field}: {error}")
        else:
            form = MejaBiliarStatusForm(instance=meja)

        return render(request, 'meja_biliar/meja_detail.html', {'form': form, 'meja': meja})
    
    except Exception as e:
        messages.error(request, f"An error occurred while fetching or updating the billiard table: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'meja_list'))  # Redirect to previous page or meja list

@login_required
@user_passes_test(is_admin)
def meja_create(request):
    try:
        if request.method == 'POST':
            form = MejaBiliarStatusForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "New billiard table created successfully!")
                return redirect('meja_list')  # Redirect to the meja list page after success
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error in {field}: {error}")
        else:
            form = MejaBiliarForm()

        return render(request, 'meja_biliar/meja_form.html', {'form': form})
    
    except Exception as e:
        messages.error(request, f"An error occurred while creating the billiard table: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'meja_list'))  # Redirect to previous page or meja list

@login_required
@user_passes_test(is_admin)
def meja_delete(request, meja_id):
    try:
        meja = get_object_or_404(MejaBiliar, id=meja_id)
        meja.delete()
        messages.success(request, "Billiard table deleted successfully!")
        return redirect('meja_list')  # Redirect to the meja list page after success
    
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the billiard table: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'meja_list'))  # Redirect to previous page or meja list
