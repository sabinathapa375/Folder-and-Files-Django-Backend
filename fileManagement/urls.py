from django.urls import path, include
from .views import  *
urlpatterns = [
    path('folders/', FolderList.as_view(), name='folders'  ),
    path('files/', FileViewSet.as_view(), name='files'),
    path('is-superuser/',IsSuperuserView.as_view(), name = 'is-superuser'),
    path('users/', UserListView.as_view(), name = 'users'),
    path('files/<int:pk>/', FileViewSet.as_view(), name='file-delete'),
    path('admin-file-list/', AdminListFile.as_view(), name='admin-file-list'),
    
    
]

