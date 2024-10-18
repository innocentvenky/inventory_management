from rest_framework import serializers
from . models import Items
from django.contrib.auth.models import User

#create serializers
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id','username','email')
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  
        )
        return user
        
class Loginserializer(serializers.Serializer):
        username=serializers.CharField(required=True)
        password=serializers.CharField(required=True,write_only=True)

class Item_serializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = "__all__"