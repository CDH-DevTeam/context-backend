from django.db.models import Count, Sum, F, FloatField
from django.db.models.functions import Cast
from rest_framework import viewsets, generics
from django_filters import rest_framework as rest_filters
import rest_framework
from . import models
from . import serializers
from . import filters


class CountViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CountSerializer

    def get_queryset(self):

        word = self.request.query_params.get('word', None)
        mode = self.request.query_params.get('mode', None)
        factor = 1e5

        if word:
            if mode == 'absolute' or not mode:
                queryset = models.Token.objects.filter(word__text=word)\
                                            .values('sentence__document__year')\
                                            .annotate(year=F('sentence__document__year'), count=Count('word'))\
                                            .values('year', 'count')\
                                            .order_by('year')\
                                            .all()                        

                return queryset

            elif mode == 'relative':
                queryset =  models.Token.objects.filter(word__text=word)\
                                                 .values('sentence__document__year')\
                                                 .annotate(year=F('sentence__document__year'),
                                                           absolute=Count('word'),
                                                           n_words=Sum('sentence__document__n_words')
                                                           )\
                                                 .values('year', 'absolute', 'n_words')\
                                                 .annotate(count=factor*Cast(F('absolute'), FloatField())/Cast(F('n_words'), FloatField()))\
                                                 .values('year', 'count')\
                                                 .order_by('year')\
                                                 .all() 

                return queryset

            else:
                return models.Token.objects.none()

        else:
            return models.Token.objects.none()

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filter_class = filters.DocumentFilter

class SentenceViewSet(viewsets.ModelViewSet):

    queryset = models.Sentence.objects.prefetch_related('token_set').all()
    serializer_class = serializers.SentenceSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, rest_framework.filters.OrderingFilter]
    ordering = ['document__year']
    filter_class = filters.SentenceFilter
    # filter_backends = [rest_framework.filters.SearchFilter, rest_framework.filters.OrderingFilter]
    # search_fields = ['^token__word__text']

class TokenViewSet(viewsets.ModelViewSet):
    queryset = models.Token.objects.all()
    serializer_class = serializers.TokenSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filter_class = filters.TokenFilter
