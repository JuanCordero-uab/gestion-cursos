# cursos/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Curso, MaterialDeApoyo

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'categoria', 'modalidad', 'tipo', 'fecha', 'hora', 'duracion', 'materiales']

class MaterialDeApoyoForm(forms.ModelForm):
    class Meta:
        model = MaterialDeApoyo
        fields = ['titulo', 'descripcion', 'archivo', 'enlace']