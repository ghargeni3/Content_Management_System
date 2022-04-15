import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):

    # These fields tie to the roles!
    ADMIN = 1
    AUTHOR = 2

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (AUTHOR, 'Author')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()
    is_staff = models.BooleanField(default=False)

    phone 					= PhoneNumberField(null=True, blank=False, unique=False)
    # phone = PhoneNumber.from_string(phone_number=raw_phone, region='RU').as_e164
    address 				= models.CharField(max_length=30, blank=True, default='')
    city 					= models.CharField(max_length=30, blank=True, default='')
    state 					= models.CharField(max_length=30, blank=True, default='')
    country					= models.CharField(max_length=30, blank=True, default='')
    pincode 				= models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Content(models.Model):

	uid      = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
	title    = models.CharField(max_length=30, blank=False)
	body     = models.CharField(max_length=300, blank=False)
	summury  = models.CharField(max_length=60, blank=False)
	author   = models.CharField(max_length=60,blank=False)
	categories   = models.CharField(max_length=60,blank=False)
	document     = models.FileField(blank=False, null=False)

	def __str__(self):
		return self.title