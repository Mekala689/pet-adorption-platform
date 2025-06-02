from django.contrib import admin
from .models import AdoptionApplication, AdoptionInterview, AdoptionDocument


class AdoptionInterviewInline(admin.TabularInline):
    model = AdoptionInterview
    extra = 0


class AdoptionDocumentInline(admin.TabularInline):
    model = AdoptionDocument
    extra = 0


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'pet', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'submitted_at', 'reviewed_at')
    search_fields = ('applicant__username', 'applicant__first_name', 'applicant__last_name', 'pet__name')
    readonly_fields = ('submitted_at', 'reviewed_at', 'completed_at')
    inlines = [AdoptionInterviewInline, AdoptionDocumentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('applicant', 'pet', 'status')
        }),
        ('Application Details', {
            'fields': ('reason_for_adoption', 'experience_with_pets', 'living_situation', 'work_schedule')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Veterinarian Information', {
            'fields': ('veterinarian_name', 'veterinarian_phone', 'veterinarian_address')
        }),
        ('Additional Information', {
            'fields': ('additional_notes', 'reviewer_notes')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'reviewed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdoptionInterview)
class AdoptionInterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interview_type', 'scheduled_date', 'status', 'interviewer')
    list_filter = ('interview_type', 'status', 'scheduled_date')
    search_fields = ('application__applicant__username', 'application__pet__name', 'interviewer__username')


@admin.register(AdoptionDocument)
class AdoptionDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'application', 'document_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('title', 'application__applicant__username', 'application__pet__name')
