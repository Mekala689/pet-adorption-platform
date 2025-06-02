"""
API Filters for Pet Adoption Platform
"""
import django_filters
from django import forms
from apps.pets.models import Pet


class PetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    breed = django_filters.CharFilter(lookup_expr='icontains')
    species = django_filters.ChoiceFilter(choices=Pet.SPECIES_CHOICES)
    size = django_filters.ChoiceFilter(choices=Pet.SIZE_CHOICES)
    gender = django_filters.ChoiceFilter(choices=Pet.GENDER_CHOICES)
    
    age_min = django_filters.NumberFilter(field_name='age_years', lookup_expr='gte')
    age_max = django_filters.NumberFilter(field_name='age_years', lookup_expr='lte')
    
    weight_min = django_filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = django_filters.NumberFilter(field_name='weight', lookup_expr='lte')
    
    fee_min = django_filters.NumberFilter(field_name='adoption_fee', lookup_expr='gte')
    fee_max = django_filters.NumberFilter(field_name='adoption_fee', lookup_expr='lte')
    
    good_with_kids = django_filters.BooleanFilter()
    good_with_dogs = django_filters.BooleanFilter()
    good_with_cats = django_filters.BooleanFilter()
    house_trained = django_filters.BooleanFilter()
    is_spayed_neutered = django_filters.BooleanFilter()
    is_vaccinated = django_filters.BooleanFilter()
    
    shelter_city = django_filters.CharFilter(
        field_name='shelter__city', 
        lookup_expr='icontains'
    )
    shelter_state = django_filters.CharFilter(
        field_name='shelter__state', 
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'species', 'size', 'gender', 'status',
            'good_with_kids', 'good_with_dogs', 'good_with_cats',
            'house_trained', 'is_spayed_neutered', 'is_vaccinated'
        ]
