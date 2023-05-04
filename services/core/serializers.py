from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        ref_name = "UserCreateSerializer"
        fields = ['id', 'username', 'email','first_name', 'last_name', 'password']
    
class UserSerializer(BaseUserSerializer, serializers.Serializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = "UserSerializer"
        fields = ['id','username', 'email', 'first_name', 'last_name']
