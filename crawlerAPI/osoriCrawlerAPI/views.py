from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription, PushToken, Session
from osoriCrawlerAPI.serializers import UserProfileSerializer, CrawlerSerializer, SubscriptionSerializer, PushTokenSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import HttpResponse
import re, json, random

class Auth():
    def verify_user(self, request, user_id, user_key):
        try:
            if request.session['user_id'] != user_id or request.session['user_key']!=user_key:
                return_data = {'result': 0, 'message':'Invalid session'}
                return return_data
        except:
            return_data = {'result': 0, 'message':'No have key in session'}
            return return_data
        return_data ={'result':1, 'message':'success', 'user_id':user_id, 'user_key':user_key}
        return return_data

    def email_auth(self, request, auth):
        result = {}
        try:
            user=UserProfile.objects.get(is_auth=auth) # is_auth : 권한이 있는 ID
            # is_auth가 auth인 row를 가져온다.
        except:
            return HttpResponse("Invalid user or already authenticated")
        user.is_auth='True' # user의 권한을 true로 변경.
        user.save() # Django doesn’t hit the database until you explicitly call save().
        # user의 변경 내용을 저장.
        return HttpResponse("Authenticated") # passing strings
        # HttpResponse will consume the iterator immediately, store its content as a string, and discard it.

class Password():
    def make_temp_password(self): # 임시비밀번호 생성
        Strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q', 'r', 's',
                   't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        password = ''
        for i in range(0, 8):
            password = password + Strings[random.randrange(0, 35)]
        return password

    def post(self, request): # 임시비밀번호 발송
        user_id = request.data['user_id']
        temp_password = Password().make_temp_password()
        try:
            user = UserProfile.objects.get(user_id=user_id)
        except:
            return ErrorResponse().error_response(-1, "Invalid user")

        send_mail( # from django.core.mail import send_mail
            '임시 비밀번호 입니다.', # subject
            temp_password + ' 로그인하여 비밀번호를 변경하세요', # message
            'bees1114@naver.com', # from_email
            [user_id], # recipient_list
        )
        user.password = make_password(password=temp_password, salt=None, hasher='default')
        # Creates a hashed password in the format used by this application.
        user.save()
        data = {"message": "Temp password sent", "ErrorCode": 0}
        return HttpResponse(data)

    def put(self, request): #
        try:
            user_id=request.data['user_id']
        except:
            return ErrorResponse().error_response(-1, "No user_id")
        try:
            password=request.data['password']
        except:
            return ErrorResponse().error_response(-1, "No current password")
        try:
            new_password=request.data['new_password']
        except:
            return ErrorResponse().error_response(-1, "No new_password")
        user=UserProfile.objects.get(user_id=user_id)
        chk_password=check_password(password=password, encoded=user.password)
        if chk_password is False:
            return ErrorResponse().error_response(-100, "Not correct current password")
        user.password=make_password(password=new_password, salt=None, hasher='default')
        user.save()
        return_data={"message":"success","ErrorCode":0}
        return Response(return_data)

class ErrorResponse():
    def error_response(self, ErrorCode, message):
        data={"message":message, "ErrorCode":ErrorCode}
        return Response(data)

class UserList(APIView):
    def make_auth_key(self):
        auth_key=''
        Strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for i in range(0, 15):
            auth_key = auth_key + Strings[random.randrange(0, 35)]
        return auth_key

    def get(self, request, format=None):
        users=UserProfile.objects.all()
        if users.count() == 0:
            return Response('No users')
        userSerializer = UserProfileSerializer(users, many=True)
        return Response(userSerializer.data)

    def post(self, request, format=None):
        data = request.data
        if re.match(' /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i',
                    data['user_id']) is not None:
            return ErrorResponse().error_response(-200, 'Invalid email address')
        exist=UserProfile.objects.filter(user_id=data['user_id'])
        if exist.count() != 0:
            return ErrorResponse().error_response(-100, 'Already exist user_id')

        password = make_password(password=data['password'], salt=None, hasher='default')
        is_auth = self.make_auth_key()
        url = 'http://127.0.0.1:8000/email_auth/'+is_auth+'/'
        user = {}
        user['user_id']=data['user_id']
        user['name']=data['name']
        user['password']=password
        user['is_auth']=is_auth
        userSerializer = UserProfileSerializer(data=user)

        if userSerializer.is_valid():
            userSerializer.save()
            send_mail(
                '가입인증 메일입니다.',
                url+' 이 페이지를 클릭하여 사용자 인증을 하세요.',
                'bees1114@naver.com',
                [data['user_id']],
                fail_silently=False,
            )
            return_data={'message':'Success', 'ErrorCode':0}
            return Response(return_data)
        return ErrorResponse().error_response(-1, 'Error')

class UserDetail(APIView):
    def make_user_key(self):
        Strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'q', 'r', 's',
                   't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        user_key = ''
        for i in range(0, 15):
            user_key = user_key + Strings[random.randrange(0, 35)]
        return user_key

    def authenticate(self, user_id, password):
        try:
            user = UserProfile.objects.get(user_id=user_id)
        except:
            return -1
        chk_password = check_password(password=password, encoded=user.password)
        if chk_password is False:
            return -2
        return user

    def get(self, request, format=None):
        try:
            user_id = request.GET['user_id']
        except Exception as e:
            return_data = {'message': 'No user_id', 'ErrorCode': -1}
            return Response(return_data)
        try:
            password = request.GET['password']
        except Exception as e:
            return_data = {'message': 'No password', 'ErrorCode': -1}
            return Response(return_data)
        try:
            user_key = request.session['user_key']
        except:
            user_key = 'asdf'
        try:
            token = request.GET['push_token']
        except Exception as e:
            return_data = {'message': 'No token', 'ErrorCode': -1}
            return Response(return_data)
        try:
            UserProfile.objects.get(user_id=user_id)
        except:
            return_data = {'message': 'Invalid user', 'ErrorCode': -100}
            return Response(return_data)
        user = self.authenticate(user_id=user_id, password=password)
        if UserProfile.objects.get(user_id=user_id).is_authenticated() is not True:
            return_data = {'message': 'Need authentication', 'ErrorCode': -300}
            return Response(return_data)
        if user is -1:
            return_data = {'message': 'Invalid user', 'ErrorCode': -100}
            return Response(return_data)
        elif user is -2:
            return_data = {'message': 'Invalid password', 'ErrorCode': -200}
            return Response(return_data)

        else:
            request.session['user_key'] = user_key
            request.session['user_id'] = user_id
            user_token = {}
            user_token['user_id'] = user_id
            user_token['push_token'] = token
            pushTokenSerializer = PushTokenSerializer(data=user_token)

            if pushTokenSerializer.is_valid():
                pushTokenSerializer.save()
            data = {'user_key': user_key, 'user_id': user_id, 'message': "Login success", 'ErrorCode': 0}
            return Response(data)

        return Response(return_data)

    def put(self, request, format=None):
        user_id=request.GET['user_id']
        user = self.get_object(id=user_id)
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
        user_id=request.GET['user_id']
        user=self.get_object(id=user_id)
        if user is False:
            return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(user_id + " deleted")

class CrawlerList(APIView):
    def get(self, request, format=None):
        crawlers=Crawler.objects.all()
        if crawlers != None:
            crawlerSerializer=CrawlerSerializer(crawlers, many=True)
            return_data={"message":"Success", "crawlers":crawlerSerializer.data, 'ErrorCode':0}
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
        crawler= self.get_object(name)
        if crawler != False:
            crawlerSerializer=CrawlerSerializer(crawler)
            return Response(crawlerSerializer.data)
        return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        name = request.GET['title']
        crawler=self.get_object(name)
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
        if crawler == False:
            Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawler.delete()
        return Response(crawler.title+" deleted")

class SubscriptionList(APIView):
    def get(self, request, format=None):
        subscription=Subscription.objects.all()
        subscriptionSerializer=SubscriptionSerializer(subscription, many=True)
        return Response(subscriptionSerializer.data)

    def post(self, request, format=None):
        user_info=Auth().verify_user(request=request, user_id=request.data['user_id'],user_key=request.data['user_key'])
        if not user_info['result']:
            return ErrorResponse.error_response(-1, user_info['message'])
        subscriptionsSerializer=SubscriptionSerializer(data=request.data)
        if subscriptionsSerializer.is_valid():
            subscriptionsSerializer.save()
            return_data={"message":"success", "ErrorCode":0}
            return Response(return_data)
        return ErrorResponse.error_response(-1, "Error")

class SubscriptionDetail(APIView):
    def post(self, request, format=None):
        user_info = Auth().verify_user(request=request, user_id=request.data['user_id'],
                                       user_key=request.data['user_key'])
        if not user_info['result']:
            return ErrorResponse().error_response(-1, user_info['message'])
        user_id = request.data['user_id']
        subscription = Subscription.objects.filter(user_id=user_id)
        if subscription.count() == 0:
            return Response(-200, "No subscriptions")
        subscriptionSerializer = SubscriptionSerializer(subscription, many = True)
        return_data={"message":'success', "subscriptions":subscriptionSerializer.data, 'ErrorCode':0}
        return Response(return_data)

    def delete(self, request, format=None):
        user_info = Auth().verify_user(request=request, user_id=request.data['user_id'],
                                       user_key=request.data['user_key'])
        if not user_info['result']:
            return ErrorResponse().error_response(-1, user_info['message'])

        user_id=request.data['user_id']
        crawler_id=request.data['crawler_id']
        subscriptions = Subscription.objects.filter(user_id=user_id)
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
        user_info = Auth().verify_user(request=request, user_id=request.data['user_id'],
                                       user_key=request.data['user_key'])
        if not user_info['result']:
            return ErrorResponse.error_response(-1, user_info['message'])

        tokenSerializer=PushTokenSerializer(data=request.data)
        if tokenSerializer.is_valid():
            tokenSerializer.save()
            return_data={"message":"success", "ErrorCode":0}
            return Response(return_data)
        return ErrorResponse.error_response(-1, "Error")

class PushTokenDetail(APIView):
    def get_object(self, id):
        try:
            return PushToken.objects.get(user_id=id)
        except PushToken.DoesNotExist:
            return False
    def get(self, request, format=None):
        token = self.get_object(id=request.GET['user_id'])
        if token != None:
            tokenSerializer=PushTokenSerializer(token)
            return Response(tokenSerializer.data)
        return Response("Invalid user-token", status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        token = PushToken.objects.filter(user_id=request.data['user_id'])
        if token == False:
            return Response("Invalid user-token", status=status.HTTP_400_BAD_REQUEST)
        token.delete()
        return Response(token.user_id+ "`s " +token.token+ " deleted")

class SubscriberPushToken(APIView):
    def post(self, request):
        try:
            subscriber=Subscription.objects.filter(crawler_id=request.data['crawler_id'])
        except:
            data={'return_code':-100, 'message':'Invalid crawler_id'}
            return Response(data)
        total=[]
        for subs in subscriber:
            push_token=PushToken.objects.filter(user_id=subs.user_id)
            for pushtoken in push_token:
                arr = {'user_id': pushtoken.user_id, 'push_token': pushtoken.push_token}
                total.append(arr)
        data={'return_code':0, 'data':total}
        return Response(data)
