import django
from django_filters import rest_framework as rest_filters
import django_filters
from . import models

class DocumentFilter(rest_filters.FilterSet):

    class Meta:
        model = models.Document
        fields ={
            'year': ['exact', 'gt', 'lt', ],
        }

class SentenceFilter(rest_filters.FilterSet):

    text = django_filters.CharFilter(field_name='token__word__text', lookup_expr='exact')
    text__contains  = django_filters.CharFilter(field_name='token__word__text', lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='document__year', lookup_expr='exact')


    class Meta:
        model = models.Sentence
        fields = {
        'id': ['exact'],
        'token__word__text': ["exact", "istartswith", "iendswith"], 
        'document__year': ["exact", "lt", "gt"],
        'document__name': ["exact"]
    }


class TokenFilter(rest_filters.FilterSet):

    text = django_filters.CharFilter(field_name='word__text', lookup_expr='exact')
    text__icontains  = django_filters.CharFilter(field_name='word__text', lookup_expr='icontains')
    text__startswith = django_filters.CharFilter(field_name='word__text', lookup_expr='istartswith')
    text__endswith   = django_filters.CharFilter(field_name='word__text', lookup_expr='iendswith')

    class Meta:
        model = models.Token
        exclude = ['sentence']