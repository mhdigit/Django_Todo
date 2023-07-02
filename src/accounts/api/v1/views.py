from rest_framework import generics, status, mixins
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404
from ..utils import Util

from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('accounts:email_verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            # email_body = 'Hi '+user.email + \
            #     ' Use the link below to verify your email \n' + absurl
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Verify your email'}
            #  Util.send_email(data)
            data = {'email': user.email, "link": absurl, "site": current_site}
            Util.send_templated_email(
                'emails/verification_template.html', data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_tokens_for_user(self, user):
    #     refresh = RefreshToken.for_user(user)
    #     return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerialier

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class TestEmailSend(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        self.email = "admin@admin.com"
        user = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user)

        current_site = get_current_site(request).domain
        relativeLink = reverse('accounts:profile')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        data = {'email': user.email, "link": absurl, "site": current_site}
        Util.send_templated_email('emails/verification_template.html', data)

        return Response("email sent")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class VerifyEmailApiView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_verified:
            user.is_verified = True
            user.save()
        return Response({"detail": "user verified successfully"}, status=status.HTTP_200_OK)


class ResendVerifyEmailApiView(generics.GenericAPIView):

    serializer_class = ResendVerifyTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["instance"]
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('accounts:email_verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            data = {'email': user.email, "link": absurl, "site": current_site}
            Util.send_templated_email(
                'emails/verification_template.html', data)

            return Response({"details": "verification mail has been sent"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestEmailApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user).access_token
        # reverse('accounts:password-reset-confirm')
        relativeLink = "/accounts/reset-password"
        current_site = get_current_site(
            request=request).domain
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        data = {'email': user.email, "link": absurl, "site": current_site}
        Util.send_templated_email('emails/reset_password_template.html', data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetTokenValidateApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = PasswordResetTokenVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)


class PasswordResetSetNewApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
