from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass

