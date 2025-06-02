from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, ShelterProfile, AdopterProfile
from .forms import UserRegistrationForm, ShelterProfileForm, AdopterProfileForm


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile_setup')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, f'Account created for {username}!')
        return response


@login_required
def profile_setup(request):
    """Setup additional profile information based on user type"""
    user = request.user
    
    if user.user_type == 'shelter':
        if hasattr(user, 'shelter_profile'):
            return redirect('users:profile')
        
        if request.method == 'POST':
            form = ShelterProfileForm(request.POST)
            if form.is_valid():
                shelter_profile = form.save(commit=False)
                shelter_profile.user = user
                shelter_profile.save()
                messages.success(request, 'Shelter profile created successfully!')
                return redirect('users:profile')
        else:
            form = ShelterProfileForm()
        
        return render(request, 'users/shelter_setup.html', {'form': form})
    
    elif user.user_type == 'adopter':
        if hasattr(user, 'adopter_profile'):
            return redirect('users:profile')
        
        if request.method == 'POST':
            form = AdopterProfileForm(request.POST)
            if form.is_valid():
                adopter_profile = form.save(commit=False)
                adopter_profile.user = user
                adopter_profile.save()
                messages.success(request, 'Adopter profile created successfully!')
                return redirect('users:profile')
        else:
            form = AdopterProfileForm()
        
        return render(request, 'users/adopter_setup.html', {'form': form})
    
    return redirect('users:profile')


@login_required
def profile_view(request):
    """Display user profile"""
    context = {'user': request.user}
    
    if request.user.user_type == 'shelter' and hasattr(request.user, 'shelter_profile'):
        context['shelter_profile'] = request.user.shelter_profile
    elif request.user.user_type == 'adopter' and hasattr(request.user, 'adopter_profile'):
        context['adopter_profile'] = request.user.adopter_profile
    
    return render(request, 'users/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'profile_picture']
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
