from turtle import home
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from api.models import Usuario
from api.serializers import UsuarioSerializer
# Create your views here.
# /usuarios
class UsuarioView(APIView):
    def get(self,request,format=None):
        usuarios = Usuario.objects.all()

        serializer = UsuarioSerializer(usuarios,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":usuarios.count()})
