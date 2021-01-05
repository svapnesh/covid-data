from django.urls import path

from .views import SignUpAPIView, LoginAPIView, user_dashboard, \
    logout_api, send_report_api

urlpatterns = [
    path('usermgmt/signup/', SignUpAPIView.as_view(), name='signup_api'),
    path('usermgmt/login/', LoginAPIView.as_view(), name='login_api'),
    path('usermgmt/dashboard/', user_dashboard, name='dashboard_api'),
    path('usermgmt/logout/', logout_api, name='logout_api'),
    path('usermgmt/send_report_email/', send_report_api, name="send_report_api"),
]
