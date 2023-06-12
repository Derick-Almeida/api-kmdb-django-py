from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from utils import IsAdmin, IsCriticAndOwner
from .serializers import RegisterSerializer, LoginSerializer
from .models import User


class LoginView(ObtainAuthToken):
    def post(self, req: Request) -> Response:
        serializer = LoginSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response(
            {"detail": "invalid username or password"},
            status.HTTP_400_BAD_REQUEST,
        )


class RegisterView(APIView):
    def post(self, req: Request) -> Response:
        user = RegisterSerializer(data=req.data)
        user.is_valid(raise_exception=True)

        user.save()

        return Response(user.data, status.HTTP_201_CREATED)


class UserView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, req: Request) -> Response:
        users = User.objects.all()
        result_page = self.paginate_queryset(users, req, view=self)
        serializer = RegisterSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsCriticAndOwner]

    def get(self, req: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(req, user)

        serializer = RegisterSerializer(user)

        return Response(serializer.data)
