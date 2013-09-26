#from django.db import models
#import datetime
#
#class Client(models.Model):
#    name    = models.CharField(max_length=255, db_index=True)
#
#    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
#
#class CustomerSource(models.Model):
#    name    = models.CharField(max_length=255, db_index=True)
#    url     = models.TextField(blank=True, null=True)
#
#    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
#
#class PhoneNumber(models.Model):
#    number          = models.CharField(max_length=255, blank=True, null=True)
#    type            = models.CharField(max_length=10, blank=True, null=True)
#
#    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
#
#class Customer(models.Model):
#    full_name       = models.CharField(max_length=255, blank=True, null=True)
#    first_name      = models.CharField(max_length=255, blank=True, null=True)
#    last_name       = models.CharField(max_length=255, blank=True, null=True)
#    middle_name     = models.CharField(max_length=255, blank=True, null=True)
#    dob             = models.DateField(blank=True, null=True)
#    email           = models.CharField(max_length=255, blank=True, null=True)
#    phone           = models.ManyToManyField(PhoneNumber, blank=True, null=True)
#    source          = models.ForeignKey(CustomerSource, blank=True, null=True)
#    description     = models.TextField(blank=True, null=True)
#
#    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
