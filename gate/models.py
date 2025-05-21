from django.db import models

class GateLocation(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Active", null=True, blank=True)

    class Meta:
        verbose_name = "Gate Location"
        verbose_name_plural = "Gate Locations"

    def __str__(self):
        return self.name

