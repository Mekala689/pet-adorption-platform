#!/usr/bin/env python
"""
Script to populate the Pet Adoption Platform with sample data
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption.settings')
django.setup()

from apps.users.models import User, ShelterProfile, AdopterProfile
from apps.pets.models import Pet, PetImage
from apps.adoptions.models import AdoptionApplication

def create_sample_users():
    """Create sample users"""
    print("Creating sample users...")
    
    # Create shelter users
    shelter1 = User.objects.create_user(
        username='happypaws_shelter',
        email='contact@happypaws.com',
        password='shelter123',
        first_name='Happy',
        last_name='Paws',
        user_type='shelter',
        phone_number='+1234567890',
        address='123 Animal Street',
        city='Pet City',
        state='CA',
        zip_code='12345'
    )
    
    ShelterProfile.objects.create(
        user=shelter1,
        organization_name='Happy Paws Animal Shelter',
        license_number='SHELTER001',
        website='https://happypaws.com',
        description='A loving shelter dedicated to finding homes for abandoned animals.',
        capacity=50,
        established_date=date(2010, 1, 1),
        is_verified=True
    )
    
    shelter2 = User.objects.create_user(
        username='rescue_haven',
        email='info@rescuehaven.org',
        password='shelter123',
        first_name='Rescue',
        last_name='Haven',
        user_type='shelter',
        phone_number='+1234567891',
        address='456 Rescue Road',
        city='Animal Town',
        state='NY',
        zip_code='54321'
    )
    
    ShelterProfile.objects.create(
        user=shelter2,
        organization_name='Rescue Haven',
        license_number='SHELTER002',
        website='https://rescuehaven.org',
        description='Specialized in rescuing and rehabilitating stray animals.',
        capacity=30,
        established_date=date(2015, 6, 15),
        is_verified=True
    )
    
    # Create adopter users
    adopter1 = User.objects.create_user(
        username='john_doe',
        email='john@example.com',
        password='adopter123',
        first_name='John',
        last_name='Doe',
        user_type='adopter',
        phone_number='+1234567892',
        address='789 Family Lane',
        city='Suburb City',
        state='CA',
        zip_code='67890'
    )
    
    AdopterProfile.objects.create(
        user=adopter1,
        housing_type='house',
        has_yard=True,
        has_other_pets=False,
        household_members=3,
        experience_with_pets='I grew up with dogs and have had pets for over 10 years.',
        preferred_pet_age='Young adult',
        preferred_pet_size='Medium',
        is_approved=True
    )
    
    adopter2 = User.objects.create_user(
        username='sarah_smith',
        email='sarah@example.com',
        password='adopter123',
        first_name='Sarah',
        last_name='Smith',
        user_type='adopter',
        phone_number='+1234567893',
        address='321 Apartment Ave',
        city='Metro City',
        state='NY',
        zip_code='13579'
    )
    
    AdopterProfile.objects.create(
        user=adopter2,
        housing_type='apartment',
        has_yard=False,
        has_other_pets=True,
        other_pets_description='One cat named Whiskers',
        household_members=2,
        experience_with_pets='I have experience with both cats and small dogs.',
        preferred_pet_age='Any age',
        preferred_pet_size='Small to medium',
        is_approved=True
    )
    
    print("✅ Sample users created successfully!")
    return shelter1, shelter2, adopter1, adopter2

def create_sample_pets(shelter1, shelter2):
    """Create sample pets"""
    print("Creating sample pets...")
    
    pets_data = [
        {
            'name': 'Buddy',
            'species': 'dog',
            'breed': 'Golden Retriever',
            'age_years': 3,
            'age_months': 6,
            'gender': 'male',
            'size': 'large',
            'weight': Decimal('65.5'),
            'color': 'Golden',
            'shelter': shelter1,
            'description': 'Buddy is a friendly and energetic Golden Retriever who loves playing fetch and swimming. He gets along well with children and other dogs.',
            'personality_traits': 'Friendly, energetic, loyal, playful',
            'good_with_kids': True,
            'good_with_dogs': True,
            'good_with_cats': False,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Up to date on all vaccinations. Recent dental cleaning.',
            'adoption_fee': Decimal('250.00'),
        },
        {
            'name': 'Luna',
            'species': 'cat',
            'breed': 'Siamese Mix',
            'age_years': 2,
            'age_months': 0,
            'gender': 'female',
            'size': 'small',
            'weight': Decimal('8.2'),
            'color': 'Cream and Brown',
            'shelter': shelter1,
            'description': 'Luna is a beautiful and intelligent Siamese mix who loves to chat and follow her humans around. She enjoys sunny windowsills and interactive toys.',
            'personality_traits': 'Intelligent, vocal, affectionate, curious',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': True,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Healthy with no known medical issues.',
            'adoption_fee': Decimal('150.00'),
        },
        {
            'name': 'Max',
            'species': 'dog',
            'breed': 'German Shepherd Mix',
            'age_years': 5,
            'age_months': 0,
            'gender': 'male',
            'size': 'large',
            'weight': Decimal('75.0'),
            'color': 'Black and Tan',
            'shelter': shelter2,
            'description': 'Max is a loyal and protective German Shepherd mix looking for an experienced owner. He is well-trained and would make an excellent guard dog.',
            'personality_traits': 'Loyal, protective, intelligent, calm',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': False,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Mild hip dysplasia, managed with supplements.',
            'adoption_fee': Decimal('300.00'),
        },
        {
            'name': 'Bella',
            'species': 'dog',
            'breed': 'Labrador Mix',
            'age_years': 1,
            'age_months': 8,
            'gender': 'female',
            'size': 'medium',
            'weight': Decimal('45.0'),
            'color': 'Chocolate Brown',
            'shelter': shelter2,
            'description': 'Bella is a young and playful Labrador mix who loves everyone she meets. She is still learning basic commands but is very eager to please.',
            'personality_traits': 'Playful, friendly, energetic, social',
            'good_with_kids': True,
            'good_with_dogs': True,
            'good_with_cats': True,
            'house_trained': False,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Healthy puppy, needs continued training.',
            'adoption_fee': Decimal('200.00'),
        },
        {
            'name': 'Whiskers',
            'species': 'cat',
            'breed': 'Domestic Shorthair',
            'age_years': 7,
            'age_months': 0,
            'gender': 'male',
            'size': 'medium',
            'weight': Decimal('12.5'),
            'color': 'Orange Tabby',
            'shelter': shelter1,
            'description': 'Whiskers is a senior cat who loves quiet companionship and gentle pets. He would do best in a calm household without young children.',
            'personality_traits': 'Calm, gentle, independent, affectionate',
            'good_with_kids': False,
            'good_with_dogs': False,
            'good_with_cats': True,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'medical_notes': 'Senior cat with mild arthritis.',
            'adoption_fee': Decimal('75.00'),
        },
    ]
    
    created_pets = []
    for pet_data in pets_data:
        pet = Pet.objects.create(**pet_data)
        created_pets.append(pet)
    
    print("✅ Sample pets created successfully!")
    return created_pets

def create_sample_applications(pets, adopter1, adopter2):
    """Create sample adoption applications"""
    print("Creating sample adoption applications...")
    
    # Application from adopter1 for Buddy
    AdoptionApplication.objects.create(
        applicant=adopter1,
        pet=pets[0],  # Buddy
        reason_for_adoption='I want to provide a loving home for a dog and have experience with Golden Retrievers.',
        experience_with_pets='I grew up with dogs and have had pets for over 10 years. My last dog lived to be 14 years old.',
        living_situation='I live in a house with a large fenced yard. My family includes my spouse and one teenage child.',
        work_schedule='I work from home 3 days a week and my spouse works part-time, so someone is usually home.',
        emergency_contact_name='Jane Doe',
        emergency_contact_phone='+1234567894',
        emergency_contact_relationship='Sister',
        veterinarian_name='Dr. Smith Animal Clinic',
        veterinarian_phone='+1234567895',
        veterinarian_address='123 Vet Street, Suburb City, CA',
        additional_notes='We are excited to welcome Buddy into our family and provide him with lots of love and exercise.',
        status='pending'
    )
    
    # Application from adopter2 for Luna
    AdoptionApplication.objects.create(
        applicant=adopter2,
        pet=pets[1],  # Luna
        reason_for_adoption='I am looking for a companion cat for my current cat and Luna seems like a perfect match.',
        experience_with_pets='I have experience with both cats and small dogs. I currently have one cat.',
        living_situation='I live in a pet-friendly apartment with my partner. We have plenty of space and cat furniture.',
        work_schedule='We both work regular hours but have a pet sitter who checks on our cat during long days.',
        emergency_contact_name='Mike Johnson',
        emergency_contact_phone='+1234567896',
        emergency_contact_relationship='Brother',
        veterinarian_name='City Animal Hospital',
        veterinarian_phone='+1234567897',
        veterinarian_address='456 Pet Ave, Metro City, NY',
        additional_notes='Our current cat Whiskers would love a friend, and we think Luna would be perfect.',
        status='approved'
    )
    
    print("✅ Sample adoption applications created successfully!")

def main():
    """Main function to populate sample data"""
    print("🚀 Populating Pet Adoption Platform with sample data...")
    
    # Check if data already exists
    if User.objects.filter(user_type='shelter').exists():
        print("ℹ️  Sample data already exists. Skipping...")
        return
    
    try:
        shelter1, shelter2, adopter1, adopter2 = create_sample_users()
        pets = create_sample_pets(shelter1, shelter2)
        create_sample_applications(pets, adopter1, adopter2)
        
        print("\n🎉 Sample data created successfully!")
        print("\nYou can now:")
        print("1. Browse pets at http://127.0.0.1:8000/pets/")
        print("2. Login as admin (username: admin, password: admin123)")
        print("3. Login as shelter (username: happypaws_shelter, password: shelter123)")
        print("4. Login as adopter (username: john_doe, password: adopter123)")
        print("5. Access admin panel at http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

if __name__ == '__main__':
    main()
