from django.contrib import admin
from django.contrib.admin import site
from polls import models

site.register(models.Poll)
site.register(models.Vote)
