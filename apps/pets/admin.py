from django.contrib import admin
from .models import Pet, PetImage, PetFavorite


class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age_display', 'gender', 'shelter', 'status', 'created_at')
    list_filter = ('species', 'gender', 'size', 'status', 'good_with_kids', 'good_with_dogs', 'good_with_cats', 'is_spayed_neutered', 'is_vaccinated')
    search_fields = ('name', 'breed', 'shelter__username', 'shelter__shelter_profile__organization_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PetImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'species', 'breed', 'age_years', 'age_months', 'gender', 'size', 'weight', 'color')
        }),
        ('Shelter & Status', {
            'fields': ('shelter', 'status', 'adoption_fee')
        }),
        ('Description', {
            'fields': ('description', 'personality_traits')
        }),
        ('Compatibility', {
            'fields': ('good_with_kids', 'good_with_dogs', 'good_with_cats', 'house_trained')
        }),
        ('Medical Information', {
            'fields': ('is_spayed_neutered', 'is_vaccinated', 'medical_notes', 'special_needs')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ('pet', 'caption', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('pet__name', 'caption')


@admin.register(PetFavorite)
class PetFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'pet__name')
