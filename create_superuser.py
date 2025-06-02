#!/usr/bin/env python
"""
Script to create a superuser for the Pet Adoption Platform
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption.settings')
django.setup()

from apps.users.models import User

def create_superuser():
    """Create a superuser if one doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type='admin'
        )
        print("✅ Superuser 'admin' created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@example.com")
    else:
        print("ℹ️  Superuser 'admin' already exists")

if __name__ == '__main__':
    create_superuser()
