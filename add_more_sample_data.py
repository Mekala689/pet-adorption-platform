#!/usr/bin/env python
"""
Script to add more sample data to the Pet Adoption Platform
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal
import random

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption.settings')
django.setup()

from apps.users.models import User, ShelterProfile, AdopterProfile
from apps.pets.models import Pet, PetImage
from apps.adoptions.models import AdoptionApplication

def create_more_pets():
    """Create additional sample pets"""
    print("Creating more sample pets...")
    
    # Get existing shelters
    shelters = User.objects.filter(user_type='shelter')
    if not shelters.exists():
        print("No shelters found. Please run populate_sample_data.py first.")
        return
    
    additional_pets = [
        {
            'name': 'Charlie',
            'species': 'dog',
            'breed': 'Beagle',
            'age_years': 4,
            'age_months': 2,
            'gender': 'male',
            'size': 'medium',
            'weight': Decimal('35.0'),
            'color': 'Tri-color',
            'shelter': random.choice(shelters),
            'description': 'Charlie is a curious and friendly Beagle who loves to explore and follow interesting scents. He would make a great companion for an active family.',
            'personality_traits': 'Curious, friendly, energetic, loyal',
            'good_with_kids': True,
            'good_with_dogs': True,
            'good_with_cats': False,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Healthy with no known issues.',
            'adoption_fee': Decimal('225.00'),
        },
        {
            'name': 'Mittens',
            'species': 'cat',
            'breed': 'Persian',
            'age_years': 3,
            'age_months': 0,
            'gender': 'female',
            'size': 'medium',
            'weight': Decimal('9.5'),
            'color': 'White',
            'shelter': random.choice(shelters),
            'description': 'Mittens is a beautiful Persian cat with a calm and gentle personality. She loves being brushed and enjoys quiet companionship.',
            'personality_traits': 'Calm, gentle, affectionate, quiet',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': True,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Requires daily brushing due to long coat.',
            'adoption_fee': Decimal('175.00'),
        },
        {
            'name': 'Rocky',
            'species': 'dog',
            'breed': 'Pit Bull Mix',
            'age_years': 2,
            'age_months': 6,
            'gender': 'male',
            'size': 'large',
            'weight': Decimal('60.0'),
            'color': 'Brindle',
            'shelter': random.choice(shelters),
            'description': 'Rocky is a strong and loving dog who needs an experienced owner. He is very loyal and protective of his family.',
            'personality_traits': 'Loyal, protective, strong, loving',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': False,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Healthy and strong, needs regular exercise.',
            'adoption_fee': Decimal('200.00'),
        },
        {
            'name': 'Daisy',
            'species': 'rabbit',
            'breed': 'Holland Lop',
            'age_years': 1,
            'age_months': 0,
            'gender': 'female',
            'size': 'small',
            'weight': Decimal('3.5'),
            'color': 'Brown and White',
            'shelter': random.choice(shelters),
            'description': 'Daisy is an adorable Holland Lop rabbit who loves to hop around and explore. She is litter trained and very social.',
            'personality_traits': 'Social, curious, gentle, playful',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': False,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Healthy rabbit, needs hay-based diet.',
            'adoption_fee': Decimal('50.00'),
        },
        {
            'name': 'Shadow',
            'species': 'cat',
            'breed': 'Black Domestic Shorthair',
            'age_years': 6,
            'age_months': 0,
            'gender': 'male',
            'size': 'large',
            'weight': Decimal('14.0'),
            'color': 'Black',
            'shelter': random.choice(shelters),
            'description': 'Shadow is a handsome black cat who is looking for a quiet home. He loves to sit by windows and watch the world go by.',
            'personality_traits': 'Quiet, observant, independent, gentle',
            'good_with_kids': False,
            'good_with_dogs': False,
            'good_with_cats': True,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Healthy senior cat.',
            'adoption_fee': Decimal('100.00'),
        },
        {
            'name': 'Rosie',
            'species': 'dog',
            'breed': 'Cocker Spaniel',
            'age_years': 8,
            'age_months': 0,
            'gender': 'female',
            'size': 'medium',
            'weight': Decimal('28.0'),
            'color': 'Golden',
            'shelter': random.choice(shelters),
            'description': 'Rosie is a sweet senior dog who loves gentle walks and cozy naps. She would be perfect for a calm household.',
            'personality_traits': 'Gentle, calm, sweet, loving',
            'good_with_kids': True,
            'good_with_dogs': True,
            'good_with_cats': True,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Senior dog with mild arthritis, managed with medication.',
            'adoption_fee': Decimal('125.00'),
        },
    ]
    
    created_pets = []
    for pet_data in additional_pets:
        pet = Pet.objects.create(**pet_data)
        created_pets.append(pet)
        print(f"✅ Created {pet.name} ({pet.get_species_display()})")
    
    print(f"✅ {len(created_pets)} additional pets created successfully!")
    return created_pets

def create_more_users():
    """Create additional sample users"""
    print("Creating more sample users...")
    
    # Create another shelter
    shelter3 = User.objects.create_user(
        username='caring_paws',
        email='info@caringpaws.org',
        password='shelter123',
        first_name='Caring',
        last_name='Paws',
        user_type='shelter',
        phone_number='+1234567898',
        address='789 Compassion Street',
        city='Kindness City',
        state='TX',
        zip_code='75001'
    )
    
    ShelterProfile.objects.create(
        user=shelter3,
        organization_name='Caring Paws Rescue',
        license_number='SHELTER003',
        website='https://caringpaws.org',
        description='A small rescue focused on senior pets and special needs animals.',
        capacity=20,
        established_date=date(2018, 3, 10),
        is_verified=True
    )
    
    # Create more adopters
    adopter3 = User.objects.create_user(
        username='emily_wilson',
        email='emily@example.com',
        password='adopter123',
        first_name='Emily',
        last_name='Wilson',
        user_type='adopter',
        phone_number='+1234567899',
        address='456 Pet Lover Lane',
        city='Animal City',
        state='FL',
        zip_code='33101'
    )
    
    AdopterProfile.objects.create(
        user=adopter3,
        housing_type='condo',
        has_yard=False,
        has_other_pets=False,
        household_members=1,
        experience_with_pets='First-time pet owner, but have done extensive research.',
        preferred_pet_age='Senior',
        preferred_pet_size='Small to medium',
        is_approved=True
    )
    
    print("✅ Additional users created successfully!")

def main():
    """Main function to add more sample data"""
    print("🚀 Adding more sample data to Pet Adoption Platform...")
    
    try:
        create_more_users()
        create_more_pets()
        
        print("\n🎉 Additional sample data created successfully!")
        print(f"Total pets now: {Pet.objects.count()}")
        print(f"Total shelters now: {User.objects.filter(user_type='shelter').count()}")
        print(f"Total adopters now: {User.objects.filter(user_type='adopter').count()}")
        
    except Exception as e:
        print(f"❌ Error creating additional sample data: {e}")

if __name__ == '__main__':
    main()
