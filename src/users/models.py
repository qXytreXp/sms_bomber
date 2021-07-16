from src.bomber.models import Spam

from mongoengine import (
    Document,
    IntField,
    StringField,
    ReferenceField,
    DateField
)


class Subscribe(Document):
    status = StringField(default='Простой')
    date_end_vip = DateField(default=None)


class User(Document):
    user_id = IntField()
    count_sent_sms = IntField(default=0)
    spam = ReferenceField(Spam)
    subscribe = ReferenceField(Subscribe)
