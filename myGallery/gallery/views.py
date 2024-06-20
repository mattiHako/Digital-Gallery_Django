# Django tutorialin versio

# from django.http import HttpResponse
# # Create your views here.


# def index(request):
#     return HttpResponse("Terve vaan!")

#---------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageForm, FolderForm, FolderImageForm, EditImageForm
from .models import Image, Folder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os
from django.conf import settings

from django.urls import reverse
# Create your views here.

@login_required
def deletefolder(request, folder_id):
    # Ensure the folder exists and belongs to the user making the request
    folder = get_object_or_404(Folder, pk=folder_id, user=request.user)
    
    # Perform the delete operation
    folder.delete()
    messages.success(request, "Folder deleted successfully!")
    
    # Redirect the user back to the gallery page
    return redirect('gallery:mygallery')

@login_required
def deleteimage(request, image_id):
    referer = request.META.get('HTTP_REFERER', None)
    image = get_object_or_404(Image, pk=image_id)
    if request.user == image.user:
        image_path = image.image.path
        thumbnail_path = image.thumbnail.path if image.thumbnail else None
        
        folder_id = image.folder.id if image.folder else None
        image.delete()
        messages.success(request, "Image deleted successfully!")
        
        if os.path.isfile(image_path):
            os.remove(image_path)
        # Delete thumbnail file from filesystem, if it exists
        if thumbnail_path and os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
        
        if referer and 'searchimages/' in referer:
            return redirect('gallery:mygallery')
        
        if folder_id:
            # If the image was in a folder, redirect to that folder's view
            return redirect(reverse('gallery:myfolder', args=[folder_id]))
        else:
            # If the image wasn't in a folder, redirect to the main gallery
            return redirect('gallery:mygallery')
    else:
        messages.success(request, ("Cannot delete this image!"))
        return redirect('gallery:mygallery')

def index(request):
    if request.user.is_authenticated:
        images_exist = Image.objects.filter(user=request.user).exists()
        msg = "Welcome to Your Gallery"
    else:
        images_exist = False
        msg = "Please log in to use your gallery"

    context = {
        'user': request.user,
        'images_exist': images_exist,
        'msg': msg
    }
    return render(request, 'gallery/index.html', context)

@login_required
def addfolder(request):
    submitted = False
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect(reverse('gallery:mygallery') + '?submitted=True')
    else:
        form = FolderForm()
    return render(request, 'gallery/mygallery.html', {'form': form, 'submitted': submitted})

@login_required
def addimage(request):
    submitted = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            if not form.cleaned_data.get('folder'):
                image.folder = None
                
            image.save()
                #return HttpResponseRedirect('/addimage?submitted=True')
            return redirect(reverse('gallery:addimage') + '?submitted=True')
    else:
        form = ImageForm(user=request.user)
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'gallery/addimage.html', {'form': form, 'submitted': submitted})


@login_required
def addimagefolder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)  # Ensures the folder exists and belongs to the user
    submitted = False
    if request.method == 'POST':
        form = FolderImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.folder = folder
            image.save()
            return redirect(reverse('gallery:myfolder', args=[folder_id]) + '?submitted=True')
    else:
        form = FolderImageForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'gallery/addimagefolder.html', {'form': form, 'folder': folder, 'submitted': submitted})


@login_required
def mygallery(request):
    images_without_folder = Image.objects.filter(user=request.user, folder__isnull=True).order_by('image_title')
    folders = Folder.objects.filter(user=request.user).order_by('name')
    
    folderform = FolderForm()

    return render(request, 'gallery/mygallery.html', {'images': images_without_folder, 'folders': folders, 'folderform': folderform})

@login_required
def myfolder(request, folder_id):
    folder = Folder.objects.get(id=folder_id, user=request.user)  # Ensure the folder belongs to the user
    images = Image.objects.filter(folder=folder).order_by('image_title')
    return render(request, 'gallery/myfolder.html', {'folder': folder, 'images': images})

@login_required
def searchimages(request):
    if request.method == 'POST':
        imagesearch = request.POST.get('imagesearch')
        images = Image.objects.filter(Q(image_title__icontains=imagesearch) | Q(description__icontains=imagesearch), user=request.user).order_by('image_title')
        
        return render(request, 'gallery/searchimages.html', {'imagesearch': imagesearch, 'images': images})
    else:
        return render(request, 'gallery/searchimages.html', {})
    

@login_required
def editimage(request, image_id):
    image = Image.objects.get(pk=image_id)
    form = EditImageForm(request.POST or None, instance=image)
    if form.is_valid():
        form.save()
        return redirect('gallery:mygallery')
    
    return render(request, 'gallery/editimage.html', {'image': image, 'form': form})


@login_required
def foldereditimage(request, image_id, folder_id):
    image = Image.objects.get(pk=image_id)
    folder = Folder.objects.get(pk=folder_id)
    form = EditImageForm(request.POST or None, instance=image)
    if form.is_valid():
        form.save()
        return redirect('gallery:myfolder', folder_id=folder_id)
    
    return render(request, 'gallery/editimage.html', {'image': image, 'form': form, 'folder': folder})

@login_required
def imagecarousel(request):
    images = Image.objects.filter(user=request.user).order_by('upload_date')
    return render(request, 'gallery/imagecarousel.html', {'images': images})

