from django.contrib import admin
from .models import GateLocation


# Register your models here.
@admin.register(GateLocation)
class GateLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
