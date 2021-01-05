import os
from collections import OrderedDict

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate

from .utils import required_field_difference, \
    extra_fields_response, missing_fields_response, JSONResponse

from .messages import Message
from .serializers import CustomUserSerializer
from usermgmt.models import CustomUser


class SignUpAPIView(APIView):
    """
       Used to signup user with email, first_name, last_name, etc.
       post request is allowed
       :param : email, first_name, last_name, country, password
       :return: JSONResponse with success/error response and message
    """
    def post(self, request):
        try:
            data = request.data
            required_fields = [
                'first_name', 'last_name', 'email',
                'password', 'country'
            ]
            optional_fields = ['csrfmiddlewaretoken']
            # convert unicode to normal string
            post_params_key = map(str, request.data.keys())
            required, not_needed = required_field_difference(required_fields,
                                                             optional_fields,
                                                             post_params_key)
            # if extra fields is provided
            if not_needed:
                return extra_fields_response(not_needed)
            # if required field not provided
            if required:
                return missing_fields_response(required)

            country = data.get('country', '').upper()
            post_data = OrderedDict()
            post_data.update(data)
            post_data['country'] = country

            # Checker for email already exists
            email_exists = CustomUser.objects.filter(email=data.get('email')).exists()
            if email_exists:
                return JSONResponse({
                    'code': 0,
                    'message': 'Email already exists',
                    'response': {}
                })

            custom_user_serializer = CustomUserSerializer(data=post_data)
            if not custom_user_serializer.is_valid():
                return JSONResponse(custom_user_serializer.errors)
            custom_user = custom_user_serializer.save()

            # Set password
            if data.get('password'):
                custom_user.set_password(data.get('password'))
            else:
                return JSONResponse({
                    'code': 0,
                    'message': 'password required',
                    'response': {}
                })
            custom_user.save()

            return JSONResponse({
                'code': 1,
                'message': Message.code(1),
                'response': {}
            })
        except Exception as e:
            print(e)
            return JSONResponse({
                'code': -1,
                'message': Message.code(3),
                'response': {}
            })


class LoginAPIView(APIView):
    """
       Used to login user.
       post request is allowed
       :param : email, password
       :return: JSONResponse with success/error response and message
    """
    def post(self, request):
        try:
            data = request.data
            required_fields = [
                'email', 'password'
            ]
            optional_fields = ['csrfmiddlewaretoken']
            # convert unicode to normal string
            post_params_key = map(str, request.data.keys())
            required, not_needed = required_field_difference(required_fields,
                                                             optional_fields,
                                                             post_params_key)
            # if extra fields is provided
            if not_needed:
                return extra_fields_response(not_needed)
            # if required field not provided
            if required:
                return missing_fields_response(required)

            email = data.get('email')
            password = data.get('password')
            authenticated_user = authenticate(email=email, password=password)
            if not authenticated_user:
                return JSONResponse({
                    'code': 0,
                    'message': 'Incorrect username or password',
                    'response': {}
                })
            custom_user = CustomUser.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=custom_user)
            return JSONResponse({
                'code': 1,
                'message': Message.code(2),
                'response': {
                    'token': token.key
                }
            })

        except Exception as e:
            print(e)
            return JSONResponse({
                'code': -1,
                'message': Message.code(3),
                'response': {}
            })


@api_view(['GET'])
def user_dashboard(request):
    """
       Used to fetch dashboard(user details) data.
       get request is allowed
       :param : user(token)
       :return: JSONResponse with success/error response and message
    """
    user = request.user
    try:
        if user.is_authenticated:
            return JSONResponse({
                'code': 1,
                'message': Message.code(7),
                'response': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'country_code': 'IN' if user.country == 'INDIA' else 'US'
                }
            })
        else:
            return JSONResponse({
                'code': 0,
                'message': 'Login required',
                'response': {}
            })
    except Exception as e:
        print(e)
        return JSONResponse({
            'code': -1,
            'message': Message.code(3),
            'response': {}
        })


@api_view(['POST'])
def logout_api(request):
    """
       Used to logout user.
       post request is allowed
       :param : user(token)
       :return: JSONResponse with success/error response and message
    """
    try:
        user = request.user
        if not user.is_authenticated:
            return JSONResponse({
                'code': 0,
                'response': {},
                'message': Message.code(9)
            })
        request.user.auth_token.delete()
        return JSONResponse({
            'code': 1,
            'response': {},
            'message': Message.code(8)
        })
    except Exception as e:
        print(e)
        return JSONResponse({
            'code': -1,
            'message': Message.code(3),
            'response': {}
        })


@api_view(['POST'])
def send_report_api(request):
    """
       Used to send report via email.
       post request is allowed
       :param : user(token)
       :return: JSONResponse with success/error response and message
    """
    try:
        user = request.user
        if not user.is_authenticated:
            return JSONResponse({
                'code': 0,
                'response': {},
                'message': Message.code(9)
            })

        import plotly.graph_objects as go
        dates = ['2020-12-31', '2020-12-21', '2020-12-11']

        fig = go.Figure(data=[
            go.Bar(name='Confirmed', x=dates, y=[20, 14, 23]),
            go.Bar(name='Deaths', x=dates, y=[12, 18, 29])
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        # fig.write_image('covid_data.jpeg')
        fig.write_html('covid_data.html', auto_open=True)

        # For sending report email
        """
        from django.core.mail import EmailMessage
        mail = EmailMessage('covid_data', 'PFA', settings.EMAIL_HOST_USER, [user.email])
        f = open(os.path.join(settings.BASE_DIR, 'covid_data.jpeg'))
        mail.attach(f.name, f.read(), f.content_type)
        mail.send()
        """

        return JSONResponse({
            'code': 1,
            'response': {},
            'message': Message.code(8)
        })
    except Exception as e:
        print(e)
        return JSONResponse({
            'code': -1,
            'message': Message.code(3),
            'response': {}
        })
