import uuid

from django.db import models


class UserContainer(models.Model):
    email = models.EmailField(max_length=100, null=True)
    name_container = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Content(models.Model):
    container = models.ForeignKey(UserContainer, on_delete=models.PROTECT)
    name_of_blob = models.CharField(max_length=43)
    unique_link_to_blob = models.UUIDField(default=uuid.uuid4, unique=True)
