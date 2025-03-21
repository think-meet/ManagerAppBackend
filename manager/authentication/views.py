from django.shortcuts import render
from core.models import User, Token
from core.authentication import CustomJWTAuthentication
from .serializer import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Register(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
register_view = Register.as_view()

class ResetPassword(APIView):
    
    def post(self, request, format=None):
        
        email = request.data.get("email")
        password = request.data.get("password")
    
        if email:
            email = email.strip()
            if email == "":
                return Response({"email":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"email":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not password or password=="":
            return Response({"password":"Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found"},status=status.HTTP_401_UNAUTHORIZED)
        
        user.password = make_password(password=password)
        user.save()
    
        return Response({"email":email},status=status.HTTP_202_ACCEPTED)
            
reset_password_view = ResetPassword.as_view()

class Login(APIView):
    def post(self, request, format=None):
        
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email:
            email = email.strip()
            if email == "":
                return Response({"email":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"email":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not password or password=="":
            return Response({"password":"Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found"},status=status.HTTP_401_UNAUTHORIZED)
        
        is_owner = check_password(password,user.password)
                
        if not is_owner:
            return Response({"error":"Invalid email or password"},status=status.HTTP_401_UNAUTHORIZED)
        
        refreshToken = RefreshToken()
        refreshToken["user_id"] = user.id
        accessToken = refreshToken.access_token
        
        Token.objects.create(refresh_token=str(refreshToken), user=user)
        
        return Response({"access_token":str(accessToken),"refresh_token":str(refreshToken)},status=status.HTTP_200_OK)
    
login_view = Login.as_view()

class Logout(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        try:
            user = request.user
            accessToken = request.auth
            
            tokenObj = Token.objects.get(user_id=user.id)
            
            token = RefreshToken(tokenObj.refresh_token)
            token.blacklist()
            
            Token.objects.filter(user_id=user.id).delete()
            user._is_authenticated = False
            
            return Response({"message":"Logged out Successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":"Unbale to logout"},status=status.HTTP_400_BAD_REQUEST)
    
logout_view = Logout.as_view()

# class ResetPassword(APIView):
#     def post(self, request, format=None):
#         serializer = ResetPasswordSerializer(data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
# reset_password_view = ResetPassword.as_view()
