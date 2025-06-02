from django import forms
from .models import AdoptionRequest


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message', 'phone_number', 'preferred_contact_time']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us why you want to adopt this pet and a bit about yourself...',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Your phone number',
                'class': 'form-control'
            }),
            'preferred_contact_time': forms.TextInput(attrs={
                'placeholder': 'e.g., Weekdays 9am-5pm, Evenings after 6pm',
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].label = 'Why do you want to adopt this pet?'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['preferred_contact_time'].label = 'Best time to contact you'
        
        # Make phone number required
        self.fields['phone_number'].required = True


class QuickAdoptionRequestForm(forms.ModelForm):
    """Simplified form for quick adoption requests from home page"""
    class Meta:
        model = AdoptionRequest
        fields = ['message', 'phone_number']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Brief message about why you want to adopt this pet...',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Your phone number',
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].label = 'Message'
        self.fields['phone_number'].label = 'Phone'
        self.fields['phone_number'].required = True
