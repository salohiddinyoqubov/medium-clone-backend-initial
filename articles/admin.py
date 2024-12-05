# Register your models here.
from django.contrib import admin

from articles.models import Article, Topic, TopicFollow

admin.site.register(Topic)

admin.site.register(Article)
admin.site.register(TopicFollow)

