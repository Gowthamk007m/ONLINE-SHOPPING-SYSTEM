from django.db import models
from user_home.models import CustomUser
from admin_products.models import Product

class ReviewRating(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    updated_at = models.DateField(auto_now=True)
    
    def str(self):
        return self.review


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.buyer}'
