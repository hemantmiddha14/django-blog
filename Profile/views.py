from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm

@login_required
def edit_profile(request):
    form = ProfileEditForm()
    if request.method == "POST":
    	form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)

    	if form.is_valid():
    		form.save()
    	else:
    		form = ProfileEditForm(instance=request.user.profile)
    		return render(request, 'Profile/edit_profile.html', {'form': form})
    else:
    	return render(request, 'Profile/edit_profile.html', {'form': form})


