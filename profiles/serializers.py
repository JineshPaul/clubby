from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from . import models

class UserSerializer(serializers.ModelSerializer):
    """
    User information Get and put API
    """
    name = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'phone_number', 'gender', 'name', 'first_name', 'last_name', 'image')



class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Information after login and signup
    """
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(read_only=True, source="get_full_name")

    class Meta:
        model = models.User
        fields = ('email', 'phone_number', 'password', 'name')