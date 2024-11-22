# Register your models here.
from django.contrib import admin

from articles.models import Article, Topic

admin.site.register(Topic)

admin.site.register(Article)
