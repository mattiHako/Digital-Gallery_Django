from django import forms
from django.forms import ModelForm
from .models import Image, Folder

# Form for user
class ImageForm(ModelForm):
    
    class Meta:
        model = Image
        fields = ('image_title', 'description', 'image', 'folder')
        
        widgets = {
            'image_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'folder': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(ImageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(user=user)  # Filter folders by the user
            
            
class FolderImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ('image_title', 'description', 'image')

        widgets = {
            'image_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
            

        
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name',)
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class EditImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ('image_title', 'description')

        widgets = {
            'image_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }
