from django.db import models
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from myapp.models import Item, Nortify


def is_notify(user):
    nortify = Nortify.objects.filter(notice_to=user,is_checked=False).exists()
    return nortify
