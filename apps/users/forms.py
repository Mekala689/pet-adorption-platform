from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ShelterProfile, AdopterProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShelterProfileForm(forms.ModelForm):
    class Meta:
        model = ShelterProfile
        fields = ['organization_name', 'license_number', 'website', 'description', 'capacity', 'established_date']
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AdopterProfileForm(forms.ModelForm):
    class Meta:
        model = AdopterProfile
        fields = [
            'housing_type', 'has_yard', 'has_other_pets', 'other_pets_description',
            'household_members', 'experience_with_pets', 'preferred_pet_age', 'preferred_pet_size'
        ]
        widgets = {
            'other_pets_description': forms.Textarea(attrs={'rows': 3}),
            'experience_with_pets': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
