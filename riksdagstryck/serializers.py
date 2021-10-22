from rest_framework import serializers, filters
from . import models

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Document
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Token
        fields = ['sentence']
        depth = 1

class SentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sentence
        fields = ['id', 'document', 'text']
        depth = 1

class CountSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField(read_only=True)
    year  = serializers.SerializerMethodField(read_only=True)

    def get_count(self, model):
        return model['count']

    def get_year(self, model):
        return model['year']

    class Meta:
        model = models.Token
        fields  = ('count', 'year')