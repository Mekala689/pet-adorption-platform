from django import forms
from .models import AdoptionApplication, AdoptionInterview, AdoptionDocument


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = [
            'reason_for_adoption', 'experience_with_pets', 'living_situation', 'work_schedule',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'veterinarian_name', 'veterinarian_phone', 'veterinarian_address', 'additional_notes'
        ]
        widgets = {
            'reason_for_adoption': forms.Textarea(attrs={'rows': 4}),
            'experience_with_pets': forms.Textarea(attrs={'rows': 4}),
            'living_situation': forms.Textarea(attrs={'rows': 4}),
            'work_schedule': forms.Textarea(attrs={'rows': 3}),
            'veterinarian_address': forms.Textarea(attrs={'rows': 3}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Add help text
        self.fields['reason_for_adoption'].help_text = "Please explain why you want to adopt this specific pet."
        self.fields['experience_with_pets'].help_text = "Describe your previous experience with pets, including current pets."
        self.fields['living_situation'].help_text = "Describe your home (apartment, house, yard, etc.) and living arrangements."
        self.fields['work_schedule'].help_text = "How many hours per day will the pet be alone? Who will care for the pet when you're away?"


class AdoptionInterviewForm(forms.ModelForm):
    class Meta:
        model = AdoptionInterview
        fields = ['interview_type', 'scheduled_date', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'notes':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class AdoptionDocumentForm(forms.ModelForm):
    class Meta:
        model = AdoptionDocument
        fields = ['document_type', 'title', 'file']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ApplicationReviewForm(forms.ModelForm):
    """Form for shelter staff to review applications"""
    class Meta:
        model = AdoptionApplication
        fields = ['reviewer_notes']
        widgets = {
            'reviewer_notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reviewer_notes'].help_text = "Add any notes about your review of this application."
