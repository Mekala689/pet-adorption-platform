from django.db import models
from django.urls import reverse
from apps.users.models import User
from apps.pets.models import Pet


class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Adoption Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_applications')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Application Details
    reason_for_adoption = models.TextField(help_text="Why do you want to adopt this pet?")
    experience_with_pets = models.TextField(help_text="Describe your experience with pets")
    living_situation = models.TextField(help_text="Describe your living situation")
    work_schedule = models.TextField(help_text="Describe your work schedule and how it affects pet care")
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relationship = models.CharField(max_length=50)
    
    # Veterinarian Information
    veterinarian_name = models.CharField(max_length=100, blank=True)
    veterinarian_phone = models.CharField(max_length=15, blank=True)
    veterinarian_address = models.TextField(blank=True)
    
    # Additional Information
    additional_notes = models.TextField(blank=True, help_text="Any additional information you'd like to share")
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Review Information
    reviewer_notes = models.TextField(blank=True, help_text="Notes from the shelter reviewer")
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['applicant', 'pet']
    
    def __str__(self):
        return f"Application by {self.applicant.username} for {self.pet.name}"
    
    def get_absolute_url(self):
        return reverse('adoptions:detail', kwargs={'pk': self.pk})
    
    @property
    def can_be_approved(self):
        return self.status == 'pending'
    
    @property
    def can_be_rejected(self):
        return self.status == 'pending'
    
    @property
    def can_be_completed(self):
        return self.status == 'approved'


class AdoptionInterview(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone Interview'),
        ('video', 'Video Call'),
        ('in_person', 'In-Person Meeting'),
        ('home_visit', 'Home Visit'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conducted_interviews')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.get_interview_type_display()} for {self.application}"


class AdoptionDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('contract', 'Adoption Contract'),
        ('medical_records', 'Medical Records'),
        ('vaccination_records', 'Vaccination Records'),
        ('identification', 'ID Document'),
        ('proof_of_residence', 'Proof of Residence'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='adoption_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.application}"
