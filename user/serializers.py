import re

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from user.models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_staff',
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[('landlord', 'Арендодатель'), ('tenant', 'Арендатор')],
        required=True
    )
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'password',
            're_password',
            'email',
            'role',
            'is_staff'
        ]

    def validate(self, attrs):
        email = attrs.get('email')



        if not email:
            raise serializers.ValidationError({'email': 'Это поле является обязательным.'})

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({'email': 'Пожалуйста, введите правильный адрес электронной почты.'})


        # if role in [RoleType.LESSEE.name, RoleType.LESSOR.name] and is_staff:
        #     raise serializers.ValidationError({
        #         'is_staff': 'У данной роли нельзя установить is_staff=True'
        #     })
        #
        # if role in [RoleType.ADMIN.name, RoleType.MODERATOR.name] and not is_staff:
        #     raise serializers.ValidationError({
        #         'is_staff': 'У данной роли необходимо установить is_staff=True.'
        #     })

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "Это поле является обязательным."}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "Это поле является обязательным."}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Пароль не совпадает."}
            )

        return attrs

    def create(self, validated_data):
        role = validated_data.get('role')

        # STAFF_ROLES = (RoleType.ADMIN.name, RoleType.MODERATOR.name)
        # validated_data['is_staff'] = role in STAFF_ROLES

        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)

        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': _('Поле email обязательно для заполнения'),
            'invalid': _('Введите корректный email адрес')
        }
    )
    # username = serializers.CharField(
    #     required=True,
    #     error_messages={
    #         'required': _('Поле username обязательно для заполнения'),
    #         'invalid': _('Введите корректное username')
    #     }
    # )

    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={
            'required': _('Поле password обязательно для заполнения'),
            'min_length': _('Пароль должен содержать минимум 8 символов')
        }
    )