from django.db import models
from users.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    introdution = models.TextField()
    image = models.ImageField(blank=True, null=True)
    brand = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="like_products")

    def __str__(self):
        return str(self.name)
    
