import jwt
import pyotp

from django.shortcuts import render
from django.contrib.auth import authenticate, logout

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accountapp.serializers import UserRegisterSerializer
from accountapp.models import User


from baseapp.base import jwt_expired_time, send_otp_via_email, otp_expired_time





## creates a user
class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
      
            return Response({
                'message':'registration successfully',
                'status':status.HTTP_201_CREATED,
                'otp_expired_time':'24 hours'
            })
            
        return Response({
            'data':serializer.errors,
            'message':'Something went wrong',
            'status':status.HTTP_400_BAD_REQUEST,
        })



## login with email
class LoginAPIView(APIView):
    def post(self, request):
        try:
            username = request.data['email'] 
            password = request.data['password']
        except:
            return Response({
                'messsage':'Email and Password field required',
                'status':status.HTTP_405_METHOD_NOT_ALLOWED
            })

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({
                'message':'Username or password incorrect',
                'status':status.HTTP_400_BAD_REQUEST
            })

        payload = {
            'id':user.id,
            'exp':jwt_expired_time(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.data ={
            'message':'Successfully login',
            'token':token
        }
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response



# login with otp
class LoginWithOtp(APIView):
    def post(self, request, format=None):

        try:
            email = request.data['email'] 
        except:
            return Response({
                'messsage':'Email field required',
                'status':status.HTTP_405_METHOD_NOT_ALLOWED
            })
        
        is_send = send_otp_via_email(email=email)
        if is_send:
            return Response({
                    'message':f'otp has been successfully send to your email',
                    'status':status.HTTP_201_CREATED,
                    'otp_expired_time':'24 hours'
                }) 
        return Response({
            'message':'Something went wrong',
            'status':status.HTTP_400_BAD_REQUEST,
        })


## login otp verfication
class OtpVerificationForLogin(APIView):
    def post(self, request):
        try:
            otp = request.data['otp']
        except:
            return Response({
            'messsage':'Otp field required',
            'status':status.HTTP_405_METHOD_NOT_ALLOWED
        })

        try:
            user = User.objects.get(otp=otp)
        except:
            return Response({
                'data':'wrong Otp',
                'message':'Something went wrong',
                'status':status.HTTP_400_BAD_REQUEST,
            })
        
        print(user)
    
        totp = pyotp.TOTP(user.activation_key, interval=otp_expired_time())
        verify = totp.verify(otp)

        if not verify:
            return Response({
                'message':'Given otp is expired',
                'status':status.HTTP_408_REQUEST_TIMEOUT
            })

        user.save()

        payload = {
            'id':user.id,
            'exp':jwt_expired_time(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.data ={
            'message':'Successfully login',
            'token':token
        }
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response


## logout 
class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'User logout successfully'
        }
        return response


