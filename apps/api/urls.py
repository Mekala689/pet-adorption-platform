"""
API URLs for Pet Adoption Platform
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/profile/', views.UserProfileView.as_view(), name='profile'),
    
    # Pets
    path('pets/', views.PetListCreateView.as_view(), name='pet-list'),
    path('pets/<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    path('pets/<int:pet_id>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('pets/search/', views.search_pets, name='search-pets'),
    path('pets/favorites/', views.FavoritePetsView.as_view(), name='favorite-pets'),
    
    # Adoptions
    path('adoptions/', views.AdoptionApplicationListCreateView.as_view(), name='adoption-list'),
    path('adoptions/<int:pk>/', views.AdoptionApplicationDetailView.as_view(), name='adoption-detail'),
    path('adoptions/<int:application_id>/status/', views.update_application_status, name='update-application-status'),
    
    # Platform
    path('stats/', views.platform_stats, name='platform-stats'),
]
