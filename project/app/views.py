
from django.shortcuts import render, redirect
from .models import Document
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login, authenticate





def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect(login)
    return render(request,'register.html')
    
def login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  
            return redirect('view')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')




def logout(request):
    messages.success(request, 'Logout successful.')
    return redirect(login)





def add(req):
    if req.method == 'POST':
        title = req.POST.get('title')
        file = req.FILES.get('file')  
        user = req.user  
        if title and file:  
            Document.objects.create(user=user, title=title, file=file)
            return redirect(view)  
        else:
            return render(req, 'add.html', {'error': 'All fields are required.'})
    return render(req, 'add.html')

def view(req):
    user = req.user 
    documents = Document.objects.filter(user=user)  
    return render(req, 'view.html', {'documents': documents})



def edit(req, id):
    document = Document.objects.get(pk=id)
    if req.method == 'POST':
        title = req.POST.get('title')
        file = req.FILES.get('file')
        if title:
            document.title = title
        if file:
            document.file = file
        document.save()
        return redirect('view')  
    return render(req, 'edit.html', {'document': document})



def add(req):
    if req.method == 'POST':
        title = req.POST.get('title')
        file = req.FILES.get('file')  
        user = req.user  
        if title and file:  
            Document.objects.create(user=user, title=title, file=file)
            return redirect(view)  
        else:
            return render(req, 'add.html', {'error': 'All fields are required.'})
    return render(req, 'add.html')

def view(req):
    user = req.user 
    documents = Document.objects.filter(user=user)  
    return render(req, 'view.html', {'documents': documents})



def edit(req, id):
    document = Document.objects.get(pk=id)
    if req.method == 'POST':
        title = req.POST.get('title')
        file = req.FILES.get('file')
        if title:
            document.title = title
        if file:
            document.file = file
        document.save()
        return redirect('view')  
    return render(req, 'edit.html', {'document': document})



def delete(req, id):
    try:
        document = Document.objects.get(pk=id)
        document.delete()
    except Document.DoesNotExist:
        pass  
    
    return redirect('view') 