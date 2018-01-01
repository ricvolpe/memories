from django.db import models
from datetime import date
from django.contrib.postgres.fields import ArrayField, JSONField
from django.forms.models import ValidationError

class Note(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=36)
    text = models.CharField(max_length=100000)
    title = models.CharField(max_length=255)

class Memory(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    memory = models.CharField(max_length=100000)
