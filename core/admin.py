from django.contrib import admin
from .models import Product
from .models import UserProfile

admin.site.register(Product,)
admin.site.register(UserProfile)
