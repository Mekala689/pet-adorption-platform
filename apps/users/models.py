from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('adopter', 'Adopter'),
        ('shelter', 'Shelter'),
        ('admin', 'Admin'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='adopter')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class ShelterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shelter_profile')
    organization_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField(help_text="Maximum number of animals the shelter can house")
    established_date = models.DateField()
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.organization_name


class AdopterProfile(models.Model):
    HOUSING_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condominium'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adopter_profile')
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPE_CHOICES)
    has_yard = models.BooleanField(default=False)
    has_other_pets = models.BooleanField(default=False)
    other_pets_description = models.TextField(blank=True)
    household_members = models.PositiveIntegerField(default=1)
    experience_with_pets = models.TextField(blank=True)
    preferred_pet_age = models.CharField(max_length=50, blank=True)
    preferred_pet_size = models.CharField(max_length=50, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.full_name} - Adopter Profile"
