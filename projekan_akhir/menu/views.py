from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Menu
from .forms import MenuForm

def user_is_admin_or_staff(user):
    return user.is_authenticated and user.role in ['admin', 'staff']

def user_is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def user_is_staff(user):
    return user.is_authenticated and user.role == 'staff'

@login_required
def menu_list(request):
    try:
        if not user_is_admin_or_staff(request.user):
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        menus = Menu.objects.all()
        return render(request, 'menu/menu_list.html', {'menus': menus})
    except Exception as e:
        messages.error(request, f"An error occurred while retrieving the menu list: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def menu_detail(request, menu_id):
    try:
        if not user_is_admin_or_staff(request.user):
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        
        menu = get_object_or_404(Menu, id=menu_id)
        return render(request, 'menu/menu_detail.html', {'menu': menu})
    except Exception as e:
        messages.error(request, f"An error occurred while fetching the menu details: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'menu_list'))

@login_required
def menu_create(request):
    try:
        if not user_is_admin_or_staff(request.user):
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        
        if request.method == 'POST':
            form = MenuForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Menu item created successfully!")
                return redirect('menu_list')
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            form = MenuForm()
        return render(request, 'menu/menu_form.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred while creating the menu item: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'menu_list'))

@login_required
def menu_edit(request, menu_id):
    try:
        if not user_is_admin_or_staff(request.user):
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        
        menu = get_object_or_404(Menu, id=menu_id)
        if request.method == 'POST':
            form = MenuForm(request.POST, request.FILES, instance=menu)
            if form.is_valid():
                form.save()
                messages.success(request, "Menu item updated successfully!")
                return redirect('menu_list')
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            form = MenuForm(instance=menu)
        return render(request, 'menu/menu_form.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred while editing the menu item: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'menu_list'))

@login_required
def menu_delete(request, menu_id):
    try:
        if not user_is_admin_or_staff(request.user):
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        
        menu = get_object_or_404(Menu, id=menu_id)
        menu.delete()
        messages.success(request, "Menu item deleted successfully!")
        return redirect('menu_list')
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the menu item: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'menu_list'))
