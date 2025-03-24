from core.models import Item, User
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ["id","item_name","item_required","item_cost","item_stock","min_quantity"]
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        request = self.context.get('request')
        
        # Ensure request.user is a valid instance of your custom User model
        if not isinstance(request.user, User):
            raise serializers.ValidationError("Invalid user. Please authenticate properly.")
        
        validated_data['user'] = request.user
        return super().create(validated_data)
    
    # def to_representation(self, instance):
    #     print("  called")
    #     data = super().to_representation(instance)
    #     data.pop('user',None)
    #     return data
