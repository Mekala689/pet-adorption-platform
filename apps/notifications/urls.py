from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Notifications
    path('', views.notifications_list, name='list'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
    
    # Adoption Requests
    path('quick-request/<int:pet_id>/', views.quick_adoption_request, name='quick_request'),
    path('requests/', views.AdoptionRequestListView.as_view(), name='request_list'),
    path('requests/<int:pk>/', views.AdoptionRequestDetailView.as_view(), name='request_detail'),
    path('requests/<int:request_id>/respond/', views.respond_to_request, name='respond_to_request'),
]
