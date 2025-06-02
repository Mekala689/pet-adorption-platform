from django.urls import path
from . import views

app_name = 'adoptions'

urlpatterns = [
    # Application URLs
    path('', views.AdoptionApplicationListView.as_view(), name='list'),
    path('<int:pk>/', views.AdoptionApplicationDetailView.as_view(), name='detail'),
    path('apply/<int:pet_pk>/', views.AdoptionApplicationCreateView.as_view(), name='apply'),
    
    # Application actions
    path('<int:pk>/approve/', views.approve_application, name='approve'),
    path('<int:pk>/reject/', views.reject_application, name='reject'),
    path('<int:pk>/complete/', views.complete_adoption, name='complete'),
    
    # Interview URLs
    path('<int:application_pk>/interview/add/', views.AdoptionInterviewCreateView.as_view(), name='add_interview'),
    
    # Document URLs
    path('<int:application_pk>/document/add/', views.AdoptionDocumentCreateView.as_view(), name='add_document'),
]
