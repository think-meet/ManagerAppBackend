import csv
import io
from django.shortcuts import get_object_or_404
from core.models import Item
from core.authentication import CustomJWTAuthentication
from .serializer import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.

# class GetItems(APIView):
    
#     authentication_classes = [CustomJWTAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, format=None):
        

class ItemView(APIView):
    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    
    def get(self, request, format=None):
        itemId = request.query_params.get('id')
        userId = request.user.id
        
        if itemId:
            item = get_object_or_404(Item, id=itemId, user=userId)
            serializer = ItemSerializer(item)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        else:
            items = Item.objects.filter(user=userId)
            serializer = ItemSerializer(items,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        
        serializer = ItemSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            item = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        itemId = request.query_params.get('id')
        userId = request.user.id
        
        try:
            item = Item.objects.get(id=itemId, user=userId)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
 
    
item_view = ItemView.as_view()

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])  # Apply authentication
@permission_classes([IsAuthenticated])
def uploadItemsFile(request):
    
    if "file" not in request.FILES:
        return Response({"error":"No file provided"},status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES["file"]
    
    if not file.name.endswith('.csv'):
        return Response({"error":"Invalid file format"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        decoded_file = file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(decoded_file))
        
        next(csv_reader, None)
        
        items_created = 0
        errors = []
        
        for row_num,row in enumerate(csv_reader, start=2):
            try:
                if len(row)<4:
                    continue
                
                item_name, item_cost, item_stock, min_quantity = row[:4]
                
                Item.objects.create(
                    user=request.user,
                    item_name=item_name.strip(),
                    item_cost=int(item_cost.strip()),
                    item_stock=int(item_stock.strip()),
                    min_quantity=int(min_quantity.strip())
                )
                items_created+=1
            
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                
            response_data = {
                "status": "success",
                "message": f"{items_created} items added successfully!",
                "errors": errors if errors else None  # Include errors if any
            }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {"status": "error", "message": "Error processing file", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# class UpdateItem(APIView):
    
#     authentication_classes = [CustomJWTAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post()