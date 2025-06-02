import django_filters
from django import forms
from .models import Pet


class PetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )
    
    breed = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by breed...'
        })
    )
    
    species = django_filters.ChoiceFilter(
        choices=Pet.SPECIES_CHOICES,
        empty_label="Any Species",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    size = django_filters.ChoiceFilter(
        choices=Pet.SIZE_CHOICES,
        empty_label="Any Size",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    gender = django_filters.ChoiceFilter(
        choices=Pet.GENDER_CHOICES,
        empty_label="Any Gender",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    age_years = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control'})
    )
    
    adoption_fee = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control'})
    )
    
    good_with_kids = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    good_with_dogs = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    good_with_cats = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    house_trained = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    is_spayed_neutered = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    is_vaccinated = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'species', 'size', 'gender', 'age_years', 'adoption_fee',
            'good_with_kids', 'good_with_dogs', 'good_with_cats', 'house_trained',
            'is_spayed_neutered', 'is_vaccinated'
        ]
