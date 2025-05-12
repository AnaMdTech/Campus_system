from django.contrib import admin
from .models import Student, Belonging

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'department')
    search_fields = ('first_name', 'last_name', 'student_id')
    list_filter = ('department',)
    ordering = ('first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at', 'qr_code')

admin.site.register(Belonging)