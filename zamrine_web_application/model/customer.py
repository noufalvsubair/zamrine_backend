from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, null=True)
    auth_token = models.TextField(null=False, default="")
    mobile = models.CharField(blank=False, max_length=15)
    image_url = models.URLField(null=True)
    email_otp = models.IntegerField(blank=False, default=0)
    mobile_otp = models.IntegerField(blank=False, default=0)
    is_mobile_verifiied = models.BooleanField(blank=False, default=False)
    is_email_verified = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.user.get_full_name()

class UserForm(UserCreationForm):
    password1 = forms.CharField(label= 'password', widget=forms.PasswordInput)
    password2 = forms.CharField(label= 'confirm_password', widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput, label= 'email')
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    username = forms.CharField(label='username')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    error_messages= {
        "password_mismatch": "Passwords do not match.",
        "username_exists": "Username already present`"
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print(password1 and password2 and password1 != password2)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

class CustomerForm(forms.ModelForm):
    mobile = forms.CharField(label='mobile')
    image_url = forms.CharField(label='image_url', required=False)

    class Meta:
        model = Customer
        fields = ['mobile', 'image_url']

    error_messages= {
        "username_exists": "Username already present`"
    }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if Customer.objects.exclude(pk=self.instance.pk).filter(mobile= mobile).exists():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        return mobile
