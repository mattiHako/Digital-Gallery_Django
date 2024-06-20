from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.index, name='index'),
    path('mygallery/', views.mygallery, name="mygallery"),
    path('addimage/', views.addimage, name="addimage"),
    path('addimagefolder/<int:folder_id>/', views.addimagefolder, name="addimagefolder"),
    path('deleteimage/<int:image_id>/', views.deleteimage, name="deleteimage"),
    path('addfolder/', views.addfolder, name="addfolder"),
    path('myfolder/<int:folder_id>/', views.myfolder, name='myfolder'),
    path('deletefolder/<int:folder_id>/', views.deletefolder, name='deletefolder'),
    path('searchimages/', views.searchimages, name='searchimages'),
    path('editimage/<int:image_id>/', views.editimage, name="editimage"),
    path('editimage/<int:image_id>/<int:folder_id>/', views.foldereditimage, name='foldereditimage'),
    path('imagecarousel/', views.imagecarousel, name='imagecarousel')
]
