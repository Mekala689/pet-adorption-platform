from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ShelterProfile, AdopterProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'address', 'city', 'state', 'zip_code', 'profile_picture', 'date_of_birth')
        }),
    )


@admin.register(ShelterProfile)
class ShelterProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user', 'license_number', 'is_verified', 'capacity')
    list_filter = ('is_verified', 'established_date')
    search_fields = ('organization_name', 'license_number', 'user__username')
    readonly_fields = ('user',)


@admin.register(AdopterProfile)
class AdopterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'housing_type', 'has_yard', 'has_other_pets', 'is_approved')
    list_filter = ('housing_type', 'has_yard', 'has_other_pets', 'is_approved')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('user',)
