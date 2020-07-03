from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from localflavor.br.models import BRCPFField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    cpf = BRCPFField(verbose_name='CPF', primary_key=True, db_index=True)
    email = models.EmailField('email address', unique=True)
    fullname = models.CharField('full name', max_length=30, blank=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'cpf']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Purchase(models.Model):
    code = models.CharField(max_length=150, primary_key=True)
    value = models.DecimalField(
        max_digits=20, decimal_places=2, blank=False, null=False
    )
    date = models.DateField(blank=False, null=False)
    reseller = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=12, blank=False, null=False, default='Em validação'
    )

    def __str__(self):
        return self.code
