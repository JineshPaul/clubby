from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Movie
        fields = ('movie', 'category', 'title', 'description')




class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cast
        fields = ('role_name','real_name','email','phone_number','gender','image')


