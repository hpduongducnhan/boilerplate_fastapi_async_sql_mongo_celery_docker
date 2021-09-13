# -*- coding: utf-8 -*-
from datetime import datetime
from umongo import Document, fields, validate
from app.core.database.mongo import umongo_cnx


@umongo_cnx.register
class MixinCreateUpdate(Document):
    create_at = fields.DateTimeField(allow_none=True)
    update_at = fields.DateTimeField(allow_none=True)

    class Meta:
        abstract = True

    def pre_insert(self):
        if not self.create_at:
            self.create_at = datetime.utcnow()
        if not self.update_at:
            self.update_at = datetime.utcnow()

    def pre_update(self):
        self.update_at = datetime.utcnow()


@umongo_cnx.register
class User(MixinCreateUpdate):
    username = fields.StringField(unique=True, required=True)
    full_name = fields.StringField(allow_none=True)
    email = fields.EmailField(required=True)
    date_of_birth = fields.DateTimeField(allow_none=True)
    phone_number = fields.StringField(allow_none=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        collection_name = "User"


@umongo_cnx.register
class UserCredentials(MixinCreateUpdate):
    user_id = fields.ObjectIdField(required=True, unique=True)
    password = fields.StringField(max_length=255, null=False)
    google_id = fields.StringField(max_length=255, null=True)
    google_token = fields.StringField(max_length=255, null=True)
    facebook_id = fields.StringField(max_length=255, null=True)
    facebook_token = fields.StringField(max_length=255, null=True)

    class Meta:
        collection_name = "UserCredentials"
