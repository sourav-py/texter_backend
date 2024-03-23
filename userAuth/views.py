from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.files.base import ContentFile
from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

import jwt, datetime, base64

from twilio.rest import Client
from django.http import HttpResponse


from . import helpers
from .models import OTPObject,Profile, UserActivity
from chat.models import ChatRoom, Participation

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

        profile = Profile.objects.filter(id=payload['id']).first()

        serializer = ProfileSerializer(profile)

        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.COOKIES.get('jwt')
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        } 
        
        return response
    
class TestView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        response = Response()
        response.data = {
            "message": "success"
        }

        return response

class OTPSenderView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        TWILIO_DEFAULT_CALLERID = os.getenv("TWILIO_DEFAULT_CALLERID")

        phoneNumber = request.data['phoneNumber']

        newProfile = False

        if not Profile.objects.filter(phone = phoneNumber).exists():
            profileObject = Profile.objects.create(phone=phoneNumber)   
            profileObject.save()
            print("new profile!!!")
            newProfile = True

        otp = helpers.generateOTP()

        otpValidity = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)

        #Fetch and delete the last otp object corresponding to this phone number
        try:
            lastOTPObject = OTPObject.objects.get(phone=phoneNumber)
            lastOTPObject.delete()
        except:
            print("OTP object for this phoneNumber does not exists!!")

        #Create and store a new otp object corresponding to this phone number
        otpInstance = OTPObject.objects.create(otp=otp,phone=phoneNumber,validTill=otpValidity) 
        otpInstance.save()
        print(otpInstance)
        
        #Uncomment this send messages through twilio API
        #Make sure the following env variables are exported
        # -- TWILIO_ACCOUNT_SID
        # -- TWILIO_AUTH_TOKEN
        # -- TWILIO_DEFAULT_CALLERID

        """
        client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN) 
        message = client.messages.create(
                                body='Here is your OTP: ' + otp,
                                from_=TWILIO_DEFAULT_CALLERID,
                                to=phoneNumber)
    
        #return HttpResponse('Message Sent Successfully..')
        """
        response = Response()
        response.data = {
            'newProfile': newProfile,
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
        if True:
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

            response.set_cookie(key='jwt',value=token,httponly=True,samesite='None',secure=True,path="/")
            response.data = serializedProfile.data
        else:
            response = Response(status=400)
            response.data = {
                'message' : "OTP is invalid. Can't create a session"
            } 
            return response
            
        return response




class UserActivityStatusView(APIView):
    
    permission_classes = [AllowAny]

    def post(self,request):

        #response = Response()

        #The request is to fetch the activity status of a user
        if 'action' in request.query_params and request.query_params['action'] == 'fetch':

            chatroomId = request.data['chatroomId']
            userId = request.data['userId']

            otherParticipation = Participation.objects.filter(chatroom_id=chatroomId).exclude(user_id=userId)[0]
            otherUser = otherParticipation.user 

            activityStatusObj = UserActivity.objects.get(user=otherUser)
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
                    "status": "last seen: " + lastseenTimestamp.strftime("%Y-%m-%d %H:%M %Z")
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

class ProfileUpdate(APIView):
    permission_classes = [AllowAny]

    def options(self,request):
        # Handle preflight request
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"  # Replace with your allowed origins
        return response

    def post(self,request):
        phoneNumber = request.data['phone']
        profileObj = Profile.objects.get(phone=phoneNumber)
        serializedProfile = ProfileSerializer(instance=profileObj,data=request.data)
        print(serializedProfile)
        if serializedProfile.is_valid():
            serializedProfile.save()
            return Response(serializedProfile.data)
        else:
            print("Invalid data!!")
            response = Response()
            response.status = 500
            response.message = "Invalid data"
            return response

class FetchUser(APIView):

    permission_classes = [AllowAny] 

    def post(self,request):
        phoneNumber = request.data['phoneNumber']
        try:
            profileObj = Profile.objects.get(phone=phoneNumber)
            serializedProfile = ProfileSerializer(profileObj)
            response = Response()
            response.data = serializedProfile.data
            return response
        except:
            raise NotFound("User with this phone number does not exist!!")