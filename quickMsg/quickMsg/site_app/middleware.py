from .models import *
from django.contrib.auth import logout
from django.shortcuts import redirect,render


def handleBannedAccount(get_response):
    # One-time configuration and initialization.

    def middleware(request):

        response = get_response(request)

        if request.user.is_authenticated : 
            if request.user.isBanned : 
                logout(request)
                return redirect("homepage")
                

        return response

    return middleware