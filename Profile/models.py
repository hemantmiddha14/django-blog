from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from django.core.validators import RegexValidator

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	photo = models.ImageField(null=True, blank=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
	phone_number = models.CharField(validators=[phone_regex], max_length=12, null=True, blank=True)
	fav_post = models.ManyToManyField(Post, null=True, blank=True)

	def __str__(self):
		return "Profile of user {}".format(self.user.username)
