from django.urls import path
from .views import RegisterView, HomePageView, RecipePageView, delete_account_view, RecipeCreateView, RecipePageView, RecipeDetailView, RecipeUpdateView, RecipeDeleteView, ReviewDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path('', HomePageView.as_view(), name = 'home'),
    path('recipes/create/', RecipeCreateView.as_view(), name='create_recipe'),
    path('recipes/', RecipePageView.as_view(), name='recipe_page'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]


