from django.utils import timezone
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as f
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

class ValidateSwimRecord:
    # validates that the stroke is one of 'front crawl', 'butterfly', 'breast', 'back', or 'freestyle'
    @staticmethod
    def validate_strokes(stroke):
        if stroke not in ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']:
            raise ValidationError("%(stroke)s is not a valid stroke", params={"stroke":stroke})

    @staticmethod
    def validate_record_data(date):
        if date > timezone.now():
            raise ValidationError("Can't set record in the future.")
        return date

    @staticmethod
    def validate_broken_record_data(date):
        if date < timezone.now():
            raise ValidationError("Can't break record before record was set.")
        return date
    

class SwimRecord(models.Model):



    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    relay = models.BooleanField(default=False)
    stroke = models.CharField(max_length=255, validators=[ValidateSwimRecord.validate_strokes])
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators=[ValidateSwimRecord.validate_record_data])
    record_broken_date = models.DateTimeField(validators=[ValidateSwimRecord.validate_broken_record_data])
