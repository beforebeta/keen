import logging
import re
from datetime import datetime

from django.conf import settings
from django.db import DatabaseError, transaction
from django.utils.timezone import now
from django import forms
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.localflavor.us.forms import USZipCodeField

from main.models import Visitor, Customer, PhoneNumber, CustomerSource
from main.vendors.mchimp import Mailchimp


logger = logging.getLogger(__name__)


NAME_PATTERN = re.compile(r'^\s*(\S+)(?:\s+(.+))?\s*$')

class SignupForm(forms.Form):
    name = forms.RegexField(NAME_PATTERN, widget=forms.TextInput(
        attrs={'id': 'name', 'placeholder': 'Name *', 'required': True}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'id': 'email', 'type': 'email', 'placeholder': 'Email *', 'required': True}))
    dob = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'id': 'dob', 'placeholder': 'Birthday'}))
    phone = forms.CharField(max_length=255, required=False, widget=forms.TextInput(
        attrs={'id': 'phone', 'type': 'phone', 'placeholder': 'Phone'}))
    zip = USZipCodeField(min_length=5, max_length=10, widget=forms.TextInput(
        attrs={'id': 'zip', 'placeholder': 'Zip Code *', 'required': True}))

    def clean(self):
        super(SignupForm, self).clean()

        if self.data.get('dob') == 'Birthday':
            self.cleaned_data['dob'] = ''
            if 'dob' in self._errors:
                del self._errors['dob']

        if self.data.get('phone') == 'Phone':
            self.cleaned_data['phone'] = ''
            if 'phone' in self._errors:
                del self._errors['phone']

        return self.cleaned_data


@ensure_csrf_cookie
@transaction.commit_on_success
def mdo_signup(request):
    mailchimp_id = request.REQUEST.get('list_id')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            customer = Customer()
            customer.full_name = form.cleaned_data['name'].strip()
            customer.first_name, customer.last_name = NAME_PATTERN.match(
                customer.full_name).groups()
            customer.email = form.cleaned_data['email']
            customer.dob = form.cleaned_data['dob'] if form.cleaned_data['dob'] else None
            customer.zip = form.cleaned_data['zip']

            # FIXME: client/source should not be hadrcoded!!!
            client_name = 'mdo'
            source_name = 'signup'
            try:
                customer.source = CustomerSource.objects.get(
                    name=source_name, client__name=client_name)
            except CustomerSource.DoesNotExist:
                logger.error('Customer source {}:{} cannot be found'.format(
                    client_name, source_name))

            if 'visitor' in request.session:
                try:
                    customer.visitor = Visitor.objects.get(uuid=request.session['visitor'])
                except Visitor.DoesNotExist:
                    logger.warn('Session with non-existent visitor UUID')
            else:
                logging.warn('Session without visitor UUID')

            phone_number = form.cleaned_data['phone']

            try:
                logger.debug('Customer signup: %r %r %r %r',
                             customer.full_name,
                             customer.email,
                             customer.dob,
                             customer.zip,
                             )
                customer.save()
                if phone_number:
                    phone = PhoneNumber(number=phone_number, type='Default')
                    phone.save()
                    customer.phone.add(phone)
            except DatabaseError:
                transaction.rollback()
                logger.exception('Failed to save new customer')
            else:
                Mailchimp().subscribe(
                    mailchimp_id or settings.MDO_MAILCHIMP_LIST_ID,
                    customer)
                return render(request, 'clients/mdo/signup_thanks.html')
        else:
            logger.debug('Signup form validation error: %s\n%r', form.errors, form.data)
    else:
        form = SignupForm()

    return render(request, 'clients/mdo/mdo_signup.html', {
        'form': form,
        'list_id': mailchimp_id,
    })
