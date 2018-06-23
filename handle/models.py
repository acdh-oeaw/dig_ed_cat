from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . utils import *


class Pid(models.Model):
    handle = models.CharField(max_length=250, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, related_name="get_pid"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.handle:
            super(Pid, self).save(*args, **kwargs)
        elif self.content_object:
            try:
                parsed_data = "{}{}".format(
                    handle_app_base_url, self.content_object.get_absolute_url(),
                )
            except AttributeError:
                parsed_date = None
            if parsed_data:
                fetched_handle = create_handle(
                    handle_url,
                    handle_user,
                    handle_pw,
                    parsed_data
                )
                if fetched_handle:
                    self.handle = fetched_handle['epic-pid']
                else:
                    self.handle = 'something went wrong'
            super(Pid, self).save(*args, **kwargs)
        else:
            super(Pid, self).save(*args, **kwargs)

    def __str__(self):
        if self.handle:
            return "{}/{}".format(handle_resolver, self.handle)
        else:
            return "{}".format(self.id)
