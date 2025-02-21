from rest_framework import serializers
from users.models import CustomerUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('email', 'first_name','last_name', 'password',
                  'is_staff', 'is_active', 'username')

    def create(self, validated_data):
        user = CustomerUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUser
        exclude =('groups', 'user_permissions','is_superuser')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        # Add other fields as needed
        fields = ('first_name', 'last_name',
                  'is_staff', 'is_active', 'password')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value:
                if attr == "password":
                    # Hash the password
                    instance.set_password(validated_data['password'])
                    continue    
                setattr(instance, attr, value)
        instance.save()
        return instance
