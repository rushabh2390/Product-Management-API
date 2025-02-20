from rest_framework import serializers
from users.models import CustomerUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('email', 'name', 'password','is_staff','is_active','username')

    def create(self, validated_data):
        user = CustomerUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUser
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        # Add other fields as needed
        fields = ('name', 'is_staff', 'is_active')
