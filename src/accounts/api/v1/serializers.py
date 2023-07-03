from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password1"]
        read_only_fields = ["is_active"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "passswords doesnt match"})

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        validated_data["is_active"] = False
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # if not self.user.is_active:
        #     raise serializers.ValidationError(
        #         {"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["username"] = self.user.username
        validated_data["user_id"] = self.user.id
        return validated_data


class ChangePasswordSerialier(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "passswords doesnt match"})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ["token"]

    def validate(self, attrs):
        token = attrs["token"]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError as identifier:
            return ValidationError({"detail": "Activation Expired"})
        except jwt.exceptions.DecodeError as identifier:
            raise ValidationError({"detail": "Invalid token"})

        attrs["user"] = user

        return super().validate(attrs)


class ResendVerifyTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs.get("email"))
        if user.is_active:
            raise serializers.ValidationError({"details": "User already verified"})
        attrs["instance"] = user
        return attrs


class PasswordResetRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise ValidationError({"detail": "There is no user with provided email"})
        attrs["user"] = user
        return super().validate(attrs)


class PasswordResetTokenVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ["token"]

    def validate(self, attrs):
        token = attrs["token"]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError as identifier:
            return ValidationError({"detail": "Token expired"})
        except jwt.exceptions.DecodeError as identifier:
            raise ValidationError({"detail": "Token invalid"})

        attrs["user"] = user
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password1 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ["password", "password1", "token"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError({"details": "Passwords does not match"})
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            user.set_password(password)
            user.save()

            return super().validate(attrs)
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
