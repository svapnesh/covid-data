from django.urls import path
from .views import HomePageView, RegisterPageView, LoginPageView, \
    dashboard_page_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('signup/', RegisterPageView.as_view(), name='register_page'),
    path('login/', LoginPageView.as_view(), name='login_page'),
    path('dashboard/', dashboard_page_view, name='dashboard_page'),
]
