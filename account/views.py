from django.shortcuts import render, redirect
from django.contib.auth import authenticate, login
from .forms import UserForm



class UserFormView(View):
    form_class = UserForm
    template_name = 'account/registeration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name{'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_Data['username']
            password = form.cleaned_Data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, self.template_name{'form': form})
