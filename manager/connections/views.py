import random
import string
import time
from django.db.models import Q
from core.models import Code, Connection
from core.authentication import CustomJWTAuthentication
from .serializer import CodeSerializer, ConnectionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound


def generate_random_string(length=4):
    characters = string.ascii_letters + string.digits  # Includes both letters and digits
    return ''.join(random.choice(characters) for _ in range(length))

# Create your views here.
class CodeView(APIView):
    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer
    
    def get(self, request, format=None):        
        code = generate_random_string().capitalize()
        serializer = CodeSerializer(code, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
code_view = CodeView.as_view()

class ConnectionView(APIView):
    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionSerializer
    
    def get(self, request, format=None):
        userId = request.user.id
        
        try:
            allConnections = Connection.objects.filter(Q(connection_from__id=userId) | Q(connection_to__id=userId))
            
            connections = []
            for connection in allConnections:
                connections.append(
                    {
                        "id": connection.id,
                        "from": connection.connection_from.email,
                        "to": connection.connection_to.email
                    }
                )
                
            return Response(connections,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, format=None):
        try:
            code = request.data.get("code",None)
            
            if not code:
                return Response("Code is required",status=status.HTTP_400_BAD_REQUEST)
            
            codeObj = Code.objects.filter(code=code).order_by('-creation_epoch').first()
            
            current_epoch = int(time.time())
            
            if codeObj.creation_epoch<=current_epoch and current_epoch<=codeObj.expiry_epoch:
                serializer = ConnectionSerializer()
                
                if serializer.is_valid():
                    connection = serializer.save()
                    
                    connectionData = {
                        "id": connection.id,
                        "from": connection.connection_from.email,
                        "to": connection.connection_to.email
                    }
                    
                    return Response(connectionData,status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response("Code expired", status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": "An unexpected error occurred."},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        connectionId = request.data.get("id",None)
        
        if connectionId is None:
            return Response("Connection id needed",status=status.HTTP_400_BAD_REQUEST)
        
        try:
            connection = Connection.objects.get(id=connectionId)
            connection.delete()
            return Response("Connection deleted successfully", status=status.HTTP_200_OK)
        except Connection.DoesNotExist:
            raise NotFound(detail="Connection not found")

connection_view = ConnectionView.as_view()
