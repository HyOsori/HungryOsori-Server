from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription, PushToken
from osoriCrawlerAPI.serializers import UserProfileSerializer, CrawlerSerializer, SubscriptionSerializer, PushTokenSerializer
from crawlerAPI.keys import HOST_IP
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

import re, json, random

def main(request):
    return render(request, 'osoriCrawlerAPI/main.html', {})


class Auth():
    def authenticate(self, email, sign_up_type, password):
        try:
            user = UserProfile.objects.get(email=email, sign_up_type=sign_up_type)
        except:
            return -1
        chk_password = check_password(password=password, encoded=user.password)
        if chk_password is False:
            return -2
        return user

    def email_auth(self, request, auth):
        result = dict()
        try:
            user = UserProfile.objects.get(is_auth=auth)
        except:
            return HttpResponse("Invalid user or already authenticated")
        user.is_auth = 'True'
        user.save()
        return HttpResponse("Authenticated")

class ErrorResponse():
    def error_response(ErrorCode, message):
        data = {"message": message, "ErrorCode": ErrorCode}
        return Response(data)

class Password(APIView):
    def make_temp_password(self):
        strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q',
                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        password = ''
        for i in range(0, 8):
            password = password + strings[random.randrange(0, 35)]
        return password

    def post(self, request):
        email = request.data['email']
        temp_password = Password().make_temp_password()
        try:
            user = UserProfile.objects.get(email=email)
        except ObjectDoesNotExist:
            return ErrorResponse().error_response(-1, "Invalid user")
     
        send_mail(
            'temp password',
            temp_password + ' login and modify your password.',
            'bees1114@naver.com',
            [email],
        )
        user.password = make_password(password=temp_password, salt=None, hasher='default')
        user.save()
        data = {'message': 'Temp password sent', 'ErrorCode': 0}
        return HttpResponse(data)

    def put(self, request):
        try:
            email = request.data['email']
        except:
            return ErrorResponse().error_response(-1, "No email")
        try:
            password = request.data['password']
        except:
            return ErrorResponse().error_response(-1, "No current password")
        try:
            new_password = request.data['new_password']
        except:
            return ErrorResponse().error_response(-1, "No new_password")
        user = UserProfile.objects.get(email=email)
        chk_password = check_password(password=password, encoded=user.password)
        if chk_password is False:
            return ErrorResponse().error_response(-100, "Not correct current password")
        user.password = make_password(password=new_password, salt=None, hasher='default')
        user.save()
        return_data = {"message": "success", "ErrorCode": 0}
        return Response(return_data)

class SocialSign(APIView):
    permission_classes = ()

    def post(self, request, format=None):
        data = request.data
        try:
            user = UserProfile.objects.get(email=data['email'], sign_up_type=data['sign_up_type'])
        except ObjectDoesNotExist:
            user = None
        if user is None:
            if re.match(' /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i',
                        data['email']) is not None:
                return ErrorResponse.error_response(-200, 'Invalid email address')

            # checking email address is duplicated or not
            exist = UserProfile.objects.filter(email=data['email'], sign_up_type=data['sign_up_type'])
            if exist.count() != 0:
                return ErrorResponse.error_response(-100, 'Already exist user_id')

            user = dict()
            user['email'] = data['email']
            user['name'] = data['name']
            user['password'] = 'Null'
            user['is_auth'] = 'True'
            user['sign_up_type'] = data['sign_up_type']
            userSerializer = UserProfileSerializer(data=user)

            if userSerializer.is_valid():
                userSerializer.save()
                return_data = {'message': 'Success', 'ErrorCode': 0}
                return Response(return_data)
            else:
                return ErrorResponse().error_response(-1, 'Error at the end')
        else:
            try:
                email = data['email']
            except MultiValueDictKeyError:
                return_data = {'message': 'No email', 'ErrorCode': -1}
                return Response(return_data)
            try:
                push_token = data['push_token']
            except MultiValueDictKeyError:
                return_data = {'message': 'No push token', 'ErrorCode': -1}
                return Response(return_data)
            try:
                sign_up_type = data['sign_up_type']
            except MultiValueDictKeyError:
                return_data = {'message': 'No sign up type', 'ErrorCode': -1}
                return Response(return_data)
            try:
                UserProfile.objects.get(email=email)
            except ObjectDoesNotExist:
                return_data = {'message': 'Invalid user', 'ErrorCode': -100}
                return Response(return_data)

            user = UserProfile.objects.get(email=data['email'], sign_up_type=sign_up_type)

            user_token = dict()
            user_token['owner'] = user
            user_token['push_token'] = push_token

            pushTokenSerializer = PushTokenSerializer(data=user_token)

            token, created = Token.objects.get_or_create(user=user)
            if pushTokenSerializer.is_valid():
                pushTokenSerializer.save()
            data = {'token': token.key, 'email': email, 'message': "Login success", 'ErrorCode': 0}
            return Response(data)

        return Response(return_data)


class SignUp(APIView):
    permission_classes = ()

    def make_auth_key(self):
        auth_key = ''
        strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for i in range(0, 15):
            auth_key = auth_key + strings[random.randrange(0, 35)]
        return auth_key

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        if users.count() == 0:
            return Response('No users')
        userSerializer = UserProfileSerializer(users, many=True)
        return Response(userSerializer.data)

    def post(self, request, format=None):
        data = request.data
        # sign up Case1: by email
        if data['sign_up_type'] == 'email':
            # checking email address in requested data are correct email format or not
            if re.match(' /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i',
                        data['email']) is not None:
                return ErrorResponse.error_response(-200, 'Invalid email address')

            # checking email address is duplicated or not
            exist = UserProfile.objects.filter(email=data['email'], sign_up_type=data['sign_up_type'])
            if exist.count() != 0:
                return ErrorResponse.error_response(-100, 'Already exist user_id')

            password = make_password(password=data['password'], salt=None, hasher='default')

            # make email authenticate key
            is_auth = self.make_auth_key()

            # send confirm email
            url = 'http://' + HOST_IP + '/email_auth/'+is_auth+'/'
            user = dict()
            user['email'] = data['email']
            user['name'] = data['name']
            user['password'] = password
            user['is_auth'] = is_auth
            user['sign_up_type'] = 'email'
            userSerializer = UserProfileSerializer(data=user)

            if userSerializer.is_valid():
                userSerializer.save()
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
        # Sign up Case2 : by social / facebook, google, kakao
        else:
            # checking email address in requested data are correct email format or not
            return ErrorResponse().error_response(-1, 'Error at the class end')


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
            return_data = {'message': 'No email', 'ErrorCode': -1}
            return Response(return_data)
        try:
            password = data['password']
        except MultiValueDictKeyError:
            return_data = {'message': 'No password', 'ErrorCode': -1}
            return Response(return_data)
        try:
            push_token = data['push_token']
        except MultiValueDictKeyError:
            return_data = {'message': 'No push token', 'ErrorCode': -1}
            return Response(return_data)
        try:
            UserProfile.objects.get(email=email, sign_up_type='email')
        except ObjectDoesNotExist:
            return_data = {'message': 'Invalid user', 'ErrorCode': -100}
            return Response(return_data)
        if UserProfile.objects.get(email=email).is_email_authenticated() is not True:
            return_data = {'message': 'Need authentication', 'ErrorCode': -300}
            return Response(return_data)

        user = Auth().authenticate(email=email, sign_up_type='email', password=password)
        if user is -1:
            return_data = {'message': 'Invalid user', 'ErrorCode': -100}
            return Response(return_data)
        elif user is -2:
            return_data = {'message': 'Invalid password', 'ErrorCode': -200}
            return Response(return_data)
        else:
            user_token = dict()
            user_token['owner'] = user
            user_token['push_token'] = push_token
            pushTokenSerializer = PushTokenSerializer(data=user_token)

            token, created = Token.objects.get_or_create(user=user)
            if pushTokenSerializer.is_valid():
                pushTokenSerializer.save()
            data = {'token': token.key, 'email': email, 'message': "Login success", 'ErrorCode': 0}
            return Response(data)

        return Response(return_data)


class UserDetail(APIView):

    def get_object(self, email):
        try:
            return UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return False

    def put(self, request, format=None):
        email = request.GET['email']
        user = self.get_object(email=email)
        if user == False:
            return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['password'] = make_password(password=data['password'], salt=None, hasher='default')
        userSerializer = UserProfileSerializer(user, data=data)
        if userSerializer.is_valid():
            userSerializer.save()
            return Response(userSerializer.data)
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        email = request.GET['email']
        user = self.get_object(email=email)
        if user is False:
            return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(email + " deleted")

class CrawlerList(APIView):
    def get(self, request, format=None):
        crawlers = Crawler.objects.all()
        if crawlers != None:
            crawlerSerializer=CrawlerSerializer(crawlers, many=True)
            return_data={"message": "Success", "crawlers": crawlerSerializer.data, 'ErrorCode': 0}
            return Response(return_data)
        return ErrorResponse().error_response(-100, 'No crawler list')

    def post(self, request, format=None):
        crawlerSerializer=CrawlerSerializer(data=request.data)
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
            crawlerSerializer=CrawlerSerializer(crawler)
            return Response(crawlerSerializer.data)
        return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name, format=None):
        crawler = self.get_object(name)
        if crawler == False:
            return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawlerSerializer=CrawlerSerializer(crawler, data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        crawler_id = request.GET['crawler_id']
        crawler=self.get_object(crawler_id)
        if crawler is False:
            Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawler.delete()
        return Response(crawler.title+" deleted")

class SubscriptionList(APIView):
    def get(self, request, format=None):
        subscription = Subscription.objects.all()
        subscriptionSerializer = SubscriptionSerializer(subscription, many=True)
        return Response(subscriptionSerializer.data)

    def post(self, request, format=None):
        '''
        TODO: 사용자 로그인 시에만 구동되도록
        user_info = Auth().verify_user(request=request, email=request.data['email'], token=request.data['user_key'])
        if not user_info['result']:
            return ErrorResponse().error_response(-1, user_info['message'])
        '''
        subscriptionsSerializer=SubscriptionSerializer(data=request.data)
        if subscriptionsSerializer.is_valid():
            subscriptionsSerializer.save()
            return_data={"message":"success", "ErrorCode":0}
            return Response(return_data)
        return ErrorResponse().error_response(-1, "Error")

class SubscriptionDetail(APIView):
    def post(self, request, format=None):

        email = request.data['email']
        subscription = Subscription.objects.filter(email=email)
        if subscription.count() == 0:
            return Response(-200, "No subscriptions")
        subscriptionSerializer = SubscriptionSerializer(subscription, many=True)
        return_data={"message":'success', "subscriptions":subscriptionSerializer.data, 'ErrorCode':0}
        return Response(return_data)

    def delete(self, request, format=None):

        email=request.data['email']
        crawler_id=request.data['crawler_id']
        subscriptions = Subscription.objects.filter(email=email)
        if subscriptions == None :
            return ErrorResponse().error_response(-1, 'Invalid user_id')
        subscription = subscriptions.filter(crawler_id=crawler_id)

        if subscription == False:
            return Response(-1, "Invalid crawler_id")
        subscription.delete()
        return_data={"message":"success", "ErrorCode":0}
        return Response(return_data)

class PushTokenList(APIView):
    def get(self, request, format=None):
        token = PushToken.objects.all()
        tokenSerializer=PushTokenSerializer(token, many=True)
        return Response(tokenSerializer.data)

    def post(self, request, format=None):
        '''
        user_info = Auth().verify_user(request=request, user_id=request.data['user_id'], user_key=request.data['user_key'])
        if not user_info['result']:
            return ErrorResponse().error_response(-1, user_info['message'])
        '''
        tokenSerializer=PushTokenSerializer(data=request.data)
        if tokenSerializer.is_valid():
            tokenSerializer.save()
            return_data={"message":"success", "ErrorCode":0}
            return Response(return_data)
        return ErrorResponse().error_response(-1, "Error")

class PushTokenDetail(APIView):
    def get_object(self, email):
        try:
            return PushToken.objects.get(email=email)
        except PushToken.DoesNotExist:
            return False
    def get(self, request, format=None):
        token = self.get_object(email=request.GET['email'])
        if token != None:
            tokenSerializer=PushTokenSerializer(token)
            return Response(tokenSerializer.data)
        return Response("Invalid user-token", status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        email = request.data['email']
        token = PushToken.objects.filter(email=email)
        if token == False:
            return Response("Invalid user-token", status=status.HTTP_400_BAD_REQUEST)
        token.delete()
        return Response(" deleted")


class SubscriberPushToken(APIView):
    def post(self, request):
        try:
            subscriber = Subscription.objects.filter(crawler_id=request.data['crawler_id'])
        except:
            data={'return_code': -100, 'message':'Invalid crawler_id'}
            return Response(data)
        #data={'subscriber':subscriber[0].user_id}
        #return Response(data)
        total = []
        for subs in subscriber:
            push_token = PushToken.objects.filter(email=subs.email)
            for pushtoken in push_token:
                arr = {'email': pushtoken.email, 'push_token': pushtoken.push_token}
                total.append(arr)

        #except:
        #    data={'return_code':-200, 'message':'No subscriber'}
        #    return Response(data)
        data = {'return_code': 0, 'data': total}
        return Response(data)
