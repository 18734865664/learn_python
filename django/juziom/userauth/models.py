# -*- coding:UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from registration.signals import user_registered


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    level = models.IntegerField(u'权限级别', default=1)

    class Meta:
        verbose_name = u'权限'
        verbose_name_plural = verbose_name


def create_user_profile(**kwargs):
    UserProfile.objects.get_or_create(user=kwargs['user'])


user_registered.connect(create_user_profile)
