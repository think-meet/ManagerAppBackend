import jwt
import os
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from core.models import User, Token
 
load_dotenv()
 
class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing')
 
        # Split the header into 'Bearer' and the token
        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) == 1:
            raise AuthenticationFailed(
                'Authorization header must start with Bearer'
            )
 
        # Extract the token
        accessToken = parts[1]        
 
        if request.path == '/api/user/refresh-access-token/':
            tokenValid, tokenPayload = decode_access_token(accessToken)
            if not tokenValid:
                tokenPayload = decode_expired_token(accessToken)
                
            user = User.objects.get(id=tokenPayload.get('user_id'))
            refreshToken = Token.objects.get(user_id=user.id).refresh_token
                        
            if is_refresh_token_valid(refreshToken):
                accessToken = RefreshToken(refreshToken).access_token
            else:
                raise AuthenticationFailed('Refresh token expired or invalid')
                
        else:
            tokenValid, tokenPayload = decode_access_token(accessToken)
            if tokenValid:
                user = User.objects.get(id=tokenPayload.get('user_id'))
            else:
                raise AuthenticationFailed('Access token expired or invalid')
 
        # Return the authenticated user and the token
        return (user, accessToken)


def is_refresh_token_valid(refresh_token):
    try:
        RefreshToken(refresh_token)  # Will raise error if invalid or expired
        return True
    except Exception as e:
        return False
    
def decode_access_token(access_token):
    try:
        token = AccessToken(access_token)
        return True,token.payload  
    except Exception as e:
        return False, None  # Invalid or expired token

def decode_expired_token(token):
    try:
        payload = jwt.decode(token, os.getenv("SIGNING_KEY"), algorithms=["HS256"], options={"verify_exp": False})
        return payload  # Decoded token payload (contains user_id, exp, etc.)
    except jwt.InvalidTokenError:
        return None  # Invalid token


