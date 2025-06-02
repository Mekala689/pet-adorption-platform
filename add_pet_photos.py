#!/usr/bin/env python
"""
Script to add sample pet photos to the Pet Adoption Platform
"""
import os
import sys
import django
import requests
from io import BytesIO
from PIL import Image

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption.settings')
django.setup()

from apps.pets.models import Pet, PetImage
from django.core.files.base import ContentFile

# Sample pet photos from Unsplash (free to use)
PET_PHOTOS = {
    'dog': [
        'https://images.unsplash.com/photo-1552053831-71594a27632d?w=500&h=500&fit=crop',  # Golden Retriever
        'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500&h=500&fit=crop',  # Beagle
        'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=500&h=500&fit=crop',  # German Shepherd
        'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop',  # Labrador
        'https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=500&h=500&fit=crop',  # Pit Bull
        'https://images.unsplash.com/photo-1544568100-847a948585b9?w=500&h=500&fit=crop',  # Cocker Spaniel
    ],
    'cat': [
        'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500&h=500&fit=crop',  # Siamese
        'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=500&h=500&fit=crop',  # Persian
        'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=500&h=500&fit=crop',  # Orange Tabby
        'https://images.unsplash.com/photo-1513245543132-31f507417b26?w=500&h=500&fit=crop',  # Black Cat
    ],
    'rabbit': [
        'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=500&h=500&fit=crop',  # Holland Lop
        'https://images.unsplash.com/photo-1606115915090-be18fea23ec7?w=500&h=500&fit=crop',  # Brown Rabbit
    ],
    'bird': [
        'https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=500&h=500&fit=crop',  # Colorful Bird
    ],
    'hamster': [
        'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=500&h=500&fit=crop',  # Hamster
    ],
    'guinea_pig': [
        'https://images.unsplash.com/photo-1548767797-d8c844163c4c?w=500&h=500&fit=crop',  # Guinea Pig
    ]
}

def download_image(url, pet_name, species):
    """Download an image from URL and return a Django file"""
    try:
        print(f"  📥 Downloading image for {pet_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Create a PIL Image to ensure it's valid
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        # Create Django file
        filename = f"{pet_name.lower().replace(' ', '_')}_{species}.jpg"
        return ContentFile(img_io.read(), name=filename)
        
    except Exception as e:
        print(f"  ❌ Error downloading image for {pet_name}: {e}")
        return None

def add_photos_to_pets():
    """Add photos to existing pets"""
    print("🖼️  Adding photos to pets...")
    
    pets = Pet.objects.all()
    photo_index = {}
    
    for pet in pets:
        species = pet.species
        if species not in PET_PHOTOS:
            print(f"  ⚠️  No photos available for species: {species}")
            continue
        
        # Get the next photo for this species
        if species not in photo_index:
            photo_index[species] = 0
        
        photos = PET_PHOTOS[species]
        photo_url = photos[photo_index[species] % len(photos)]
        photo_index[species] += 1
        
        # Check if pet already has images
        if pet.images.exists():
            print(f"  ℹ️  {pet.name} already has images, skipping...")
            continue
        
        # Download and add image
        image_file = download_image(photo_url, pet.name, species)
        if image_file:
            pet_image = PetImage.objects.create(
                pet=pet,
                image=image_file,
                caption=f"Photo of {pet.name}",
                is_primary=True
            )
            print(f"  ✅ Added photo to {pet.name} ({pet.get_species_display()})")
        else:
            print(f"  ❌ Failed to add photo to {pet.name}")

def create_additional_pets_with_photos():
    """Create additional pets with photos to showcase variety"""
    print("🐾 Creating additional pets with photos...")
    
    from apps.users.models import User
    from decimal import Decimal
    import random
    
    # Get shelters
    shelters = User.objects.filter(user_type='shelter')
    if not shelters.exists():
        print("  ❌ No shelters found!")
        return
    
    additional_pets = [
        {
            'name': 'Fluffy',
            'species': 'cat',
            'breed': 'Maine Coon',
            'age_years': 2,
            'age_months': 6,
            'gender': 'female',
            'size': 'large',
            'weight': Decimal('12.0'),
            'color': 'Gray and White',
            'description': 'Fluffy is a gentle giant Maine Coon who loves to be brushed and enjoys quiet companionship.',
            'personality_traits': 'Gentle, calm, affectionate, quiet',
            'good_with_kids': True,
            'good_with_dogs': True,
            'good_with_cats': True,
            'house_trained': True,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'adoption_fee': Decimal('200.00'),
        },
        {
            'name': 'Zippy',
            'species': 'bird',
            'breed': 'Cockatiel',
            'age_years': 1,
            'age_months': 6,
            'gender': 'male',
            'size': 'small',
            'weight': Decimal('0.3'),
            'color': 'Yellow and Gray',
            'description': 'Zippy is a cheerful cockatiel who loves to whistle and can learn simple tunes.',
            'personality_traits': 'Cheerful, vocal, intelligent, social',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': False,
            'house_trained': False,
            'is_spayed_neutered': False,
            'is_vaccinated': True,
            'adoption_fee': Decimal('75.00'),
        },
        {
            'name': 'Peanut',
            'species': 'hamster',
            'breed': 'Syrian Hamster',
            'age_years': 0,
            'age_months': 8,
            'gender': 'female',
            'size': 'small',
            'weight': Decimal('0.2'),
            'color': 'Golden Brown',
            'description': 'Peanut is an active little hamster who loves running on her wheel and exploring tunnels.',
            'personality_traits': 'Active, curious, playful, nocturnal',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': False,
            'house_trained': False,
            'is_spayed_neutered': False,
            'is_vaccinated': False,
            'adoption_fee': Decimal('25.00'),
        },
        {
            'name': 'Oreo',
            'species': 'guinea_pig',
            'breed': 'American Guinea Pig',
            'age_years': 1,
            'age_months': 3,
            'gender': 'male',
            'size': 'small',
            'weight': Decimal('2.5'),
            'color': 'Black and White',
            'description': 'Oreo is a social guinea pig who loves vegetables and enjoys being petted.',
            'personality_traits': 'Social, gentle, vocal, friendly',
            'good_with_kids': True,
            'good_with_dogs': False,
            'good_with_cats': False,
            'house_trained': False,
            'is_spayed_neutered': True,
            'is_vaccinated': True,
            'adoption_fee': Decimal('40.00'),
        }
    ]
    
    for pet_data in additional_pets:
        # Check if pet already exists
        if Pet.objects.filter(name=pet_data['name']).exists():
            print(f"  ℹ️  {pet_data['name']} already exists, skipping...")
            continue
        
        # Add shelter
        pet_data['shelter'] = random.choice(shelters)
        
        # Create pet
        pet = Pet.objects.create(**pet_data)
        print(f"  ✅ Created {pet.name} ({pet.get_species_display()})")
        
        # Add photo
        species = pet.species
        if species in PET_PHOTOS:
            photo_url = random.choice(PET_PHOTOS[species])
            image_file = download_image(photo_url, pet.name, species)
            if image_file:
                PetImage.objects.create(
                    pet=pet,
                    image=image_file,
                    caption=f"Photo of {pet.name}",
                    is_primary=True
                )
                print(f"  📸 Added photo to {pet.name}")

def main():
    """Main function to add pet photos"""
    print("🎨 Adding Pet Photos to Adoption Platform...")
    print("=" * 50)
    
    try:
        # Add photos to existing pets
        add_photos_to_pets()
        
        # Create additional pets with photos
        create_additional_pets_with_photos()
        
        # Summary
        total_pets = Pet.objects.count()
        pets_with_photos = Pet.objects.filter(images__isnull=False).distinct().count()
        
        print("=" * 50)
        print(f"📊 Summary:")
        print(f"   • Total Pets: {total_pets}")
        print(f"   • Pets with Photos: {pets_with_photos}")
        print(f"   • Species Available: {', '.join(Pet.objects.values_list('species', flat=True).distinct())}")
        
        print("\n🎉 Pet photos added successfully!")
        print("🌐 Visit http://127.0.0.1:8000/pets/ to see the updated pet listings!")
        
    except Exception as e:
        print(f"❌ Error adding pet photos: {e}")

if __name__ == '__main__':
    main()
