from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib import messages
from blog.models import Post

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        # print("usermname________________________")
        # print(username)
        password = request.POST.get('password')
        # print("password++++++++++++++++++++++++++")
        # print(password)
        user = authenticate(username=username, password=password)
        # print("user+++++++++++++++++++++++++")
        # print(user)
        if user is not None :
            # print("in if +++++++++++++++++++++++++++++")
            login(request, user)
            # print("authenticated+++++++++++++++++++++++")
            print(request.user.is_authenticated())
            return redirect("post_list")
            # posts = Post.objects.filter(user=request.user)
            # return render(request, 'blog/post_list.html', {'posts': posts})
        else: 
            return render(request, 'account/login.html', {'error_message': '*Username or Password is incorrect'})
    return render(request, 'account/login.html')       

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    # return render(request, 'account/login.html', {'form': form})
    messages.success(request, 'You have been successfully logged out')
    return redirect('/')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'account/register.html', {'form': form})



