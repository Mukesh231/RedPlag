# Register your models here.
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin 
from .forms import CustomUserCreationForm, CustomUserChangeForm 
<<<<<<< HEAD
from .models import CustomUser
from .models import Organisation 
=======
from .models import CustomUser, Organisation
>>>>>>> 9edfc3e7d6ed404647ad85feba2961175d871325

class CustomUserAdmin(UserAdmin):
    model = CustomUser 
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm 
    add_fieldsets = UserAdmin.add_fieldsets + (
    (None, {'fields': ('email', 'first_name', 'last_name', 'org_name', 'org_code',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('org_name', 'org_code')}),
    )

admin.site.register(CustomUser, CustomUserAdmin) 
admin.site.register(Organisation)