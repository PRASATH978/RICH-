from django.contrib import admin
from .models import Product
from .models import UserProfile
from .models import Purchase

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Purchase)
