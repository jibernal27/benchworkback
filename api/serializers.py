

from rest_framework import serializers

from .models import BaseUser, User, Place, File, Language

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields =  ['username', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['base_user']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ['user']

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ['user']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ['created','modified'] 