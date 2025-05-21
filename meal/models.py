from django.db import models
from django.utils import timezone

class Cafeteria(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Active", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cafeteria"
        verbose_name_plural = "Cafeterias"

class MealRecord(models.Model):
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='meal_records',
        verbose_name="Student",
        db_index=True
    )

    # Store timestamp in UTC (Django default)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="Scan Timestamp")

    MEAL_TYPE_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    )
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE_CHOICES, verbose_name="Meal Type")

    # Used for unique constraints and daily logic
    date = models.DateField(verbose_name="Date", db_index=True)

    def save(self, *args, **kwargs):
        if self.timestamp:
            # Convert timestamp to local time to get the correct local date
            local_timestamp = timezone.localtime(self.timestamp)
            self.date = local_timestamp.date()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Meal Record"
        verbose_name_plural = "Meal Records"
        ordering = ['-timestamp']
        unique_together = [['student', 'date', 'meal_type']]

    def __str__(self):
        student_name = self.student.get_full_name() if self.student else "Unknown Student"
        meal_type_display = self.get_meal_type_display()
        time_str = timezone.localtime(self.timestamp).strftime('%Y-%m-%d %H:%M')  # show in local time
        return f"{meal_type_display} for {student_name} at {time_str}"
