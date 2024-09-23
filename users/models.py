import random
import uuid

from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail, UserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_supper, **extra_fields):
        """
        Create and save a user with the given username, phone_number, email, password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('Users must have an username')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          phone_number=phone_number,
                          email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_supper,
                          date_joined=now,
                          **extra_fields)
        if not extra_fields.get('no password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = "".join(random.sample('abcdefghijklmnopqrstuvwxyz', 4)) + str(phone_number)[-4:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)


    def create_superuser(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(verbose_name=_('username'), max_length=32, unique=True,
                                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only",
                                validators=[
                                    validators.RegexValidator(regex=r"^[a-zA-z][a-zA-z0-9_\.]+$",
                                                              message=_("Enter a valid username."),
                                                              code="Invalid username")
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                })
    first_name = models.CharField(verbose_name=_('first name'), max_length=30, blank=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=30, blank=True)
    email = models.EmailField(verbose_name=_('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(verbose_name=_('phone number'), unique=True, null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(regex=r"^989[0-39]\d{8}$",
                                                                        message=_("Enter a valid phone number."),
                                                                        code="Invalid phone number")
                                          ],
                                          error_messages={
                                              'unique': _("A user with that phone number already exists."),
                                          })
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(verbose_name=_('active status'), default=True,
                                    help_text=_('Designates whether this user should be treated as active.'
                                                'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(verbose_name=_('last seen'), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None , **kwargs):
        """
        Send an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):
        """
        Returns True if user is logged in with valid credentials.
        """
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
        PREFER_NOT_TO_SAY = 'N', _('Prefer not to say')


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(verbose_name=_('nick name'), max_length=30, blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, upload_to='UsersAvatar/')
    birthday = models.DateField(verbose_name=_('birthday'), null=True, blank=True)
    gender = models.CharField(verbose_name=_('gender'), max_length=1, choices=Gender.choices,
                              default=Gender.PREFER_NOT_TO_SAY)
    province = models.ForeignKey(verbose_name=_('province'), to='Province', null=True, on_delete=SET_NULL)

    class Meta:
        db_table = 'user_profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


    @property
    def get_full_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nick_name(self):
        return self.nick_name if self.nick_name else self.user.username

class Device(models.Model):
    class DeviceType(models.TextChoices):
        WEB = 'WEB', _('Web')
        IOS = 'IOS', _('IOS')
        ANDROID = 'AND', _('Android')
        OTHER = 'OTH', _('Other')

    user = models.ForeignKey(verbose_name=_('user'), to=User, on_delete=models.CASCADE, related_name='devices')
    device_uuid = models.UUIDField(verbose_name=_('device uuid'), unique=True, default=uuid.uuid4, editable=False, null=True)

    last_login = models.DateTimeField(verbose_name=_('last login date'), null=True)
    device_type = models.CharField(verbose_name=_('device type'), max_length=3, choices=DeviceType.choices,
                                   default=DeviceType.WEB)
    device_os = models.CharField(verbose_name=_('device OS'), max_length=20, blank=True)
    device_model = models.CharField(verbose_name=_('device model'), max_length=50, blank=True)
    app_version = models.CharField(verbose_name=_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_device'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = (('user', 'device_uuid'),)

class Province(models.Model):
    name = models.CharField(verbose_name=_('province name'), max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
