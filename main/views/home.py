from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from main.models import Customer
from main.vendors.mchimp import Mailchimp
from django.conf import settings

def index(request):
    context = {}
    return render_to_response('index.html', context)

class SignupForm(forms.Form):
    name    = forms.CharField(max_length=255)
    email   = forms.EmailField()
    dob     = forms.DateField()
    phone   = forms.CharField(max_length=255)

@ensure_csrf_cookie
def mdo_signup(request):
    context = {}

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if not form.is_valid():
            print "invalid form", form.errors
        print "#---"
        for field in form:
            print field
        print "#---"
        name=""
        email=""
        dob=""
        phone=""
        try:
            name = form.cleaned_data["name"].strip()
        except: pass
        try:
            email = form.cleaned_data["email"].strip()
        except: pass
        try:
            dob = form.cleaned_data["dob"]
        except: pass
        try:
            phone = form.cleaned_data["phone"].strip()
        except: pass
        if phone == "Phone":
            phone = ""
        if name == "Name*":
            name= ""
        customer = Customer.objects.add_new_signup("mdo","signup",name,email,dob,phone)
        if customer:
            Mailchimp().subscribe(settings.MDO_MAILCHIMP_LIST_ID, customer)
        return render_to_response('clients/mdo/signup_thanks.html',
                                  context,
                                  context_instance=RequestContext(request))
    else:
        form = SignupForm()

    context["form"] = form
    return render_to_response('clients/mdo/mdo_signup.html',
                              context,
                              context_instance=RequestContext(request))
