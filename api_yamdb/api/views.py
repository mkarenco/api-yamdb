from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer


class RegisterUserViewSet(viewsets.ModelViewSet):
    pass


class UsersViewSet(viewsets.ModelViewSet):
    pass