from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Energy(models.Model):

    wellbeing = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a value from 1 (very unwell) to 10 (extremely well)",
    )
    mental_stress = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a value from 1 (no stress) to 10 (extremely stressed)",
    )
    physical_stress = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a value from 1 (no stress) to 10 (extremely stressed)",
    )
    date_added = models.DateTimeField(auto_now_add=True)

