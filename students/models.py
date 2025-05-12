from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone
from django.utils.text import slugify
from pathlib import Path

def student_image_upload_path(instance, filename):
    """Generates the upload path for student profile images using pathlib."""
    student_id_slug = slugify(instance.student_id)
    return str(Path('student_data') / student_id_slug / 'profile_images' / filename)

def student_qr_code_upload_path(instance, filename):
    """Generates the upload path for student QR codes using pathlib."""
    student_id_slug = slugify(instance.student_id)
    return str(Path('student_data') / student_id_slug / 'qr_codes' / filename)

def belonging_image_upload_path(instance, filename):
    """Generates the upload path for belonging images."""
    student_id_slug = slugify(instance.student.student_id)
    return str(Path('student_data') / student_id_slug / 'belonging_images' / filename)

class Student(models.Model):
    DEPARTMENTS = [
        ('CS', 'Computer Science'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('SE', 'Software Engineering'),
        # Add more as needed
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    student_id = models.CharField(max_length=100, unique=True, db_index=True)
    image = models.ImageField(upload_to=student_image_upload_path, null=True, blank=True)
    qr_code = models.ImageField(upload_to=student_qr_code_upload_path, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        # Generate QR code
        qr_data = f'{self.student_id}'
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_file_name = f"{slugify(self.student_id)}_qr.png"
        self.qr_code.save(qr_file_name, File(buffer), save=False)

        # Rename the profile image file (optional)
        if self.image:
            file_extension = self.image.name.split('.')[-1].lower()
            new_image_name = f"profile.{file_extension}"
            self.image.name = new_image_name

        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    get_full_name.short_description = "Full Name"
    full_name = get_full_name

    def __str__(self):
        return self.get_full_name()

class Belonging(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='belongings')
    name = models.CharField(max_length=100)  # e.g., Laptop, Backpack
    identifier = models.CharField(max_length=255, null=True, blank=True, unique=True)  # Serial number or description
    image = models.ImageField(upload_to=belonging_image_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Rename the profile image file (optional)
        if self.image:
            file_extension = self.image.name.split('.')[-1].lower()
            new_image_name = f"{self.student.first_name}'s-{self.name}.{file_extension}"
            self.image.name = new_image_name

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.identifier}"