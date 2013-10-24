import logging

from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from main.models import Customer
from main.vendors.mchimp import Mailchimp
from django.conf import settings
from django.contrib.localflavor.us.forms import USZipCodeField


logger = logging.getLogger(__name__)


def index(request):
    context = {}
    return render_to_response('index.html', context)


class SignupForm(forms.Form):
    name    = forms.CharField(max_length=255)
    email   = forms.EmailField()
    dob     = forms.DateField()
    phone   = forms.CharField(max_length=255)
    zip     = USZipCodeField(min_length=5, max_length=10)


@ensure_csrf_cookie
def mdo_signup(request):
    context = {}

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            kw = dict(dob=form.cleaned_data['dob'])
            for name in ('name', 'email', 'phone', 'zip'):
                kw[name] = form.cleaned_data[name].strip()
            customer = Customer.objects.add_new_signup("mdo","signup", **kw)
            if customer:
                Mailchimp().subscribe(settings.MDO_MAILCHIMP_LIST_ID, customer)
            else:
                logger.error('Failed to add customer: %r', kw)
            return render_to_response('clients/mdo/signup_thanks.html',
                                      context,
                                      context_instance=RequestContext(request))
        else:
            logger.error('Invalid signup form submitted: %s', form.errors)
            print "invalid form", form.errors
            print "#---"
            for field in form:
                print field
            print "#---"
    else:
        form = SignupForm()

    context["form"] = form
    return render_to_response('clients/mdo/mdo_signup.html',
                              context,
                              context_instance=RequestContext(request))
