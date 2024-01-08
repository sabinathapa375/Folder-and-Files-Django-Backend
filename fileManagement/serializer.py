from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = File
        fields =  ['id','name', 'file_type', 'file', 'folder', 'created_at', 'user', 'for_user']
        depth = 1
        
class FolderSerializer(serializers.ModelSerializer):
    
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent_folder', 'files']




        

    # def validate_file_type(self, value):
    #     return value
     
    

        

    
    


