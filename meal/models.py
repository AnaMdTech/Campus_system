from django.db import models
from django.utils import timezone

class MealRecord(models.Model):
    # Link to the student who ate
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE, # If student deleted, delete meal records
        related_name='meal_records',
        verbose_name="Student",
        db_index=True # Index for faster filtering by student
    )

    # Timestamp of when the meal was recorded (scan time)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="Scan Timestamp")

    # Type of meal (important for our 1-per-day logic)
    MEAL_TYPE_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    )
    # We'll determine this in the view based on the scan time
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE_CHOICES, verbose_name="Meal Type")

    class Meta:
        verbose_name = "Meal Record"
        verbose_name_plural = "Meal Records"
        # Unique together constraint: Ensure a student can only have one record
        # of a specific meal type on a specific date.
        # Note: This requires us to reliably set meal_type. We will handle the
        # date check mainly in the *view* logic before saving, but this
        # adds a database-level constraint for robustness.
        # We need a date field to make this constraint simple. Let's add one.
        # unique_together = ['student', 'date', 'meal_type'] # See added date field below

        ordering = ['-timestamp'] # Show most recent meals first

    # Add a date field derived from the timestamp for easier daily checks
    # and for the unique_together constraint.
    date = models.DateField(verbose_name="Date", db_index=True)

    def save(self, *args, **kwargs):
        # Automatically set the date field based on the timestamp before saving
        if self.timestamp:
            # Ensure timestamp is timezone-aware if using timezones
            # For simplicity here, assuming naive or settings.TIME_ZONE handled
             self.date = self.timestamp.date()
        super().save(*args, **kwargs) # Call the original save method

    class Meta: # Redefine Meta to include the unique_together after date field exists
         verbose_name = "Meal Record"
         verbose_name_plural = "Meal Records"
         ordering = ['-timestamp']
         # Constraint: A student cannot have two 'Breakfast' records on the same 'date'.
         unique_together = [['student', 'date', 'meal_type']]


    def __str__(self):
        student_name = self.student.get_full_name() if self.student else "Unknown Student"
        meal_type_display = self.get_meal_type_display()
        time_str = self.timestamp.strftime('%Y-%m-%d %H:%M') # Use timestamp for display
        return f"{meal_type_display} for {student_name} at {time_str}"