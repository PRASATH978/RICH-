from django.db import models
from datetime import date 

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    open_date = models.DateField(default=date.today)
    close_date = models.DateField(default=date.today)
    nye_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gain_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    mail = models.EmailField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
