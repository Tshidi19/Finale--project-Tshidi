from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, Review
from .forms import RecipeForm
from django.urls import reverse
from django.core.exceptions import PermissionDenied

# Registration View
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            form.save()  
            messages.success(self.request, 'Registration successful. You can now log in.')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error occurred during registration: {str(e)}')
            return self.form_invalid(form)

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        try:
            request.user.delete()  
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error occurred while deleting your account: {str(e)}')

    return render(request, 'registration/delete_account.html')

# The following are recipe and review based views

class HomePageView(TemplateView):
    template_name = 'weightloss_app/home.html'

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm  
    template_name = 'weightloss_app/recipe_form.html'  
    success_url = reverse_lazy('recipe_page')

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user  
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error occurred while creating the recipe: {str(e)}')
            return self.form_invalid(form)

class RecipePageView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'weightloss_app/recipes.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RecipeForm()  
        return context

    def post(self, request, *args, **kwargs):
        form = RecipeForm(request.POST)
        if form.is_valid():
            try:
                recipe = form.save(commit=False)
                recipe.user = request.user  
                recipe.save()
                messages.success(request, 'Recipe created successfully.')
                return redirect('recipes')
            except Exception as e:
                messages.error(request, f'Error occurred while saving the recipe: {str(e)}')
        else:
            messages.error(request, 'There were errors in your form.')
        
        return self.get(request, *args, **kwargs)  

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'weightloss_app/recipe_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.review_set.all()  
        return context

    def post(self, request, *args, **kwargs):
    
        recipe = self.get_object()
        
        review_content = request.POST.get('review')

        if review_content: 
            try:
                Review.objects.create(
                    recipe=recipe,
                    user=request.user,
                    review=review_content
                )
                messages.success(request, 'Review submitted successfully.')
            except Exception as e:
                messages.error(request, f'Error occurred while submitting the review: {str(e)}')

        # Always return an HttpResponse - in this case, a redirect to the recipe detail page
        return redirect(reverse('recipe_detail', kwargs={'pk': recipe.pk}))

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'weightloss_app/recipe_form.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error occurred while updating the recipe: {str(e)}')
            return self.form_invalid(form)

class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'weightloss_app/recipe_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('recipe_page')  

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, 'You do not have permission to delete this recipe.')
            return redirect('recipe_page')
        except Exception as e:
            messages.error(request, f'Error occurred while deleting the recipe: {str(e)}')
            return redirect('recipe_page')

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'weightloss_app/review_confirm_delete.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        return context

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.recipe.pk})

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error occurred while deleting the review: {str(e)}')
            return redirect(self.get_success_url())
            