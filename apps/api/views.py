"""
API Views for Pet Adoption Platform
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import login
from django.db.models import Q, Count
from django.utils import timezone

from apps.users.models import User, ShelterProfile, AdopterProfile
from apps.pets.models import Pet, PetFavorite
from apps.adoptions.models import AdoptionApplication
from .serializers import *
from .filters import PetFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for immediate login
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PetListCreateView(generics.ListCreateAPIView):
    queryset = Pet.objects.filter(status='available')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PetFilter
    search_fields = ['name', 'breed', 'description', 'personality_traits']
    ordering_fields = ['created_at', 'name', 'age_years', 'adoption_fee']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PetCreateUpdateSerializer
        return PetListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'shelter':
            raise permissions.PermissionDenied("Only shelters can add pets")
        serializer.save(shelter=self.request.user)


class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetDetailSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PetCreateUpdateSerializer
        return PetDetailSerializer
    
    def perform_update(self, serializer):
        if self.request.user != self.get_object().shelter:
            raise permissions.PermissionDenied("You can only edit your own pets")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user != instance.shelter:
            raise permissions.PermissionDenied("You can only delete your own pets")
        instance.delete()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request, pet_id):
    """Toggle favorite status for a pet"""
    try:
        pet = Pet.objects.get(id=pet_id)
        favorite, created = PetFavorite.objects.get_or_create(
            user=request.user, pet=pet
        )
        
        if not created:
            favorite.delete()
            return Response({
                'favorited': False,
                'message': f'{pet.name} removed from favorites'
            })
        else:
            return Response({
                'favorited': True,
                'message': f'{pet.name} added to favorites'
            })
    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class FavoritePetsView(generics.ListAPIView):
    serializer_class = PetListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Pet.objects.filter(
            favorited_by__user=self.request.user
        ).order_by('-favorited_by__created_at')


class AdoptionApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'adopter':
            return AdoptionApplication.objects.filter(applicant=user)
        elif user.user_type == 'shelter':
            return AdoptionApplication.objects.filter(pet__shelter=user)
        else:  # admin
            return AdoptionApplication.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'adopter':
            raise permissions.PermissionDenied("Only adopters can submit applications")
        serializer.save(applicant=self.request.user)


class AdoptionApplicationDetailView(generics.RetrieveUpdateAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        # Check permissions
        if (user != obj.applicant and 
            user != obj.pet.shelter and 
            not user.is_staff):
            raise permissions.PermissionDenied()
        
        return obj


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_application_status(request, application_id):
    """Update adoption application status"""
    try:
        application = AdoptionApplication.objects.get(id=application_id)
        
        # Only shelter can update status
        if request.user != application.pet.shelter:
            raise permissions.PermissionDenied()
        
        new_status = request.data.get('status')
        reviewer_notes = request.data.get('reviewer_notes', '')
        
        if new_status not in ['approved', 'rejected', 'completed']:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = new_status
        application.reviewer_notes = reviewer_notes
        application.reviewed_at = timezone.now()
        
        if new_status == 'completed':
            application.completed_at = timezone.now()
            application.pet.status = 'adopted'
            application.pet.save()
        elif new_status == 'approved':
            application.pet.status = 'pending'
            application.pet.save()
        
        application.save()
        
        return Response({
            'message': f'Application {new_status} successfully',
            'application': AdoptionApplicationSerializer(application).data
        })
        
    except AdoptionApplication.DoesNotExist:
        return Response(
            {'error': 'Application not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def platform_stats(request):
    """Get platform statistics"""
    stats = {
        'total_pets': Pet.objects.count(),
        'available_pets': Pet.objects.filter(status='available').count(),
        'adopted_pets': Pet.objects.filter(status='adopted').count(),
        'pending_applications': AdoptionApplication.objects.filter(status='pending').count(),
        'total_shelters': User.objects.filter(user_type='shelter').count(),
        'total_adopters': User.objects.filter(user_type='adopter').count(),
        'pets_by_species': list(
            Pet.objects.values('species')
            .annotate(count=Count('species'))
            .order_by('-count')
        ),
        'recent_adoptions': list(
            AdoptionApplication.objects.filter(status='completed')
            .select_related('pet', 'applicant')
            .order_by('-completed_at')[:5]
            .values(
                'pet__name', 'pet__species', 'applicant__first_name',
                'completed_at'
            )
        )
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def search_pets(request):
    """Advanced pet search"""
    serializer = SearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    queryset = Pet.objects.filter(status='available')
    
    # Apply filters
    filters = serializer.validated_data
    
    if filters.get('query'):
        query = filters['query']
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(breed__icontains=query) |
            Q(description__icontains=query) |
            Q(personality_traits__icontains=query)
        )
    
    if filters.get('species'):
        queryset = queryset.filter(species=filters['species'])
    
    if filters.get('breed'):
        queryset = queryset.filter(breed__icontains=filters['breed'])
    
    if filters.get('size'):
        queryset = queryset.filter(size=filters['size'])
    
    if filters.get('gender'):
        queryset = queryset.filter(gender=filters['gender'])
    
    if filters.get('age_min') is not None:
        queryset = queryset.filter(age_years__gte=filters['age_min'])
    
    if filters.get('age_max') is not None:
        queryset = queryset.filter(age_years__lte=filters['age_max'])
    
    if filters.get('good_with_kids') is not None:
        queryset = queryset.filter(good_with_kids=filters['good_with_kids'])
    
    if filters.get('good_with_dogs') is not None:
        queryset = queryset.filter(good_with_dogs=filters['good_with_dogs'])
    
    if filters.get('good_with_cats') is not None:
        queryset = queryset.filter(good_with_cats=filters['good_with_cats'])
    
    if filters.get('house_trained') is not None:
        queryset = queryset.filter(house_trained=filters['house_trained'])
    
    if filters.get('max_fee') is not None:
        queryset = queryset.filter(adoption_fee__lte=filters['max_fee'])
    
    if filters.get('location'):
        location = filters['location']
        queryset = queryset.filter(
            Q(shelter__city__icontains=location) |
            Q(shelter__state__icontains=location)
        )
    
    # Paginate results
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = PetListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    serializer = PetListSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)
