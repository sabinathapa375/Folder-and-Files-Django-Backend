from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, SignupSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

class SignupAPIView(APIView):
   
    def post(self,request):
            serializer = SignupSerializer(data = request.data)
            if serializer.is_valid():
                    """If the validation success, it will created a new user."""
                    serializer.save()
                    res = { 'status' : status.HTTP_201_CREATED }
                    return Response(res, status = status.HTTP_201_CREATED)
            res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
  
  
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        
            
       
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Generating JWT tokens using simplejwt
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": str(refresh),
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Username or Password",
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Bad Request",
                "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
 
        
 
