import uuid
import json
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_upload_dir(instance, filename):
    ext = filename.split('.')[-1]
    new_filename =  f'{uuid.uuid4().hex}.{ext}'
    return f'avatar/{new_filename}'

class User(AbstractUser):
    user_id  =   models.CharField(
        primary_key=True, null = False, max_length = 255, unique = True, default = uuid.uuid4)
    email =   models.EmailField(
        null = False, max_length = 64, unique = True)
    username =   models.CharField(
        null = False, max_length = 32, unique = True)
    fullname =   models.CharField(
        null = False,  max_length = 32)
    mobile =   models.CharField(
        null = True,  max_length = 16, blank = True)
    email_verified  = models.BooleanField(
        null = False, default = False)
    mobile_verified  = models.BooleanField(
        null = False, default = False)
    avatar = models.ImageField(upload_to=avatar_upload_dir, null=True, blank=True)
        

    USERNAME_FIELD  =   'email'
    REQUIRED_FIELDS =   []

    def __str__(self):
        return self.email

    def is_type_admin(self):
        return self.user_type == self.ROLE_ADMIN

    def is_type_member(self):
        return self.user_type == self.ROLE_PATIENT

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def get_info(self):
        return {
            "fullname": self.fullname,
            "email": self.email,
            "user_type": self.user_type,
        }

class Invitation( models.Model):

    id = models.UUIDField(
        primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(null = False, max_length = 255)
    space_id = models.UUIDField(null = True, editable = False)
    invitor_id = models.UUIDField(null = True, editable = False)
    creation_time = models.DateTimeField(null = True, auto_now_add=True)
    accepted =  models.BooleanField(null = True, default = False)
    accepted_time = models.DateTimeField(null = True)

    def __str__(self):
        return json.dumps({
            "id" : str(self.id),
            "email" : self.email,
            "space_id" : str(self.space_id),
            "creation_time" : str(self.creation_time)
        })

class UserEmail(models.Model):
    email = models.EmailField(null = False, max_length = 64, unique = True)
    email_verified  = models.BooleanField(null = False, default = False)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)