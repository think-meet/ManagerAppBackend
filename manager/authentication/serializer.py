from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','email','password']
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
# class ResetPasswordSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = ['email','password']
#         extra_kwargs = {'password':{'write_only':True}}
        
#     def __init__(self, *args, **kwargs):
#         """Remove unique field validation for email to prevent 'User already exists' error."""
#         super().__init__(*args, **kwargs)
#         self.fields['email'].validators = []
    
#     def validate(self, attrs):
#         email = attrs.get("email")
#         password = attrs.get("password")
        
#         print("in the validation logic")
        
#         if not email or email=="":
#             raise serializers.ValidationError({"email":"Please check email id"})

#         if not password or password=="":
#             raise serializers.ValidationError({"password":"Please check password"})
        
#         return attrs

#     def save(self, **kwargs):
        
#         email = self.validated_data["email"]
#         password = self.validated_data["password"]
        
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise serializers.ValidationError({"error":"User not found"})
        
#         user.password = make_password(password=password)
#         user.save()
#         return user
    
    