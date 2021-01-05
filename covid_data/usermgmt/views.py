from django.shortcuts import render
from django.views import View


class HomePageView(View):
    """ Home Page View """
    def get(self, request):
        return render(request, 'index.html')


class RegisterPageView(View):
    """ Signup Page View """
    def get(self, request):
        return render(request, 'signup.html')


class LoginPageView(View):
    """ Login Page View """
    def get(self, request):
        return render(request, 'login.html')


def dashboard_page_view(request):
    """ Dashboard page view """
    return render(request, 'dashboard.html')