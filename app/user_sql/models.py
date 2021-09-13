# -*- coding: utf-8 -*-
from tortoise.models import Model
from tortoise import fields


class CreateUpdateMixin:
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)


class User(CreateUpdateMixin, Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, null=False, unique=True)
    full_name = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, null=True)
    date_of_birth = fields.DatetimeField(null=True)
    phone_number = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return self.username


class UserCredentials(CreateUpdateMixin, Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("user.User", related_name="user", on_delete="CASCADE", unique=True)
    password = fields.CharField(max_length=255, null=False)
    google_id = fields.CharField(max_length=255, null=True)
    google_token = fields.CharField(max_length=255, null=True)
    facebook_id = fields.CharField(max_length=255, null=True)
    facebook_token = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.user}_credentials'
