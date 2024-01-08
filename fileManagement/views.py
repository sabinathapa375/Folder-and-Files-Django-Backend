from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework.response import Response
from .permission import IsOwnerOfFile
from accounts.serializers import UserSerializer

class FolderList(generics.ListAPIView):
    queryset = Folder.objects.filter(parent_folder=None)
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    
class FileViewSet(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfFile]
    
    def create(self, request, *args, **kwargs):
        folder_id =1
    
        if request.user.is_superuser:  
            folder_id = 2
            for_user_id = request.data.get('for_user_id')
            if for_user_id:
                try: 
                    for_user = User.objects.get(id=for_user_id)
                except User.DoesNotExist:
                    return Response({'error':'Invalid user ID'}) 
                
                file = File(user=request.user, 
                            for_user=for_user,
                            name=request.data['name'],
                            file_type=request.data['file_type'],
                            file=request.data['file'],
                            folder_id = folder_id)
        
        else:
            file = File(user=request.user,  
                        name=request.data['name'],
                        file_type=request.data['file_type'],
                        file=request.data['file'],
                        folder_id = folder_id)                
        file.save()
        return Response(status=status.HTTP_201_CREATED) 
     
    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def perform_destroy(self, instance):
        instance.delete()
     
        
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class IsSuperuserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        is_superuser = request.user.is_superuser
        return Response({'is_superuser': is_superuser})
    
    
class AdminListFile(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = FileSerializer
    def get(self, request):

        user_id = request.query_params.get('selected_user')
        
        if user_id:

            client_files = File.objects.filter(user_id=user_id)  
            cpa_files = File.objects.filter(for_user_id=user_id)

            client_serializer = FileSerializer(client_files, many=True)
            cpa_serializer = FileSerializer(cpa_files, many=True)

            return Response({
                "users": UserSerializer(User.objects.all(), many=True).data,
                "client_files": client_serializer.data,
                "cpa_files": cpa_serializer.data
            })
        
        else:
            files = File.objects.all()
            serializer = FileSerializer(files, many=True)  
            users_serializer = UserSerializer(User.objects.all(), many=True)    

            return Response({
                "users": users_serializer.data,
                "files": serializer.data
            })
    

 
    