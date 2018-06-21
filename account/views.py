from django.shortcuts import render, redirect
from django.contib.auth import authenticate, login
from .forms import UserForm


def register(request):
    template_name = 'account/registeration_form.html'
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
    return render(request, self.template_name{'form': form})
