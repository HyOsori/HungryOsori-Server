from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, BasePermission
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes

from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription, PushToken
from osoriCrawlerAPI.serializers import UserProfileSerializer, CrawlerSerializer, SubscriptionSerializer, PushTokenSerializer
from crawlerAPI.keys import HOST_IP, PORT_NUMBER

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone


import re, json, random


# Authentication. ----------------
# 1. check id and password
# 2. method for email auth (When user sign up by email)
# Default Permission ----> IsAuthenticated
# if you want to change default permission, go to setting.py and find the option


class Auth:

    # find user and check password
    @staticmethod
    def authenticate(email, sign_up_type, password):
        try:
            user = UserProfile.objects.get(email=email, sign_up_type=sign_up_type)
        except ObjectDoesNotExist:
            return -1
        chk_password = check_password(password=password, encoded=user.password)
        if chk_password is False:
            return -2
        return user

    # email authentication
    @staticmethod
    def email_auth(self, auth):
        try:
            user = UserProfile.objects.get(is_auth=auth)
        except ObjectDoesNotExist:
            return HttpResponse("Invalid user or already authenticated")
        user.is_auth = 'True'
        user.save()
        return HttpResponse("Authenticated")


# class for making error response object
class ErrorResponse:
    @staticmethod
    def error_response(error_code, message):
        data = {"message": message, "ErrorCode": error_code}
        return Response(data)


class PasswordClassPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated()


# for password change or find
class Password(APIView):
    # make temp password. To use find password
    permission_classes = (PasswordClassPermission, )

    @staticmethod
    def make_temp_password():
        strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q',
                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        password = ''
        for i in range(0, 8):
            password = password + strings[random.randrange(0, 35)]
        return password

    # find password. making temp password and send it to email.
    def get(self, request):
        try:
            email = request.GET['email']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-100, 'Please give email')

        temp_password = Password().make_temp_password()

        try:
            user = UserProfile.objects.get(email=email, sign_up_type='email')
        except ObjectDoesNotExist:
            return ErrorResponse.error_response(-101, "Invalid user")

        user.password = make_password(password=temp_password, salt=None, hasher='default')
        user.save()

        send_mail(
            'temp password',
            temp_password + ' login and modify your password.',
            'bees1114@naver.com',
            [email],
        )
        return_data = {'message': 'Temp password sent', 'ErrorCode': 0}
        return Response(return_data)

    # password change
    def put(self, request):

        # get data from request.
        try:
            email = request.data['email']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-101, "No email")
        try:
            password = request.data['password']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-102, "No current password")
        try:
            new_password = request.data['new_password']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-103, "No new_password")

        try:
            user = UserProfile.objects.get(email=email, sign_up_type='email')
        except ObjectDoesNotExist:
            return ErrorResponse.error_response(-200, "Invalid user")
        chk_password = check_password(password=password, encoded=user.password)
        if chk_password is False:
            return ErrorResponse.error_response(-300, "Not correct current password")
        user.password = make_password(password=new_password, salt=None, hasher='default')
        user.save()
        return_data = {"message": "success", "ErrorCode": 0}
        return Response(return_data)


# Sign up and Sign in class for social user
class SocialSign(APIView):
    permission_classes = ()

    # some user request login, if it is first login, signup the user. if not, just login
    def post(self, request, format=None):
        data = request.data
        # If user already signup? or not
        try:
            user = UserProfile.objects.get(email=data['email'], sign_up_type=data['sign_up_type'])
        except ObjectDoesNotExist:
            user = None

        # If user visit first time, do sign up
        if user is None:
            if re.match(' /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i',
                        data['email']) is not None:
                return ErrorResponse.error_response(-200, 'Invalid email address during social sign up')

            # checking email address is duplicated or not
            exist = UserProfile.objects.filter(email=data['email'], sign_up_type=data['sign_up_type'])
            if exist.count() != 0:
                return ErrorResponse.error_response(-100, 'Already exist user_id in social sign up')

            user = dict()
            user['email'] = data['email']
            user['name'] = data['name']
            user['password'] = 'Null'
            user['is_auth'] = 'True'
            user['sign_up_type'] = data['sign_up_type']
            user_serializer = UserProfileSerializer(data=user)

            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return ErrorResponse.error_response(-300, 'Error in saving user date during sign up')

        # if user is already sign up, login the user
        else:
            try:
                email = data['email']
            except MultiValueDictKeyError:
                return_data = {'message': 'No email', 'ErrorCode': -201}
                return Response(return_data)
            try:
                push_token = data['push_token']
            except MultiValueDictKeyError:
                return_data = {'message': 'No push token', 'ErrorCode': -400}
                return Response(return_data)
            try:
                sign_up_type = data['sign_up_type']
            except MultiValueDictKeyError:
                return_data = {'message': 'No sign up type', 'ErrorCode': -500}
                return Response(return_data)
            try:
                UserProfile.objects.get(email=email)
            except ObjectDoesNotExist:
                return_data = {'message': 'Invalid user in login', 'ErrorCode': -100}
                return Response(return_data)

        user = UserProfile.objects.get(email=data['email'], sign_up_type=sign_up_type)

        user_token = dict()
        user_token['owner'] = user
        user_token['push_token'] = push_token

        # user: push token added
        push_token_serializer = PushTokenSerializer(data=user_token)
        # login -> create app token
        token, created = Token.objects.get_or_create(user=user)

        if push_token_serializer.is_valid():
            push_token_serializer.save()
        data = {'token': token.key, 'email': email, 'message': "Login success", 'ErrorCode': 0}
        return Response(data)


# sign up by using email (just in our app)
class SignUp(APIView):
    permission_classes = ()

    # auth key for email authentication.
    def make_auth_key(self):
        auth_key = ''
        strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q', 'r', 's',
                   't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for i in range(0, 15):
            auth_key = auth_key + strings[random.randrange(0, 35)]
        return auth_key

    def post(self, request, format=None):
        data = request.data
        # sign up by email
        # checking email address in requested data are correct email format or not
        if re.match(' /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i',
                    data['email']) is not None:
            return ErrorResponse.error_response(-200, 'Invalid email address')

        # checking email address is duplicated or not (in same sign up type)
        exist = UserProfile.objects.filter(email=data['email'], sign_up_type=data['sign_up_type'])
        if exist.count() != 0:
            return ErrorResponse.error_response(-100, 'Already exist user_id')

        # password hashed
        password = make_password(password=data['password'], salt=None, hasher='default')

        # make email authenticate key
        is_auth = self.make_auth_key()

        # send confirm email
        url = 'http://' + HOST_IP + ':' + PORT_NUMBER + '/api/email_auth/'+is_auth+'/'
        user = dict()
        user['email'] = data['email']
        user['name'] = data['name']
        user['password'] = password
        user['is_auth'] = is_auth
        user['sign_up_type'] = 'email'
        user_serializer = UserProfileSerializer(data=user)

        if user_serializer.is_valid():
            user_serializer.save()
            send_mail(
                'Authentication mail.',
                url+' authentication by click this urls.',
                'beespjh@gmail.com',
                [data['email']],
                fail_silently=False,
            )
            return_data = {'message': 'Success', 'ErrorCode': 0}
            return Response(return_data)
        return ErrorResponse().error_response(-1, 'Error at the end')


# sign in class
class SignIn(APIView):
    permission_classes = ()

    def get_object(self, email, sign_up_type):
        try:
            return UserProfile.objects.get(email=email, sign_up_type=sign_up_type)
        except UserProfile.DoesNotExist:
            return False

    def post(self, request, format=None):
        data = request.data
        try:
            email = data['email']
        except MultiValueDictKeyError:
            return_data = {'message': 'No email', 'ErrorCode': -100}
            return Response(return_data)
        try:
            password = data['password']
        except MultiValueDictKeyError:
            return_data = {'message': 'No password', 'ErrorCode': -200}
            return Response(return_data)
        try:
            push_token = data['push_token']
        except MultiValueDictKeyError:
            return_data = {'message': 'No push token', 'ErrorCode': -300}
            return Response(return_data)
        try:
            UserProfile.objects.get(email=email, sign_up_type='email')
        except ObjectDoesNotExist:
            return_data = {'message': 'Invalid user', 'ErrorCode': -101}
            return Response(return_data)
        if UserProfile.objects.get(email=email).is_email_authenticated() is not True:
            return_data = {'message': 'Need authentication', 'ErrorCode': -102}
            return Response(return_data)

        user = Auth.authenticate(email=email, sign_up_type='email', password=password)
        if user is -1:
            return_data = {'message': 'Invalid user', 'ErrorCode': -103}
            if push_token == '-1':
                return redirect('/', return_message=return_data['message'])
            return Response(return_data)
        elif user is -2:
            return_data = {'message': 'Invalid password', 'ErrorCode': -201}
            if push_token == '-1':
                return redirect('/', return_message=return_data['message'])
            return Response(return_data)
        else:
            user_token = dict()
            user_token['owner'] = user
            user_token['push_token'] = push_token
            pushTokenSerializer = PushTokenSerializer(data=user_token)

            token, created = Token.objects.get_or_create(user=user)
            if pushTokenSerializer.is_valid():
                pushTokenSerializer.save()
            return_data = {'token': token.key, 'email': email, 'message': "Login success", 'ErrorCode': 0}
            if push_token == '-1':
                return redirect('/', return_message=return_data['message'])
            return Response(return_data)

        return Response(return_data)


# class for log out
class Logout(APIView):

    def post(self, request):
        try:
            user = request.user
        except exceptions:
            return ErrorResponse.error_response(-400, 'No User')
        try:
            token = Token.objects.get(user=user)
        except exceptions:
            return ErrorResponse.error_response(-300, 'No Tokens')

        token.delete()
        try:
            push_token = PushToken.objects.get(owner=user)
        except ObjectDoesNotExist:
            return ErrorResponse.error_response(-200, 'No Pushtoken')
        return_data = {'ErrorCode': 0, 'message': 'Logout success'}
        return Response(return_data)


class UserDetail(APIView):

    def get_object(self, email):
        try:
            return UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return False

    def get(self, request):
        user = request.user
        if user is None:
            return ErrorResponse.error_response(-100, "Invalid user")
        return_user_data = {'email': user.email, 'name': user.name}
        return_data = {'ErrorCode': 0, 'message': 'successfully return user data', 'user_data': return_user_data}
        return Response(return_data)

    def put(self, request, format=None):
        user = request.user
        if user is None:
            return ErrorResponse.error_response(-100, "Invalid user")
        data = request.data
        data['password'] = make_password(password=data['password'], salt=None, hasher='default')
        user_serializer = UserProfileSerializer(user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        current_user = request.user
        try:
            user = UserProfile.objects.get(email=current_user.email, sign_up_type=current_user.sign_up_type)
        except ObjectDoesNotExist:
            return ErrorResponse.error_response(-100, "Invalid user")
        user.delete()
        return_data = {'ErrorCode': 0, 'message': 'successfully deleted'}
        return Response(return_data)


class CrawlerList(APIView):
    def get(self, request, format=None):
        crawlers = Crawler.objects.all()
        if crawlers != None:
            crawlerSerializer = CrawlerSerializer(crawlers, many=True)
            return_data = {"message": "Success", "crawlers": crawlerSerializer.data, 'ErrorCode': 0}
            return Response(return_data)
        return ErrorResponse().error_response(-100, 'No crawler list')

    def post(self, request, format=None):
        crawlerSerializer = CrawlerSerializer(data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrawlerDetail(APIView):
    def get_object(self, name):
        try:
            return Crawler.objects.get(crawler_id=name)
        except Crawler.DoesNotExist:
            return False

    def get(self, request, format=None):
        name = request.GET['title']
        crawler = self.get_object(name)
        if crawler != False:
            crawlerSerializer = CrawlerSerializer(crawler)
            return Response(crawlerSerializer.data)
        return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name, format=None):
        crawler = self.get_object(name)
        if crawler == False:
            return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawlerSerializer = CrawlerSerializer(crawler, data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        crawler_id = request.GET['crawler_id']
        crawler = self.get_object(crawler_id)
        if crawler is False:
            Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawler.delete()
        return Response(crawler.title+" deleted")


class SubscriptionList(APIView):
    def get(self, request, format=None):
        subscription = Subscription.objects.all()
        subscriptionSerializer = SubscriptionSerializer(subscription, many=True)
        return Response(subscriptionSerializer.data)


class SubscriptionDetail(APIView):
    def get(self, request, format = None):
        subscriber = request.user
        subscription = Subscription.objects.filter(subscriber=subscriber)
        subscription_serializer = SubscriptionSerializer(subscription, many=True)
        return_data = {"message": "Successfully return subscriptions",
                       "subscriptions": subscription_serializer.data, "ErrorCode": 0}
        return Response(return_data)

    def post(self, request, format = None):
        try:
            crawler_id = request.data['crawler_id']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-101, "No crawler id data in http request")
        try:
            crawler = Crawler.objects.get(crawler_id=crawler_id)
        except ObjectDoesNotExist:
            return ErrorResponse.error_response(-200, "Invalid crawler")
        subscriber = request.user
        Subscription.objects.create(subscriber=subscriber, crawler=crawler, latest_pushtime=timezone.now())
        return_data = {"message": 'success', 'ErrorCode': 0}
        return Response(return_data)

    def delete(self, request, format=None):
        try:
            crawler_id = request.data['crawler_id']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-101, "No crawler data in request")
        subscriber = request.user
        try:
            subscription = Subscription.objects.get(subscriber=subscriber, crawler_id=crawler_id)
        except ObjectDoesNotExist:
            return ErrorResponse.error_response(-200, "Invalid subscriptions")
        subscription.delete()
        return_data = {"message": "success", "ErrorCode": 0}
        return Response(return_data)


class PushTokenList(APIView):
    def get(self, request, format=None):
        token = PushToken.objects.all()
        tokenSerializer=PushTokenSerializer(token, many=True)
        return Response(tokenSerializer.data)


class PushTokenDetail(APIView):
    def post(self, request, format=None):
        owner = request.user
        try:
            push_token = request.data['push_token']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response('-100', 'no push_token data in request')
        PushToken.objects.create(owner=owner, push_token=push_token)
        return_data = {'ErrorCode': 0, 'message': 'success'}
        return Response(return_data)

    def get(self, request, format=None):
        owner = request.user
        push_token = PushToken.objects.get(owner=owner)
        if push_token is not None:
            return_data = {'ErrorCode': 0,
                           'data': {'owner': owner.__str__(), 'push_token': push_token.push_token},
                           'message': 'success'}
            return Response(return_data)
        return ErrorResponse.error_response(-100, 'Error')

    def delete(self, request, format=None):
        owner = request.user
        push_token = PushToken.objects.get(owner=owner)
        if push_token is None:
            return ErrorResponse.error_response(-100, 'push token is none')
        push_token.delete()
        return_data = {'message': 'push token deleted', 'ErrorCode': 0}
        return Response(return_data)


class SubscriberPushToken(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        try:
            crawler_id = request.GET['crawler_id']
        except MultiValueDictKeyError:
            return ErrorResponse.error_response(-100, 'Invalid crawler_id')
        subscription_list = Subscription.objects.filter(crawler_id=crawler_id)
        total = []
        for subscription in subscription_list:
            subscriber = subscription.subscriber
            push_token_list = PushToken.objects.filter(owner=subscriber)
            for push_token in push_token_list:
                arr = {'email': push_token.owner.email, 'push_token': push_token.push_token}
                total.append(arr)

        return_data = {'ErrorCode': 0, 'data': total, 'message': 'successfully return list'}
        return Response(return_data)
