from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', null=True, blank=True, related_name='folder', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def file_upload_path(instance, filename):
    if instance.user.is_superuser:
        return 'cpa_files/{0}/{1}'.format(instance.for_user.username, filename)
    else:
        return 'client_files/{0}/{1}'.format(instance.user.username, filename)


class File(models.Model):
    File_Choices = [
        ('Contract', 'Contract'),
        ('Document', 'Document'),
    ]
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=200, choices=File_Choices)
    file = models.FileField(upload_to=file_upload_path, blank=True, null=True)
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cpa_files', null = True, blank = True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.file_type} (uploaded by {self.user.username})"
    