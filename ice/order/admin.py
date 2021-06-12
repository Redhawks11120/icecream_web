from django.contrib import admin

# Register your models here.
from .models import Ice_Cream, Comments, Statistics

admin.site.register(Ice_Cream)
admin.site.register(Comments)
admin.site.register(Statistics)