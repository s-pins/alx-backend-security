from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='anon', block=True)
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse("You are already logged in.")
    return HttpResponse("This is the login page.")

@ratelimit(key='ip', rate='auth', block=True)
def protected_view(request):
    return HttpResponse("This is a protected view for authenticated users.")