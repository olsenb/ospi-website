from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(User)
    ip = models.IPAddressField()
    port = models.IntegerField(default=8080)

    def __unicode__(self):
        return u"%s" % self.user
