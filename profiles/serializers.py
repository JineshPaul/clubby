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
        fields = ('email', 'phone_number', 'gender', 'name', 'first_name', 'last_name', 'occupation','image')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Information after login and signup
    """
    password = serializers.CharField(write_only=True)
    class Meta:
        model = models.User
        fields = ('email', 'phone_number', 'password','occupation','first_name')


class AddressSerializer(serializers.Serializer):
    """
    This is address serializer.
    This is for the continue button.
    """
    pincode = serializers.CharField(allow_blank=False, allow_null=False, max_length=2048, required=True)
    address1 = serializers.CharField(allow_blank=False, allow_null=False, max_length=2048, required=True)
    address2 = serializers.CharField(allow_blank=True, allow_null=True, max_length=2048, required=False)
    city = serializers.CharField(allow_blank=False, allow_null=False, max_length=2048, required=True)
    district = serializers.CharField(allow_blank=False, allow_null=False, max_length=2048, required=True)
    state = serializers.CharField(allow_blank=False, allow_null=False, max_length=2048, required=True)
    country = serializers.CharField(allow_blank=False, allow_null=False, max_length=2048, required=True)


class AdditionalInfoSerializer(serializers.ModelSerializer):
    """
    Users Additional information
    """
    class Meta:
        model = models.User
        fields = ('dob', 'gender', 'marital_status')