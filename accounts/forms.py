from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password_confirm = forms.CharField(label='повторите пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    
    class Meta:
        model = User
        fields = ['username', 'email',]
        labels = {'username': 'Имя пользователя', 'email': 'Почта',}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}),
            'email': forms.TextInput(attrs={'placeholder': 'Введите почту'}),
        }
        
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            
            if password != password_confirm:
                raise forms.ValidationError('Пароли не совпадают')
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    username = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))