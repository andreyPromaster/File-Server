import uuid

from django.db import models


class UserContainer(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    container = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Content(models.Model):
    name_of_blob = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    unique_link_to_blob = models.UUIDField(default=uuid.uuid4, unique=True)
