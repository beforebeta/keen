import logging
from datetime import timedelta
from uuid import uuid4

from django.db import models, DatabaseError
from django.utils.timezone import now


logger = logging.getLogger(__name__)


class Client(models.Model):
    unique_id       = models.CharField(max_length=255, db_index=True)
    name            = models.CharField(max_length=255, db_index=True)

    date_added      = models.DateTimeField(default=now, auto_now_add=True)
    last_modified   = models.DateTimeField(default=now, auto_now=True, auto_now_add=True)


class Visitor(models.Model):

    first_visit = models.DateTimeField(default=now)
    visits = models.PositiveSmallIntegerField(default=0)
    last_visit = models.DateTimeField()
    source = models.CharField(max_length=255)
    medium = models.CharField(max_length=255)
    campaign = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)


class CustomerSource(models.Model):
    client  = models.ForeignKey(Client, blank=True, null=True)
    name    = models.CharField(max_length=255, db_index=True)
    url     = models.TextField(blank=True, null=True)

    date_added      = models.DateTimeField(default=now, auto_now_add=True)
    last_modified   = models.DateTimeField(default=now, auto_now=True, auto_now_add=True)

    def client_name(self):
        return self.client.name


class PhoneNumber(models.Model):
    number          = models.CharField(max_length=255, blank=True, null=True)
    type            = models.CharField(max_length=10, blank=True, null=True)

    date_added      = models.DateTimeField(default=now, auto_now_add=True)
    last_modified   = models.DateTimeField(default=now, auto_now=True, auto_now_add=True)


class Customer(models.Model):
    full_name       = models.CharField(max_length=255, blank=True, null=True)
    first_name      = models.CharField(max_length=255, blank=True, null=True)
    last_name       = models.CharField(max_length=255, blank=True, null=True)
    middle_name     = models.CharField(max_length=255, blank=True, null=True)
    dob             = models.DateField(blank=True, null=True)
    email           = models.CharField(max_length=255, blank=True, null=True)
    phone           = models.ManyToManyField(PhoneNumber, blank=True, null=True)
    zip             = models.CharField(max_length=10, blank=True, null=True)
    source          = models.ForeignKey(CustomerSource, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)
    visitor         = models.ForeignKey(Visitor, null=True, related_name='customer')

    date_added      = models.DateTimeField(default=now, auto_now_add=True)
    last_modified   = models.DateTimeField(default=now, auto_now=True, auto_now_add=True)

    def source_client_name(self):
        return self.source.client.name

    def get_phone_number(self):
        try:
            if self.phone.all().count()>0:
                return self.phone.all()[0].number
        except:
            return "000-000-0000"
