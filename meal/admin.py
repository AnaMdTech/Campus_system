from django.contrib import admin
from .models import MealRecord
from .models import Cafeteria

# Register your models here.
admin.site.register(MealRecord)

@admin.register(Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
