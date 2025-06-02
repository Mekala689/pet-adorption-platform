from django.db import models
from django.urls import reverse
from apps.users.models import User
from apps.pets.models import Pet
from apps.adoptions.models import AdoptionApplication


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('adoption_request', 'Adoption Request'),
        ('application_approved', 'Application Approved'),
        ('application_rejected', 'Application Rejected'),
        ('new_pet_added', 'New Pet Added'),
        ('adoption_completed', 'Adoption Completed'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('favorite_pet_adopted', 'Favorite Pet Adopted'),
        ('system_announcement', 'System Announcement'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    adoption_application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Quick request details
    message = models.TextField(help_text="Brief message about why you want to adopt this pet")
    phone_number = models.CharField(max_length=15, help_text="Contact phone number")
    preferred_contact_time = models.CharField(max_length=100, blank=True, help_text="Best time to contact you")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Response from shelter
    shelter_response = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['requester', 'pet']
    
    def __str__(self):
        return f"Request by {self.requester.username} for {self.pet.name}"
    
    def get_absolute_url(self):
        return reverse('notifications:request_detail', kwargs={'pk': self.pk})
