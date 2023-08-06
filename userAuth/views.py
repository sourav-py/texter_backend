from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import userSerializer
from django.contrib.auth.models import User

# Create your views here.

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = userSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
