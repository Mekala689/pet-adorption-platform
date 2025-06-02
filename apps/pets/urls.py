from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.PetListView.as_view(), name='list'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='detail'),
    path('add/', views.PetCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.PetUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.PetDeleteView.as_view(), name='delete'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('my-pets/', views.my_pets, name='my_pets'),
]
