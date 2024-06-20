from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def userlogin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('gallery:index')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ('Invalid username or password'))
            return redirect('sitemembers:userlogin')
    else:
        return render(request, 'auth/userlogin.html', {})

def userlogout(request):
    logout(request)
    messages.success(request, ('Logged out successfully!'))
    return redirect('gallery:index')

def registeruser(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Your account has been created!'))
            return redirect('gallery:index')
    else:
        form = RegisterUserForm()
        
        
    return render(request, 'auth/registeruser.html', {'form': form,})
