from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.


def homepage(request):
    # homepage view
    if request.user.is_authenticated:
        # if the user logged in, show the firstname of user
        # otherwise, show the register and login button
        is_logged_in = True
        first_name = request.user.username
        return render(request, 'homepage/homepage.html', {'is_logged_in': is_logged_in, 'first_name': first_name})
    else:
        return render(request, 'homepage/homepage.html')
