from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True, null = True)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.review}"
