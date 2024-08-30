from rest_framework import serializers

from boj.models import BOJUser
from boj.serializers import BOJUserSerializer
from users.models import User


PK = 'id'


# Username or Email Serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class IsEmailUsableField(serializers.BooleanField):
    def get_attribute(self, instance):
        assert 'email' in instance, instance
        assert isinstance(instance['email'], str)
        return not User.objects.filter(email=instance['email']).exists()


class IsEmailUsableSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_usable = IsEmailUsableField(read_only=True)


class EmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class EmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class SignUpSerializer(serializers.ModelSerializer):
    verification_token = serializers.CharField()

    class Meta:
        model = User
        fields = [
            User.field_name.EMAIL,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.PASSWORD,
            User.field_name.BOJ_USERNAME,
            'verification_token',
        ]


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    boj = BOJField()

    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.USERNAME,
            User.field_name.PROFILE_IMAGE,
            'boj',
        ]
        read_only_fields = ['__all__']


class UserUpdateSerializer(serializers.ModelSerializer):
    boj = BOJField()

    class Meta:
        model = User
        fields = [
            User.field_name.EMAIL,
            User.field_name.PASSWORD,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.BOJ_USERNAME,
            'boj',
        ]
        extra_kwargs = {
            User.field_name.EMAIL: {
                'read_only': True,
            },
            User.field_name.PASSWORD: {
                'write_only': True,
                'style': {'input_type': 'password'},
            },
            User.field_name.BOJ_USERNAME: {
                'write_only': True,
            }
        }

    def save(self, **kwargs):
        instance: User = super().save(**kwargs)
        if User.field_name.PASSWORD in self.validated_data:
            instance.set_password(self.validated_data[User.field_name.PASSWORD])
            instance.save()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
        ]
        read_only_fields = ['__all__']
