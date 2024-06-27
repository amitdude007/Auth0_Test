from rest_framework import serializers

from ...user.models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            '_id',
            'email',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            '_id',
            'email',
            'password',
            'auth0_user_id',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            '_id': {'read_only': True},
            'auth0_user_id': {'read_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
