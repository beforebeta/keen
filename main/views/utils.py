from functools import wraps

from django.conf import settings

from main.models import Visitor


VISITOR_COOKIE_NAME = getattr(settings, 'VISITOR_COOKIE_NAME', 'keen_visitor')
VISITOR_COOKIE_LIFETIME = int(getattr(settings, 'VISITOR_COOKIE_LIFETIME', 365))


def expect_visitor(view_callable):
    """View decorator that adds visitor property to request
    """
    # Convert days to seconds
    max_age = VISITOR_COOKIE_LIFETIME * 86400

    @wraps(view_callable)
    def view_wrapper(request, *args, **kw):
        key = request.COOKIES.get(VISITOR_COOKIE_NAME)
        request.visitor = Visitor.objects.get_visitor(
            key, request.method=='GET')
        response = view_callable(request, *args, **kw)
        response.set_cookie(VISITOR_COOKIE_NAME, request.visitor.key, max_age=max_age)
        return response

    return view_wrapper
