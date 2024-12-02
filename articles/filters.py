from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from .models import Article, Topic


class ArticleFilter(filters.FilterSet):
    get_top_articles = filters.BaseInFilter(
        method="filter_get_top_articles", label="Eng ko‘p o‘qilgan 2 ta maqola"
    )
    topic_id = filters.BaseInFilter(
        method="filter_topic_id", label="Ma’lum bir mavzuga oid maqolalar"
    )

    is_recommend = filters.BooleanFilter(
        method="filter_is_recommend", label="Eng ko‘p o‘qilgan 2 ta maqola"
    )

    def filter_is_recommend(self, queryset, name, value):
        if name == 'is_recommend' and value:
            return queryset.filter(articles_more_recommended__isnull=False)


    def filter_get_top_articles(self, queryset, name, value):
        if not value or not value[0].isdigit():
            raise ValidationError(
                {
                    name: ["Enter a number."],  # Kalit nomini dinamik tarzda yuboramiz
                }
            )
        return queryset.order_by("-views_count")[: int(value[0])]

    def filter_topic_id(self, queryset, name, value):
        if not value or not value[0].isdigit():
            raise ValidationError(
                {
                    name: ["Enter a number."],  # Kalit nomini dinamik tarzda yuboramiz
                }
            )
        return queryset.filter(topics__id=int(value[0]))

    class Meta:
        model = Article
        fields = ["topic_id"]
