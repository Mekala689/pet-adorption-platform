from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import Notification, AdoptionRequest
from .forms import AdoptionRequestForm
from apps.pets.models import Pet


@login_required
def notifications_list(request):
    """List all notifications for the current user"""
    notifications = Notification.objects.filter(recipient=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications[:20],  # Latest 20 notifications
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications:list')


@login_required
def mark_all_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(recipient=request.user, is_read=False).update(
        is_read=True, 
        read_at=timezone.now()
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications:list')


@login_required
def get_unread_count(request):
    """Get unread notification count (AJAX endpoint)"""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})


@login_required
def quick_adoption_request(request, pet_id):
    """Quick adoption request from home page"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.user.user_type != 'adopter':
        messages.error(request, 'Only adopters can submit adoption requests.')
        return redirect('core:home')
    
    # Check if user already has a request for this pet
    existing_request = AdoptionRequest.objects.filter(requester=request.user, pet=pet).first()
    if existing_request:
        messages.warning(request, f'You already have a request for {pet.name}.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.requester = request.user
            adoption_request.pet = pet
            adoption_request.save()
            
            # Create notification for shelter
            Notification.objects.create(
                recipient=pet.shelter,
                sender=request.user,
                notification_type='adoption_request',
                title=f'New Adoption Request for {pet.name}',
                message=f'{request.user.get_full_name() or request.user.username} has submitted an adoption request for {pet.name}.',
                pet=pet,
                is_important=True
            )
            
            # Create confirmation notification for requester
            Notification.objects.create(
                recipient=request.user,
                notification_type='adoption_request',
                title=f'Adoption Request Submitted for {pet.name}',
                message=f'Your adoption request for {pet.name} has been submitted successfully. The shelter will contact you soon.',
                pet=pet
            )
            
            messages.success(request, f'Your adoption request for {pet.name} has been submitted!')
            return redirect('core:home')
    else:
        form = AdoptionRequestForm()
    
    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'notifications/quick_request_form.html', context)


class AdoptionRequestListView(LoginRequiredMixin, ListView):
    model = AdoptionRequest
    template_name = 'notifications/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'adopter':
            return AdoptionRequest.objects.filter(requester=user)
        elif user.user_type == 'shelter':
            return AdoptionRequest.objects.filter(pet__shelter=user)
        else:
            return AdoptionRequest.objects.all()


class AdoptionRequestDetailView(LoginRequiredMixin, DetailView):
    model = AdoptionRequest
    template_name = 'notifications/request_detail.html'
    context_object_name = 'request'
    
    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        # Check permissions
        if (user != obj.requester and 
            user != obj.pet.shelter and 
            not user.is_staff):
            raise PermissionDenied()
        
        return obj


@login_required
def respond_to_request(request, request_id):
    """Shelter responds to adoption request"""
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    
    if request.user != adoption_request.pet.shelter:
        messages.error(request, 'You can only respond to requests for your pets.')
        return redirect('notifications:request_list')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        response_message = request.POST.get('response_message', '')
        
        if action == 'approve':
            adoption_request.status = 'approved'
            notification_title = f'Your adoption request for {adoption_request.pet.name} has been approved!'
            notification_message = f'Great news! Your request to adopt {adoption_request.pet.name} has been approved. The shelter will contact you soon to proceed with the adoption process.'
        elif action == 'reject':
            adoption_request.status = 'rejected'
            notification_title = f'Update on your adoption request for {adoption_request.pet.name}'
            notification_message = f'Thank you for your interest in {adoption_request.pet.name}. Unfortunately, we cannot proceed with your request at this time.'
        else:
            messages.error(request, 'Invalid action.')
            return redirect('notifications:request_detail', pk=request_id)
        
        adoption_request.shelter_response = response_message
        adoption_request.responded_at = timezone.now()
        adoption_request.save()
        
        # Create notification for requester
        Notification.objects.create(
            recipient=adoption_request.requester,
            sender=request.user,
            notification_type='application_approved' if action == 'approve' else 'application_rejected',
            title=notification_title,
            message=notification_message + (f'\n\nShelter message: {response_message}' if response_message else ''),
            pet=adoption_request.pet,
            adoption_application=None,
            is_important=True
        )
        
        messages.success(request, f'Request has been {action}d successfully.')
        return redirect('notifications:request_detail', pk=request_id)
    
    context = {
        'adoption_request': adoption_request,
    }
    return render(request, 'notifications/respond_to_request.html', context)


def create_notification(recipient, notification_type, title, message, sender=None, pet=None, adoption_application=None, is_important=False):
    """Utility function to create notifications"""
    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        pet=pet,
        adoption_application=adoption_application,
        is_important=is_important
    )
