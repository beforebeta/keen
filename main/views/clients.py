from django.shortcuts import render

from main.views.utils import expect_visitor


@expect_visitor
def handlebar_redeem(request, promo_code=None):
    context = {
        "promo_img"             : "",
        "promo_title"           : "",
        "promo_restriction"     : "",
        "promo_code"            : promo_code if promo_code else "",

    }
    if not promo_code or promo_code[0].lower() == 'a':
        context["promo_img"] = "cake1.png"
        context["promo_title"] = "Flat $5/cup"
        context["promo_restriction"] = "Offer valid till Friday 10/4/2013"
    else:
        context["promo_img"] = "cake2.png"
        context["promo_title"] = "30% OFF"
        context["promo_restriction"] = "Offer valid till Sunday 10/6/2013"
    return render(request, 'clients/handlebar/redeem.html', context)
