from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


from .models import Account

class registrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'password1', 'password2', 'email']
        

class loginAuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Only attempt authentication when both fields are provided.
        # Django's default backend uses `username=` even when USERNAME_FIELD is `email`.
        if email and password:
            user = authenticate(request=None, username=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid login credentials")

        return cleaned_data
            

class adminRegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields =['email', 'username', 'password1', 'password2']
        
        
    def save(self, commit=True):
        user = super().save(commit=False) 
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = False
        
        if commit:
            user.save()
        return user
    

class staffRegistrationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=True)
    class Meta:
        model = Account
        fields =['email', 'username', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False) 
        user.is_staff = self.cleaned_data["is_staff"]
        if commit:
            user.save()
        return user
    
             

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class AccountRoleForm(forms.Form):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def __init__(self, *args, account, **kwargs):
        self.account = account
        if 'initial' not in kwargs:
            if account.is_superuser:
                role = 'superuser'
            elif account.is_admin:
                role = 'admin'
            else:
                role = 'user'
            kwargs['initial'] = {'role': role}
        super().__init__(*args, **kwargs)

    def save(self):
        role = self.cleaned_data['role']
        self.account.is_admin = role in ('admin', 'superuser')
        self.account.is_staff = role in ('admin', 'superuser')
        self.account.is_superuser = role == 'superuser'
        self.account.save(update_fields=['is_admin', 'is_staff', 'is_superuser'])
        return self.account