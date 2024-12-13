from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your last name.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        max_length=128,
        required=False,  # Tidak wajib untuk diisi
        widget=forms.PasswordInput,
        help_text="Kosongkan jika tidak ingin mengubah password.",
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:  # Jika password diberikan, hash dan set
            user.set_password(password)
        if commit:
            user.save()
        return user
