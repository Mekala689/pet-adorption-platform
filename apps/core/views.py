from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from apps.pets.models import Pet
from apps.adoptions.models import AdoptionApplication
from apps.users.models import User


def home(request):
    """Home page view"""
    # Get statistics for the home page
    total_pets = Pet.objects.filter(status='available').count()
    total_adopted = Pet.objects.filter(status='adopted').count()
    pending_applications = AdoptionApplication.objects.filter(status='pending').count()

    # Get featured pets (latest available pets)
    featured_pets = Pet.objects.filter(status='available').select_related('shelter').prefetch_related('images')[:6]

    # Get pets by species for statistics
    pets_by_species = Pet.objects.filter(status='available').values('species').annotate(count=Count('species'))

    context = {
        'total_pets': total_pets,
        'total_adopted': total_adopted,
        'pending_applications': pending_applications,
        'featured_pets': featured_pets,
        'pets_by_species': pets_by_species,
    }

    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """Dashboard view for different user types"""
    user = request.user
    context = {'user': user}

    if user.user_type == 'shelter':
        # Shelter dashboard statistics
        my_pets = Pet.objects.filter(shelter=user)
        context.update({
            'total_pets': my_pets.count(),
            'available_pets': my_pets.filter(status='available').count(),
            'pending_pets': my_pets.filter(status='pending').count(),
            'adopted_pets': my_pets.filter(status='adopted').count(),
            'pending_applications': AdoptionApplication.objects.filter(
                pet__shelter=user, status='pending'
            ).count(),
            'approved_applications': AdoptionApplication.objects.filter(
                pet__shelter=user, status='approved'
            ).count(),
            'recent_pets': my_pets.order_by('-created_at')[:5],
            'recent_applications': AdoptionApplication.objects.filter(
                pet__shelter=user
            ).order_by('-submitted_at')[:5],
        })
        return render(request, 'core/shelter_dashboard.html', context)

    elif user.user_type == 'adopter':
        # Adopter dashboard statistics
        my_applications = AdoptionApplication.objects.filter(applicant=user)
        context.update({
            'total_applications': my_applications.count(),
            'pending_applications': my_applications.filter(status='pending').count(),
            'approved_applications': my_applications.filter(status='approved').count(),
            'completed_adoptions': my_applications.filter(status='completed').count(),
            'recent_applications': my_applications.order_by('-submitted_at')[:5],
            'favorite_pets_count': user.favorite_pets.count(),
        })
        return render(request, 'core/adopter_dashboard.html', context)

    elif user.user_type == 'admin':
        # Admin dashboard statistics
        context.update({
            'total_users': User.objects.count(),
            'total_shelters': User.objects.filter(user_type='shelter').count(),
            'total_adopters': User.objects.filter(user_type='adopter').count(),
            'total_pets': Pet.objects.count(),
            'available_pets': Pet.objects.filter(status='available').count(),
            'adopted_pets': Pet.objects.filter(status='adopted').count(),
            'total_applications': AdoptionApplication.objects.count(),
            'pending_applications': AdoptionApplication.objects.filter(status='pending').count(),
            'completed_adoptions': AdoptionApplication.objects.filter(status='completed').count(),
            'recent_users': User.objects.order_by('-date_joined')[:5],
            'recent_pets': Pet.objects.order_by('-created_at')[:5],
        })
        return render(request, 'core/admin_dashboard.html', context)

    # Default redirect to home
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')
