from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import AdoptionApplication, AdoptionInterview, AdoptionDocument
from .forms import AdoptionApplicationForm, AdoptionInterviewForm, AdoptionDocumentForm
from apps.pets.models import Pet


class AdoptionApplicationCreateView(LoginRequiredMixin, CreateView):
    model = AdoptionApplication
    form_class = AdoptionApplicationForm
    template_name = 'adoptions/application_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'adopter':
            messages.error(request, 'Only adopters can submit adoption applications.')
            return redirect('pets:list')
        
        self.pet = get_object_or_404(Pet, pk=kwargs['pet_pk'])
        
        # Check if user already has an application for this pet
        if AdoptionApplication.objects.filter(applicant=request.user, pet=self.pet).exists():
            messages.warning(request, 'You have already submitted an application for this pet.')
            return redirect('pets:detail', pk=self.pet.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.pet
        return context
    
    def form_valid(self, form):
        form.instance.applicant = self.request.user
        form.instance.pet = self.pet
        messages.success(self.request, 'Your adoption application has been submitted successfully!')
        return super().form_valid(form)


class AdoptionApplicationDetailView(LoginRequiredMixin, DetailView):
    model = AdoptionApplication
    template_name = 'adoptions/application_detail.html'
    context_object_name = 'application'
    
    def dispatch(self, request, *args, **kwargs):
        application = self.get_object()
        # Only allow applicant or shelter owner to view
        if request.user != application.applicant and request.user != application.pet.shelter:
            messages.error(request, 'You do not have permission to view this application.')
            return redirect('pets:list')
        return super().dispatch(request, *args, **kwargs)


class AdoptionApplicationListView(LoginRequiredMixin, ListView):
    model = AdoptionApplication
    template_name = 'adoptions/application_list.html'
    context_object_name = 'applications'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.user_type == 'adopter':
            return AdoptionApplication.objects.filter(applicant=self.request.user)
        elif self.request.user.user_type == 'shelter':
            return AdoptionApplication.objects.filter(pet__shelter=self.request.user)
        else:
            return AdoptionApplication.objects.none()


@login_required
def approve_application(request, pk):
    """Approve an adoption application"""
    application = get_object_or_404(AdoptionApplication, pk=pk)
    
    if request.user != application.pet.shelter:
        messages.error(request, 'You do not have permission to approve this application.')
        return redirect('adoptions:list')
    
    if application.can_be_approved:
        application.status = 'approved'
        application.reviewed_at = timezone.now()
        application.save()
        
        # Update pet status to pending
        application.pet.status = 'pending'
        application.pet.save()
        
        messages.success(request, f'Application for {application.pet.name} has been approved.')
    else:
        messages.error(request, 'This application cannot be approved.')
    
    return redirect('adoptions:detail', pk=pk)


@login_required
def reject_application(request, pk):
    """Reject an adoption application"""
    application = get_object_or_404(AdoptionApplication, pk=pk)
    
    if request.user != application.pet.shelter:
        messages.error(request, 'You do not have permission to reject this application.')
        return redirect('adoptions:list')
    
    if application.can_be_rejected:
        application.status = 'rejected'
        application.reviewed_at = timezone.now()
        application.save()
        
        messages.success(request, f'Application for {application.pet.name} has been rejected.')
    else:
        messages.error(request, 'This application cannot be rejected.')
    
    return redirect('adoptions:detail', pk=pk)


@login_required
def complete_adoption(request, pk):
    """Mark adoption as completed"""
    application = get_object_or_404(AdoptionApplication, pk=pk)
    
    if request.user != application.pet.shelter:
        messages.error(request, 'You do not have permission to complete this adoption.')
        return redirect('adoptions:list')
    
    if application.can_be_completed:
        application.status = 'completed'
        application.completed_at = timezone.now()
        application.save()
        
        # Update pet status to adopted
        application.pet.status = 'adopted'
        application.pet.save()
        
        messages.success(request, f'Adoption of {application.pet.name} has been completed!')
    else:
        messages.error(request, 'This adoption cannot be completed.')
    
    return redirect('adoptions:detail', pk=pk)


class AdoptionInterviewCreateView(LoginRequiredMixin, CreateView):
    model = AdoptionInterview
    form_class = AdoptionInterviewForm
    template_name = 'adoptions/interview_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.application = get_object_or_404(AdoptionApplication, pk=kwargs['application_pk'])
        
        if request.user != self.application.pet.shelter:
            messages.error(request, 'You do not have permission to schedule interviews for this application.')
            return redirect('adoptions:list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.application
        return context
    
    def form_valid(self, form):
        form.instance.application = self.application
        form.instance.interviewer = self.request.user
        messages.success(self.request, 'Interview has been scheduled successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.application.get_absolute_url()


class AdoptionDocumentCreateView(LoginRequiredMixin, CreateView):
    model = AdoptionDocument
    form_class = AdoptionDocumentForm
    template_name = 'adoptions/document_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.application = get_object_or_404(AdoptionApplication, pk=kwargs['application_pk'])
        
        # Allow both applicant and shelter to upload documents
        if request.user != self.application.applicant and request.user != self.application.pet.shelter:
            messages.error(request, 'You do not have permission to upload documents for this application.')
            return redirect('adoptions:list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.application
        return context
    
    def form_valid(self, form):
        form.instance.application = self.application
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Document has been uploaded successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.application.get_absolute_url()
