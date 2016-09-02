from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import BlogPost
from .forms import BlogPostForm

def post_list(request):
	posts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
	post = get_object_or_404(BlogPost, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
	'''
	TODO:
	- check if user is logged in
	- disable new post button if user is not logged in
	'''
	if request.method == "POST":
		form = BlogPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = BlogPostForm()
	return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
	'''
	TODO:
	- check if user is logged in
	- disable new post button if user is not logged in
	'''
	post = get_object_or_404(BlogPost, pk=pk)
	if request.method == "POST":
		form = BlogPostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = BlogPostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form':form})