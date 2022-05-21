from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from auth_module.models import AuthUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'email', 'password', 'user_type')
