from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta


def two_weeks_from_now():
    return timezone.now().date() + timedelta(days=14)


class TODOList(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateField(default=two_weeks_from_now)

    def __str__(self):
        return f"Task '{self.title}'"

    def days_left(self):
        return (self.expiration_date - timezone.now().date()).days

    def get_absolute_url(self):
        return reverse("task-view", kwargs={"pk": self.pk})

    def clean(self):
        exp_date = self.expiration_date
        if exp_date < datetime.now().date():
            raise ValidationError({"expiration_date": "Expiration date must be in the future"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


