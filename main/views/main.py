from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie


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
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            dob = form.cleaned_data["dob"]
            phone = form.cleaned_data["phone"]
            print name, email, dob, phone
            return render_to_response('clients/mdo/signup_thanks.html',
                                      context,
                                      context_instance=RequestContext(request))
        else:
            for field in form:
                for error in field.errors:
                    print error
    else:
        form = SignupForm()

    context["form"] = form
    return render_to_response('clients/mdo/mdo_signup.html',
                              context,
                              context_instance=RequestContext(request))
