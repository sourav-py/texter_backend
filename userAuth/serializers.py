from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
    
    def create(self,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

