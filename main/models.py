from django.db import models
import datetime
from main import print_stack_trace


class Client(models.Model):
    unique_id       = models.CharField(max_length=255, db_index=True)
    name            = models.CharField(max_length=255, db_index=True)

    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

class CustomerSource(models.Model):
    client  = models.ForeignKey(Client, blank=True, null=True)
    name    = models.CharField(max_length=255, db_index=True)
    url     = models.TextField(blank=True, null=True)

    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def client_name(self):
        return self.client.name

class PhoneNumber(models.Model):
    number          = models.CharField(max_length=255, blank=True, null=True)
    type            = models.CharField(max_length=10, blank=True, null=True)

    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

class CustomerManager(models.Manager):

    def add_new_signup(self, client_name, source_name, name, email, dob, phone):
        try:
            first_name = ""
            last_name = ""
            middle_name = ""
            date_of_birth=None
            try:
                if " " in name:
                    split = name.split(" ")
                    first_name = split[0]
                    last_name = split[-1]
                    if len(split) > 2:
                        middle_name = " ".join(split[1:-1])
                else:
                    first_name=name
                #date_of_birth = datetime.datetime.strptime(dob, '%m/%d/%Y')
                if dob:
                    date_of_birth = dob
            except:
                print_stack_trace()
            new_customer = self.model(full_name=name,
                       first_name=first_name,
                       last_name=last_name,
                       middle_name=middle_name,
                       dob=date_of_birth,
                       email=email)
            number = PhoneNumber(number=phone, type="Default")
            number.save()

            client = None
            try:
                client = Client.objects.get(unique_id = client_name)
            except:
                client = Client(unique_id = client_name, name= client_name)
                client.save()

            source = None
            try:
                source = CustomerSource.objects.get(client=client, name=source_name)
            except:
                source = CustomerSource(client=client, name=source_name)
                source.save()

            new_customer.source = source

            new_customer.save()
            new_customer.phone.add(number)
            new_customer.save()
            return new_customer
        except:
            print_stack_trace()
            return None


class Customer(models.Model):
    full_name       = models.CharField(max_length=255, blank=True, null=True)
    first_name      = models.CharField(max_length=255, blank=True, null=True)
    last_name       = models.CharField(max_length=255, blank=True, null=True)
    middle_name     = models.CharField(max_length=255, blank=True, null=True)
    dob             = models.DateField(blank=True, null=True)
    email           = models.CharField(max_length=255, blank=True, null=True)
    phone           = models.ManyToManyField(PhoneNumber, blank=True, null=True)
    source          = models.ForeignKey(CustomerSource, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    objects         = CustomerManager()

    date_added      = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified   = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def source_client_name(self):
        return self.source.client.name

    def get_phone_number(self):
        try:
            if self.phone.all().count()>0:
                return self.phone.all()[0].number
        except:
            return "000-000-0000"