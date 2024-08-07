from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import *
from django.http import Http404
from .models import *

from django.http.response import HttpResponse

class DashViewset(ReadOnlyModelViewSet):
    queryset = WasteBin.objects.prefetch_related("compartments").all()
    permission_classes = (IsAuthenticated,)
    serializer_class = WasteBinSerializer


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

class WasteBinViewset(ModelViewSet):
    pass
    

class WasteBinRequest(ModelViewSet):
    queryset = WasteBinRequest
    serializer_class = RequestWasteBinSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get','post', 'delete']

class WasteBinPickupView(ModelViewSet):
    queryset = WastePickUp.objects.all()
    permission_classes = (IsAuthenticated,)
   


    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    
