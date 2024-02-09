from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated

class Register_user(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user= CustomUser.objects.all()
        user_serilizer =UserSerializer(user, many=True)
        return Response( user_serilizer.data)

    def post(self, requset):
        register_serilizer =  UserSerializer(data=requset.data)
        if  register_serilizer.is_valid():
             register_serilizer.save()
             return Response( register_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(register_serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
