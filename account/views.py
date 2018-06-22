from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            posts = Post.objects.filter(user=request.user)
            return render(request, 'blog/blog/post_list.html', {'albums': albums})
        else:
            return render(request, 'account/login.html', {'error_message': 'Invalid login'})
    return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'music/login.html', {'form': form})

def register(request):
    template_name = 'account/register.html'
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
    return render(request, self.template_name, {'form': form})

