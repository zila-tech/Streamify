from django.db import models
from django.urls import reverse
import string
import random
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
)
from django.db.models.functions import Now, Concat
from django.utils.translation import gettext_lazy as _
import pycountry


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),  # convert letters to lowercase
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user


class Gender(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    OTHER = "Other", "Other"


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=Gender, default=Gender.MALE)
    date_joined = models.DateTimeField(db_default=Now())
    last_login = models.DateTimeField(db_default=Now(), auto_now=True)
    is_admin = models.BooleanField(db_default=False)
    is_staff = models.BooleanField(db_default=False)
    is_active = models.BooleanField(db_default=False)
    is_superadmin = models.BooleanField(db_default=False)
    usid = models.CharField(max_length=10, unique=True, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager()

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    def save(self, *args, **kwargs):
        if not self.usid:
            alphanumeric = string.ascii_uppercase + string.digits
            usid = "".join(random.choices(alphanumeric, k=9))
            usid += random.choice(string.digits)
            self.usid = usid.capitalize()
        super(Account, self).save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_user_type(self):
        if self.is_accountant:
            return "accountant"

    @property
    def is_superuser(self):
        return self.is_admin
