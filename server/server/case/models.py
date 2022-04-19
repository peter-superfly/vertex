import json
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class Court(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

class CaseClass(models.TextChoices):
    Civil = 'Civil', _('Civil')
    Criminal = 'Criminal', _('Criminal')

class CaseAction(models.TextChoices):
    Revision = 'Revision', _('Revision')
    Judgment = 'Judgment', _('Judgment')
    Ruling = 'Ruling', _('Ruling')

class Case(models.Model):
    kenyalaw_id = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    court_name = models.CharField(max_length=200)
    case_name = models.CharField(max_length=200, blank=True, null=True)
    case_number = models.CharField(max_length=100)
    case_class = models.CharField(max_length=10, choices=CaseClass.choices)
    case_action = models.CharField(max_length=10, choices=CaseAction.choices)
    citation = models.CharField(max_length=200)
    parties = models.CharField(max_length=200, blank=True, null=True)
    file_id = models.CharField(max_length=200)
    delivery_date = models.DateField()
    updated_at = models.DateTimeField(default=timezone.now)
    tags = ArrayField(models.CharField(max_length=50, blank=True))
    judges = ArrayField(models.CharField(max_length=50, blank=True, null=True))

class PersonType(models.TextChoices):
    JUDGE = 'JUDGE', _('Judge')

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    person_type = models.CharField(max_length=20, choices=PersonType.choices)

    def __str__(self):
        
        return json.dumps({
            "id" : str(self.id),
            "name" : self.name
        })