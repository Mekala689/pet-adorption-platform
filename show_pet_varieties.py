#!/usr/bin/env python
"""
Script to display the variety of pets available on the platform
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption.settings')
django.setup()

from apps.pets.models import Pet
from collections import defaultdict

def show_pet_varieties():
    """Display all pet varieties with their details"""
    print("🐾 Pet Adoption Platform - Available Pet Varieties")
    print("=" * 60)
    
    # Group pets by species
    pets_by_species = defaultdict(list)
    for pet in Pet.objects.all().order_by('species', 'name'):
        pets_by_species[pet.species].append(pet)
    
    total_pets = Pet.objects.count()
    available_pets = Pet.objects.filter(status='available').count()
    
    print(f"📊 Platform Statistics:")
    print(f"   • Total Pets: {total_pets}")
    print(f"   • Available for Adoption: {available_pets}")
    print(f"   • Species Varieties: {len(pets_by_species)}")
    print()
    
    # Display each species
    species_icons = {
        'dog': '🐕',
        'cat': '🐱', 
        'bird': '🐦',
        'rabbit': '🐰',
        'hamster': '🐹',
        'guinea_pig': '🐹'
    }
    
    for species, pets in pets_by_species.items():
        icon = species_icons.get(species, '🐾')
        species_display = species.replace('_', ' ').title()
        
        print(f"{icon} {species_display}s ({len(pets)} available):")
        print("-" * 40)
        
        for pet in pets:
            status_icon = "✅" if pet.status == 'available' else "⏳" if pet.status == 'pending' else "🏠"
            photo_icon = "📸" if pet.images.exists() else "📷"
            
            print(f"  {status_icon} {photo_icon} {pet.name}")
            print(f"      Breed: {pet.breed}")
            print(f"      Age: {pet.age_display}")
            print(f"      Size: {pet.get_size_display()}")
            print(f"      Fee: ${pet.adoption_fee}")
            print(f"      Status: {pet.get_status_display()}")
            
            # Show traits
            traits = []
            if pet.good_with_kids:
                traits.append("Good with kids")
            if pet.good_with_dogs:
                traits.append("Good with dogs") 
            if pet.good_with_cats:
                traits.append("Good with cats")
            if pet.house_trained:
                traits.append("House trained")
            
            if traits:
                print(f"      Traits: {', '.join(traits)}")
            print()
        
        print()
    
    # Show breed variety
    print("🏷️  Breed Varieties:")
    print("-" * 30)
    breeds = Pet.objects.values_list('breed', flat=True).distinct().order_by('breed')
    for i, breed in enumerate(breeds, 1):
        print(f"  {i:2d}. {breed}")
    
    print()
    print("🌈 Age Range:")
    print("-" * 20)
    ages = []
    for pet in Pet.objects.all():
        if pet.age_years > 0:
            ages.append(pet.age_years)
        elif pet.age_months > 0:
            ages.append(pet.age_months / 12)
    
    if ages:
        print(f"   • Youngest: {min(ages):.1f} years")
        print(f"   • Oldest: {max(ages):.1f} years")
        print(f"   • Average: {sum(ages)/len(ages):.1f} years")
    
    print()
    print("💰 Adoption Fee Range:")
    print("-" * 25)
    fees = Pet.objects.values_list('adoption_fee', flat=True)
    if fees:
        print(f"   • Lowest: ${min(fees)}")
        print(f"   • Highest: ${max(fees)}")
        print(f"   • Average: ${sum(fees)/len(fees):.2f}")
    
    print()
    print("🏠 Shelter Distribution:")
    print("-" * 25)
    from apps.users.models import User
    shelters = User.objects.filter(user_type='shelter')
    for shelter in shelters:
        pet_count = Pet.objects.filter(shelter=shelter).count()
        shelter_name = getattr(shelter, 'shelter_profile', None)
        if shelter_name:
            name = shelter_name.organization_name
        else:
            name = shelter.get_full_name() or shelter.username
        print(f"   • {name}: {pet_count} pets")
    
    print()
    print("🎯 Quick Access URLs:")
    print("-" * 25)
    print("   • Browse All Pets: http://127.0.0.1:8000/pets/")
    print("   • Home Page: http://127.0.0.1:8000/")
    print("   • Admin Panel: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    show_pet_varieties()
