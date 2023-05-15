from django.db import models
from django.urls import reverse
from users.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    image = models.ImageField(blank=True, null=True)
    brand = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="like_products")

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"product_id":self.id})

    def __str__(self):
        return str(self.name)
    

class ProductReview(models.Model):
    SCORE_CHOICES = (
        (1, '1점'),
        (2, '2점'),
        (3, '3점'),
        (4, '4점'),
        (5, '5점'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.IntegerField(choices=SCORE_CHOICES)
    content = models.TextField()
    price = models.IntegerField(blank=True, null=True)
    store = models.CharField(max_length=50, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="like_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self,product_id):
        return reverse('product_review_detail', kwargs={"product_id":product_id, "review_id":self.id})

    def __str__(self):
        if len(str(self.content))>=15:
            title = str(self.content)[:15]+'...'
        else: title = str(self.content)
        return title
