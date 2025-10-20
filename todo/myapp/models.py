from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta


class TODOList(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateField(default=timezone.now() + timedelta(days=14))

    def __str__(self):
        return f"Task '{self.title}'"

    def days_left(self):
        return (self.expiration_date - timezone.now().date()).days

    def get_absolute_url(self):
        return reverse("task-view", kwargs={"pk": self.pk})

    def clean_date(self):
        exp_date = datetime.strptime(str(self.expiration_date), "%Y-%m-%d").date()
        # so basically expiration_date above is a DATETIME object, but one below a STRING wtf
        if exp_date < datetime.now().date():
            raise ValidationError({"expiration_date": "Expiration date must be in the future"})

    def save(self, *args, **kwargs):
        self.clean_date()
        super().save(*args, **kwargs)


