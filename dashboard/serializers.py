from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class WasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset=User.objects.all())
    full_bins = serializers.SerializerMethodField()
    spacious_bins = serializers.SerializerMethodField()
    half_bins = serializers.SerializerMethodField()

    class Meta:
        model  = WasteBin
        fields = "__all__"



    def full_bins(self, obj):
        return obj.full_bins
    
    def half_bins (self, obj):
        return obj.half_bins
    
    def spacious_bins(self, obj):
        return obj.spacious_bins
    

class RequestWasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset=User.objects.all())
    class Meta:
        model = WasteBinRequest
        fields = ["user", "location", "latitude", "longitude","date_requested"]

class WastePickRequestSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset = User.objects.all())
    Bin = WasteBinSerializer()

    class Meta:
        model  = WastePickUp
        fields = ["user", "Bin"]





