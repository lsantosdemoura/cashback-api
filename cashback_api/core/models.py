from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from localflavor.br.models import BRCPFField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(_('full name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    cpf = BRCPFField(verbose_name='CPF', unique=True, db_index=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('reseller')
        verbose_name_plural = _('resellers')


class Shopping(models.Model):
    code = models.CharField(max_length=150, blank=False, null=False)
    value = models.DecimalField(
        max_digits=20, decimal_places=2, blank=False, null=False
    )
    date = models.DateField(blank=False, null=False)
    reseller = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, blank=False, null=False)
