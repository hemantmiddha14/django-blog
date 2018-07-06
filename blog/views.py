from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Post, Images
from Profile.models import Profile
from .forms import PostForm
from django.contrib import messages
from django.forms import modelformset_factory
import json

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	pro_obj = Profile.objects.get(user=request.user)
	if request.method=="POST":
		query = request.POST.get("search", None)
		if query:
			posts = posts.filter(title__icontains=query)
		else:
			messages.error(request, "No matching Results")
	return render(request, 'blog/post_list.html', {'posts': posts, "pro_obj":pro_obj})

def add_or_remove_favorite(request):
	response = {"status": False, "errors": []}
	if request.is_ajax() and request.POST['action'] == 'create_favorite':
		post_id = request.POST['id']
		post = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=request.user)
		profile.fav_post.add(post)
		profile.save()

	if request.is_ajax() and request.POST['action'] == 'remove_favorite':
		post_id = request.POST['id']
		post = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=request.user)
		profile.fav_post.remove(post)
		profile.save()

	response["status"] = True
	response["id"] = post_id
	return HttpResponse(json.dumps(response))

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    ImageFormset = modelformset_factory(Images, fields=('image',))
    if request.method == "POST":
        form = PostForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid() :
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            for f in formset:
                try:
                    photo = Images(post=post, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        formset = ImageFormset(queryset = Images.objects.none())
    return render(request, 'blog/post_edit.html', {'form': form, 'formset': formset})


def post_edit(request, pk):
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        ImageFormset = modelformset_factory(Images, fields=('image',))
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                data = Images.objects.filter(post=post)
                for index, f in enumerate(formset):
                    if f.cleaned_data:
                        if f.cleaned_data['id'] is None:
                            photo = Images(post=post, image=f.cleaned_data.get('image'))
                            photo.save()

                        elif f.cleaned_data['image'] is False:
                            photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                            photo.delete()
                        else:
                            photo = Images(post=post, image=f.cleaned_data.get('image'))
                            d = Images.objects.get(id=data[index].id)
                            d.image = photo.image
                            d.save()

                return redirect('post_detail', pk=post.pk)

        else:
            form = PostForm(instance=post)
            formset = ImageFormset(queryset = Images.objects.filter(post=post))
        return render(request, 'blog/post_edit.html', {'form': form, 'formset': formset, 'post':post})
    else:
        return redirect('/')



def post_del(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("/")




def search(request):
    post_name =  request.GET.get('search')
    if post_name:
        if request.method == 'GET':
            status = Post.objects.filter(title__icontains=post_name)
    else:
         status = Post.objects.all()
         # messages.error(request, "No matching Results")


    return render(request, 'blog/post_list.html', {'post': status})
