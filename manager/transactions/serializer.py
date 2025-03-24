from rest_framework import serializers
from core.models import Transaction, User

class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
        
    def create(self, validated_data):
        
        request = self.context.get('request')
        
        if not isinstance(request.user, User):
            raise serializers.ValidationError("Invalid user. Please authenticate properly.")

        validated_data['user'] = request.user
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('user',None)
        return data
        
    