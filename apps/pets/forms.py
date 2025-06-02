from django import forms
from django.forms import inlineformset_factory
from .models import Pet, PetImage


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'species', 'breed', 'age_years', 'age_months', 'gender', 'size', 'weight', 'color',
            'description', 'personality_traits', 'good_with_kids', 'good_with_dogs', 'good_with_cats',
            'house_trained', 'is_spayed_neutered', 'is_vaccinated', 'medical_notes', 'special_needs',
            'adoption_fee', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'personality_traits': forms.Textarea(attrs={'rows': 3}),
            'medical_notes': forms.Textarea(attrs={'rows': 3}),
            'special_needs': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'step': '0.01'}),
            'adoption_fee': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


PetImageFormSet = inlineformset_factory(
    Pet, 
    PetImage, 
    form=PetImageForm,
    extra=3,
    max_num=10,
    can_delete=True
)


class PetSearchForm(forms.Form):
    SPECIES_CHOICES = [('', 'Any Species')] + Pet.SPECIES_CHOICES
    SIZE_CHOICES = [('', 'Any Size')] + Pet.SIZE_CHOICES
    GENDER_CHOICES = [('', 'Any Gender')] + Pet.GENDER_CHOICES
    
    search = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, breed, or description...'
        })
    )
    species = forms.ChoiceField(
        choices=SPECIES_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    good_with_kids = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    good_with_dogs = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    good_with_cats = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    house_trained = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_spayed_neutered = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    max_adoption_fee = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Maximum adoption fee',
            'step': '0.01'
        })
    )
