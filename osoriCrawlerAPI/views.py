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
    def verify_user(request):
        try:
            user_id=request.GET.get('user_id')
            user_key=request.GET.get('user_key')
        except:
            return False, -1, -1, "No 'user_id' or 'user_key'"

        try:
            if request.session['user_id'] != user_id or request.session['user_key']!=user_key:
                return False, -1, -1, "Invalid session"
        except:
            return False, -1, -1, "No have key in session"

        return True, user_id, user_key

    def email_auth(request, auth):
        result = {}
        try:
            user=UserProfile.objects.get(is_auth=auth)
        except:
            return HttpResponse("Invalid user or already authenticated")
        user.is_auth='True'
        user.save()
        return HttpResponse("Authenticated")

class ForgetPassword():
    def make_temp_password():
        Strings=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','q','r','s',
                 't','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','0']
        password=''
        for i in range(0,8):
            password=password+Strings[random.randrange(0,35)]
        return password

    def send_temp_password(self, user_id):
        temp_password = ForgetPassword.make_temp_password()
        try:
            user= UserProfile.objects.get(user_id=user_id)
        except:
            return HttpResponse("Invalid user")

        send_mail(
            '임시 비밀번호 입니다.',
            temp_password+' 로그인하여 비밀번호를 변경하세요',
            'bees1114@naver.com',
            [user_id],
        )
        user.password=make_password(password=temp_password, salt=None, hasher='default')
        user.save()
        return HttpResponse("Temp password sent")

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
            return Responshe("Invalid email adress")
        data['password'] = make_password(password=data['password'], salt=None, hasher='default')
        data['is_auth'] = self.make_auth_key()
        url = 'http://127.0.0.1:8000/email_auth/'+data['is_auth']+'/'
        userSerializer = UserProfileSerializer(data=data)
        if userSerializer.is_valid():
            userSerializer.save()
            send_mail(
                '가입인증 메일입니다.',
                url+' 이 페이지를 클릭하여 사용자 인증을 하세요.',
                'bees1114@naver.com',
                [data['user_id']],
                fail_silently=False,
            )

            return Response(userSerializer.data, status=status.HTTP_201_CREATED)

        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, id):
        try:
            return UserProfile.objects.get(user_id=id)
        except UserProfile.DoesNotExist:
            return False

    def get(self, request, format=None):
        user_id=request.GET.get('user_id')
        user = self.get_object(id=user_id)
        if user == None:
            return Response('No user')
        is_verified = Auth.verify_user(request=request)
        if is_verified[0] == False:
            return Response(is_verified[3])
        userSerializer = UserProfileSerializer(user)
        return Response(userSerializer.data)

    def put(self, request, format=None):
        user_id=request.GET.get('user_id')
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
        user_id=request.GET.get('user_id')
        user=self.get_object(id=user_id)
        if user == False:
            return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(user_id + " deleted")

class CrawlerList(APIView):
    def get(self, request, format=None):
        crawlers=Crawler.objects.all()
        if crawlers != None:
            crawlerSerializer=CrawlerSerializer(crawlers, many=True)
            return Response(crawlerSerializer.data)
        return Response("No crawler list")

    def post(self, request, format=None):
        crawlerSerializer=CrawlerSerializer(data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrawlerDetail(APIView):
    def get_object(self, name):
        try:
            return Crawler.objects.get(name=name)
        except Crawler.DoesNotExist:
            return False

    def get(self, request, name, format=None):
        crawler= self.get_object(name)
        if crawler != False:
            crawlerSerializer=CrawlerSerializer(crawler)
            return Response(crawlerSerializer.data)
        return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name, format=None):
        crawler=self.get_object(name)
        if crawler == False:
            return Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawlerSerializer=CrawlerSerializer(crawler, data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        crawler=self.get_object(name)
        if crawler == False:
            Response("Invalid crawler", status=status.HTTP_400_BAD_REQUEST)
        crawler.delete()
        return Response(name+" deleted")

class SubscriptionList(APIView):
    def get(self, request, format=None):
        subscription=Subscription.objects.all()
        subscriptionSerializer=SubscriptionSerializer(subscription, many=True)
        return Response(subscriptionSerializer.data)
    def post(self, request, format=None):
        subscriptionsSerializer=SubscriptionSerializer(data=request.data)
        if subscriptionsSerializer.is_valid():
            subscriptionsSerializer.save()
            return Response(subscriptionsSerializer.data)
        return Response(subscriptionsSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

class SubscriptionDetail(APIView):
    def get(self, request, format=None):

        user_id = request.GET.get('user_id')
        crawler_id = request.GET.get('crawler_id')
        if user_id != None:
            verified_user = Auth.verify_user(request=request)
            if verified_user[0] is False:
                return Response("Not valid user")
            subscription = Subscription.objects.filter(user_id=user_id)
            if subscription.count() == 0:
                return Response("No subscriptions", status=status.HTTP_400_BAD_REQUEST)
            subscriptionSerializer = SubscriptionSerializer(subscription, many=True)

        elif crawler_id != None:
            subscription = Subscription.objects.filter(crawler_id=crawler_id)
            if subscription.count() == 0:
                return Response("No subscriptions", status=status.HTTP_400_BAD_REQUEST)
            subscriptionSerializer = SubscriptionSerializer(subscription, many=True)
        else:
            return Response("No subscriptions" ,status=status.HTTP_400_BAD_REQUEST)
        return Response(subscriptionSerializer.data)

    def delete(self, request, format=None):
        user_id=request.GET.get('user_id')
        crawler_id=request.GET.get('crawler_id')
        subscriptions = Subscription.objects.filter(user_id=user_id)
        if subscriptions == None :
            return Response('Invalid user_id', status=status.HTTP_400_BAD_REQUEST)
        subscription = subscriptions.filter(crawler_id=crawler_id).delete()

        if subscription == False:
            return Response("Invalid crawler_id", status=status.HTTP_400_BAD_REQUEST)
        return Response(user_id+ "`s "+crawler_id+" subscription" +" deleted")


class PushTokenList(APIView):
    def get(self, request, format=None):
        token = PushToken.objects.all()
        tokenSerializer=PushTokenSerializer(token, many=True)
        return Response(tokenSerializer.data)

    def post(self, request, format=None):
        tokenSerializer=PushTokenSerializer(data=request.data)
        if tokenSerializer.is_valid():
            tokenSerializer.save()
            return Response(tokenSerializer.data)
        return Response(tokenSerializer.error(), status=status.HTTP_400_BAD_REQUEST)

class PushTokenDetail(APIView):
    def get_object(self, id):
        try:
            return PushToken.objects.get(user_id=id)
        except PushToken.DoesNotExist:
            return False
    def get(self, request, id, format=None):
        token = self.get_object(id=id)
        if token != None:
            tokenSerializer=PushTokenSerializer(token)
            return Response(tokenSerializer.data)
        return Response("Invalid user-token", status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        token = self.get_object(id)
        if token == False:
            return Response("Invalid user-token", status=status.HTTP_400_BAD_REQUEST)
        token.delete()
        return Response(token.user_id+ "`s " +token.token+ " deleted")

class Login(APIView):
    def authenticate(self, user_id, password):
        try:
            user=UserProfile.objects.get(user_id=user_id)
        except:
            return -1
        chk_password=check_password(password=password, encoded=user.password)
        if chk_password is False:
            return -2
        return user

    def post(self, request):
        try:
            user_id=request.data['user_id']
        except Exception as e:
            return Response("No user_id")
        try:
            password=request.data['password']
        except Exception as e:
            return Response("No password")
        try:
            user_key = request.session['user_key']
        except:
            user_key = "asdf"

        user=self.authenticate(user_id=user_id, password=password)
        if UserProfile.objects.get(user_id=user_id).is_authenticated() is not True:
            return Response("Need authentication")
        if user is -1:
            return Response("Invalid user")
        elif user is -2:
            return Response("Invalid password")
        else:
            request.session['user_key'] = user_key
            request.session['user_id'] = user_id
            data = {'user_key':user_key, 'user_id':user_id, 'message':"Login success"}
            return Response(data)

class ChangePassword(APIView):
    def post(self, request):
        try:
            user_id=request.data['user_id']
        except:
            return Response("No user_id")
        try:
            password=request.data['password']
        except:
            return Response("No current password")
        try:
            new_password=request.data['new_password']
        except:
            return Response("No new_password")
        user=UserProfile.objects.get(user_id=user_id)
        user.password=make_password(password=new_password, salt=None, hasher='default')
        user.save()
        return Response("Password changed")

