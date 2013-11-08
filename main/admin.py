from django.contrib import admin
from main.models import Client, CustomerSource, PhoneNumber, Customer, Visitor


class CustomerAdmin(admin.ModelAdmin):
    ordering = ['-date_added']
    list_display = ('full_name', 'dob','email','source_client_name')
    search_fields = ['full_name',"dob", "email", "phone__number"]


class ClientAdmin(admin.ModelAdmin):
    ordering = ['-date_added']
    list_display = ('unique_id', 'name')


class CustomerSourceAdmin(admin.ModelAdmin):
    ordering = ['-date_added']
    list_display = ('client_name', 'name', "url")


class PhoneNumberAdmin(admin.ModelAdmin):
    ordering = ['-date_added']
    list_display = ('number', 'type')


class VisitorAdmin(admin.ModelAdmin):
    ordering = ['-last_visit', '-first_visit']
    list_display = ('customer', 'first_visit', 'last_visit', 'visits',
                    'source', 'medium', 'campaign', 'keywords')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(CustomerSource, CustomerSourceAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Visitor, VisitorAdmin)
