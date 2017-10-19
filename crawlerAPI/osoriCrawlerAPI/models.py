from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError('No user Email, Give me Email!!')
        if not name:
            raise ValueError('No user name, Give me name!!')
        if not password:
            raise ValueError('No user password, Give me password!!')

        user = UserProfile(email=self.normalize_email(email), name=name, password=make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, password=password, name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user

#Models for user profile
class UserProfile(AbstractBaseUser, models.Model):
    email = models.EmailField(verbose_name='email address', primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_auth = models.CharField(max_length=100, default='False')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def is_email_authenticated(self):
        if self.is_auth is 'False':
            return False
        else:
            return True

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return UserProfile(value)

    def to_python(self, value):
        if isinstance(value, UserProfile):
            return value
        if value is None:
            return value
        return UserProfile(value)

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        ordering = ('created',)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

'''Models for Crawler'''
class Crawler(models.Model):
    crawler_id = models.CharField(max_length=100, primary_key=True)
    thumbnail_url = models.CharField(max_length=100)
    link_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created = models.DateField(auto_now=True)
    
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Crawler(value)

    def to_python(self, value):
        if isinstance(value, Crawler):
            return value
        if value is None:
            return value
        return Crawler(value)

    class Meta:
        ordering = ('title', 'created', 'crawler_id',)

'''Models for Information of who subscript which crawlers'''
class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crawler = models.ForeignKey(Crawler, on_delete=models.CASCADE)
    latest_pushtime = models.DateField(auto_now_add=True)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Subscription(value)

    def to_python(self, value):
        if isinstance(value, Subscription):
            return value
        if value is None:
            return value
        return Subscription(value)

    class Meta:
        ordering = ('subscriber', 'crawler')
        unique_together = (('subscriber', 'crawler'),)

'''Models for user and who`s device token'''
class PushToken(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    push_token = models.CharField(max_length=100)
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return PushToken(value)

    def to_python(self, value):
        if isinstance(value, PushToken):
            return value
        if value is None:
            return value
        return PushToken(value)
    
    class Meta:
        ordering = ('owner',)
        unique_together = (('owner', 'push_token'),)
