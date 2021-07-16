from mongoengine import Document, StringField, BooleanField


class Spam(Document):
    task_id = StringField(default=None)
    stopped = BooleanField(default=True)
