from django.db import models
from datetime import date
from django.contrib.auth.models import User

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

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.payment_id})"

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
