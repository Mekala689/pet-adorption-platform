from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django_filters.views import FilterView
from .models import Pet, PetImage, PetFavorite
from .forms import PetForm, PetImageFormSet, PetSearchForm
from .filters import PetFilter


class PetListView(FilterView):
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'
    paginate_by = 12
    filterset_class = PetFilter
    
    def get_queryset(self):
        return Pet.objects.filter(status='available').select_related('shelter').prefetch_related('images')


class PetDetailView(DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorited'] = PetFavorite.objects.filter(
                user=self.request.user, 
                pet=self.object
            ).exists()
        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'shelter':
            messages.error(request, 'Only shelters can add pets.')
            return redirect('pets:list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = PetImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = PetImageFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        form.instance.shelter = self.request.user
        
        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, f'{self.object.name} has been added successfully!')
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        pet = self.get_object()
        if request.user != pet.shelter:
            messages.error(request, 'You can only edit your own pets.')
            return redirect('pets:list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = PetImageFormSet(
                self.request.POST, 
                self.request.FILES, 
                instance=self.object
            )
        else:
            context['image_formset'] = PetImageFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()
            image_formset.save()
            messages.success(self.request, f'{self.object.name} has been updated successfully!')
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet_confirm_delete.html'
    success_url = reverse_lazy('pets:list')
    
    def dispatch(self, request, *args, **kwargs):
        pet = self.get_object()
        if request.user != pet.shelter:
            messages.error(request, 'You can only delete your own pets.')
            return redirect('pets:list')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        pet = self.get_object()
        messages.success(request, f'{pet.name} has been deleted.')
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_favorite(request, pk):
    """Toggle favorite status for a pet"""
    pet = get_object_or_404(Pet, pk=pk)
    favorite, created = PetFavorite.objects.get_or_create(user=request.user, pet=pet)
    
    if not created:
        favorite.delete()
        messages.success(request, f'{pet.name} removed from favorites.')
    else:
        messages.success(request, f'{pet.name} added to favorites.')
    
    return redirect('pets:detail', pk=pk)


@login_required
def my_favorites(request):
    """Display user's favorite pets"""
    favorites = PetFavorite.objects.filter(user=request.user).select_related('pet')
    return render(request, 'pets/my_favorites.html', {'favorites': favorites})


@login_required
def my_pets(request):
    """Display shelter's pets"""
    if request.user.user_type != 'shelter':
        messages.error(request, 'Only shelters can view this page.')
        return redirect('pets:list')
    
    pets = Pet.objects.filter(shelter=request.user).prefetch_related('images')
    return render(request, 'pets/my_pets.html', {'pets': pets})
