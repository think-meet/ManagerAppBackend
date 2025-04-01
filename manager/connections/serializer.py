import time
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from core.models import User, Code, Connection

class CodeSerializer(serializers.Serializer):
    
    class Meta:
        model = Code
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
        
    def create(self, validated_data):
        request = self.context.get('request')
        
        if not isinstance(request.user, User):
            raise serializers.ValidationError("nvalid user. Please authenticate properly")
        
        current_epoch = int(time.time())
        
        validated_data['user'] = request.user
        validated_data['creation_epoch'] = current_epoch
        validated_data['expiry_epoch'] = current_epoch+600
        
        return super().create(validated_data)

class ConnectionSerializer(serializers.Serializer):
    
    class Meta:
        model = Connection
        fields = '__all__'
        extra_kwargs = {'connection_from': {'read_only': True},'connection_to':{'read_only':True}}
    
    def create(self, validated_data):
        request = self.context.get('request')
        ownerId = self.context.get('ownerId',None)
        
        if not isinstance(request.user, User):
            raise serializers.ValidationError("Invalid user. Please authenticate properly")
        
        validated_data['connection_to'] = request.user
        validated_data['connection_from'] = User.objects.get(id=ownerId)
        
        return super().create(validated_data)
        