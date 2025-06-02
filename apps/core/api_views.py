from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from apps.pets.models import Pet
from apps.adoptions.models import AdoptionApplication


@api_view(['GET'])
def stats_api(request):
    """API endpoint for platform statistics"""
    stats = {
        'total_pets_available': Pet.objects.filter(status='available').count(),
        'total_pets_adopted': Pet.objects.filter(status='adopted').count(),
        'pending_applications': AdoptionApplication.objects.filter(status='pending').count(),
        'completed_adoptions': AdoptionApplication.objects.filter(status='completed').count(),
        'pets_by_species': list(
            Pet.objects.filter(status='available')
            .values('species')
            .annotate(count=Count('species'))
        ),
        'pets_by_size': list(
            Pet.objects.filter(status='available')
            .values('size')
            .annotate(count=Count('size'))
        ),
    }
    
    return Response(stats)
