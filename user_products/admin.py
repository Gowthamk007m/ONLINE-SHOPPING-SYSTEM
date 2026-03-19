from django.contrib import admin
from .models import Feedback, ReviewRating

admin.site.register(ReviewRating)
admin.site.register(Feedback)
