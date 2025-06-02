"""
API Serializers for Pet Adoption Platform
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User, ShelterProfile, AdopterProfile
from apps.pets.models import Pet, PetImage, PetFavorite
from apps.adoptions.models import AdoptionApplication, AdoptionInterview, AdoptionDocument


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 
                 'phone_number', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name',
                 'user_type', 'phone_number', 'address', 'city', 'state', 'zip_code',
                 'profile_picture', 'date_of_birth', 'date_joined']
        read_only_fields = ['id', 'username', 'user_type', 'date_joined']


class ShelterProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = ShelterProfile
        fields = '__all__'


class AdopterProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = AdopterProfile
        fields = '__all__'


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = ['id', 'image', 'caption', 'is_primary', 'uploaded_at']


class PetListSerializer(serializers.ModelSerializer):
    shelter_name = serializers.CharField(source='shelter.shelter_profile.organization_name', read_only=True)
    shelter_city = serializers.CharField(source='shelter.city', read_only=True)
    main_image = serializers.SerializerMethodField()
    age_display = serializers.CharField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'age_years', 'age_months', 'age_display',
                 'gender', 'size', 'weight', 'color', 'status', 'adoption_fee',
                 'good_with_kids', 'good_with_dogs', 'good_with_cats', 'house_trained',
                 'is_spayed_neutered', 'is_vaccinated', 'shelter_name', 'shelter_city',
                 'main_image', 'is_favorited', 'created_at']
    
    def get_main_image(self, obj):
        main_image = obj.main_image
        if main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.image.url)
        return None
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PetFavorite.objects.filter(user=request.user, pet=obj).exists()
        return False


class PetDetailSerializer(serializers.ModelSerializer):
    shelter = ShelterProfileSerializer(source='shelter.shelter_profile', read_only=True)
    images = PetImageSerializer(many=True, read_only=True)
    age_display = serializers.CharField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    can_apply = serializers.SerializerMethodField()
    
    class Meta:
        model = Pet
        fields = '__all__'
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PetFavorite.objects.filter(user=request.user, pet=obj).exists()
        return False
    
    def get_can_apply(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.user_type == 'adopter':
            return not AdoptionApplication.objects.filter(
                applicant=request.user, pet=obj
            ).exists() and obj.status == 'available'
        return False


class PetCreateUpdateSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    
    class Meta:
        model = Pet
        exclude = ['shelter', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        pet = Pet.objects.create(**validated_data)
        
        for i, image in enumerate(uploaded_images):
            PetImage.objects.create(
                pet=pet,
                image=image,
                is_primary=(i == 0),
                caption=f"Photo of {pet.name}"
            )
        
        return pet


class AdoptionApplicationSerializer(serializers.ModelSerializer):
    pet = PetListSerializer(read_only=True)
    applicant = UserProfileSerializer(read_only=True)
    pet_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AdoptionApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'submitted_at', 'reviewed_at', 'completed_at']
    
    def create(self, validated_data):
        pet_id = validated_data.pop('pet_id')
        pet = Pet.objects.get(id=pet_id)
        validated_data['pet'] = pet
        return super().create(validated_data)


class AdoptionInterviewSerializer(serializers.ModelSerializer):
    application = AdoptionApplicationSerializer(read_only=True)
    
    class Meta:
        model = AdoptionInterview
        fields = '__all__'


class AdoptionDocumentSerializer(serializers.ModelSerializer):
    application = AdoptionApplicationSerializer(read_only=True)
    
    class Meta:
        model = AdoptionDocument
        fields = '__all__'


class PlatformStatsSerializer(serializers.Serializer):
    total_pets = serializers.IntegerField()
    available_pets = serializers.IntegerField()
    adopted_pets = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    total_shelters = serializers.IntegerField()
    total_adopters = serializers.IntegerField()
    pets_by_species = serializers.ListField()
    recent_adoptions = serializers.ListField()


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False, allow_blank=True)
    species = serializers.CharField(required=False, allow_blank=True)
    breed = serializers.CharField(required=False, allow_blank=True)
    size = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    age_min = serializers.IntegerField(required=False, min_value=0)
    age_max = serializers.IntegerField(required=False, min_value=0)
    good_with_kids = serializers.BooleanField(required=False)
    good_with_dogs = serializers.BooleanField(required=False)
    good_with_cats = serializers.BooleanField(required=False)
    house_trained = serializers.BooleanField(required=False)
    max_fee = serializers.DecimalField(required=False, max_digits=8, decimal_places=2)
    location = serializers.CharField(required=False, allow_blank=True)
