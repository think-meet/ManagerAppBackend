from django.shortcuts import get_object_or_404
from core.models import Transaction
from core.authentication import CustomJWTAuthentication
from .serializer import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TransactionView(APIView):
    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    
    def get(self, request, format=None):
        startDate = request.query_params.get('start_date')
        endDate = request.query_params.get('end_date')
        userId = request.user.id

        if startDate and endDate:
            transactions = Transaction.objects.filter(transaction_date_time__range=[startDate,endDate],user=userId)
        else:
            transactions = Transaction.objects.filter(user=userId)
            
        serializer = TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        
        serializer = TransactionSerializer(data=request.data, context={'request':request})
        
        if serializer.is_valid():
            transaction = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
transaction_view = TransactionView.as_view()