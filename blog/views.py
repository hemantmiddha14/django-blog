from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib import messages


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    if request.method=="POST":
        query = request.POST.get("search", None)
        if query:
            posts = posts.filter(title__icontains=query)
        else:
            messages.error(request, "No matching Results")
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
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
