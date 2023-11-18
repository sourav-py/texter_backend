from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

import jwt, datetime

from twilio.rest import Client
from django.http import HttpResponse


from . import helpers
from .models import OTPObject,Profile, UserActivity

import os


# Create your views here.

"""
API endpoint to login

class LoginView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True,samesite='None',secure=True)
        response.data = {
            'jwt': token
        }

        return response
"""
class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = userSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        } 
        
        return response
    


class OTPSenderView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        TWILIO_DEFAULT_CALLERID = os.getenv("TWILIO_DEFAULT_CALLERID")

        phoneNumber = request.data['phoneNumber']

        otp = helpers.generateOTP()

        otpValidity = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)

        #Fetch and delete the last otp object corresponding to this phone number
        lastOTPObject = OTPObject.objects.get(phone=phoneNumber)
        lastOTPObject.delete()

        #Create and store a new otp object corresponding to this phone number
        otpInstance = OTPObject.objects.create(otp=otp,phone=phoneNumber,validTill=otpValidity) 
        otpInstance.save()
        print(otpInstance)

        client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN) 
        message = client.messages.create(
                                body='Here is your OTP: ' + otp,
                                from_=TWILIO_DEFAULT_CALLERID,
                                to=phoneNumber)
    
        #return HttpResponse('Message Sent Successfully..')

        response = Response()
        response.data = {
            'message' : 'OTP sent successfully!!'
        }

        return response




class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        phoneNumber = request.data['phoneNumber']
        otpInput = request.data['otp']

        #Fetch the otp object corresponding to received phone number
        otpObject = OTPObject.objects.get(phone=phoneNumber)
        
        otp = otpObject.otp
        validTill = otpObject.validTill

        #DEBUG: Check time difference between the entered otp and the stored otp
        print((datetime.datetime.now(datetime.timezone.utc) - validTill).total_seconds())

        #Check the validity of the otp
        otpValid = False
        if str(otpInput) == str(otp) and (datetime.datetime.now(datetime.timezone.utc) - validTill).total_seconds()/60 < 5:
            otpValid = True

        print("OTP Valid: ",otpValid) 

        response = Response()
        if otpValid:
            if not Profile.objects.filter(phone = phoneNumber).exists():
                profileObject = Profile.objects.create(phone=phoneNumber)   
                profileObject.save()

            profile = Profile.objects.get(phone = phoneNumber) 
            payload = {
                'id': profile.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload,'secret',algorithm='HS256')
            serializedProfile = ProfileSerializer(profile)

            response = Response()
            response.set_cookie(key='jwt',value=token,httponly=True,samesite='None',secure=True)
            response.data = serializedProfile.data
        else:
            response.status = 400
            response.body = {
                'message' : "OTP is invalid. Can't create a session"
            } 
            
        return response


class UserActivityStatusView(APIView):
    
    permission_classes = [AllowAny]

    def post(self,request):

        #response = Response()

        #The request is to fetch the activity status of a user
        if 'action' in request.query_params and request.query_params['action'] == 'fetch':
            userId = request.data['userId']
            
            activityStatusObj = UserActivity.objects.get(user_id = userId)
            lastseenTimestamp = activityStatusObj.last_seen

            response = Response() 

            #If last_seen timestamp is within the last 5 seconds, send the user status as "online" 
            #Else, send the last_seen timestamp in local timezone.
            if (timezone.now() - lastseenTimestamp).total_seconds() <= 5:
                response.data = {
                    "status": "online"
                }
            else:
                localTimezone = timezone.get_current_timezone()
                lastseenTimestamp = lastseenTimestamp.astimezone(localTimezone)
                response.data = {
                    "status": lastseenTimestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
                }
            return response        
        #The request is to update the activity status of a user
        elif 'action' in request.query_params and request.query_params['action'] == 'update':

            userId = request.data['userId']
            activityStatusObj = UserActivity.objects.get(user_id = userId)
            activityStatusObj.last_seen = timezone.now()
            activityStatusObj.save()
            response = Response()
            response.data  = {
                "User activity status updated!!"
            }
            return response
        #Invalid request
        else:
            print("Invalid request!!")
            response = Response(status=400)
            response.data = {
                "message": "Invalid request params!!"
            }
            return response