# Register your models here.
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin 
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser, Organisation

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