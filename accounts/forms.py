from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """!
    
    Inherits custom UserCreationForm from django.contrib.auth.forms
    
    Adds extra fields to facilitate user registration using organisation name and passcode
   
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2", "org_name", "org_code")

class CustomUserChangeForm(UserChangeForm):
    """!

    Inherits custom UserChangeForm from django.contrib.auth.forms

    """
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields