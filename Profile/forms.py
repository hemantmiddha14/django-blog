from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
    	model = Profile

    	fields = ['photo', 'phone_number', 'fav_post']
