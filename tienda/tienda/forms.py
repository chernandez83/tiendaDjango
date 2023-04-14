from django import forms
# from django.contrib.auth.models import User
from users.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(required=True,
                               min_length=3,
                               max_length=50,
                               label='Usuario',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'username',
                                   'placeholder': 'Usuario',
                               }))
    email = forms.EmailField(required=True,
                             label='E-mail',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'id': 'email',
                                 'placeholder': 'correo@servidor.tld',
                             }))
    password = forms.CharField(required=True,
                               min_length=6,
                               label='Contraseña',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'password',
                                   'placeholder': 'Contraseña',
                               }))
    password2 = forms.CharField(required=True,
                                label='Confirmar contraseña:',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'id': 'password2',
                                    'placeholder': 'Contraseña'
                                }))
    
    # clean_nombreDelCampo para validar
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'{username} ya se encuentra en uso.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email} ya está registrado.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password2', f'La contraseña no coincide.')
    
    def save(self):
        # User.objects.create_user encripta el password
        return User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
        )
