from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment, Profile
from .forms import PostForm

# Feed page
@login_required(login_url='social_login')
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('social_feed')
    else:
        form = PostForm()

    return render(request, 'social/feed.html', {'posts': posts, 'form': form})

# Likes
@login_required(login_url='social_login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('social_feed')

# Comments
@login_required(login_url='social_login')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('social_feed')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure only the comment author (or post author) can delete it
    if comment.author == request.user or comment.post.author == request.user:
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'social_feed'))

@login_required(login_url='social_login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'social_feed'))

@login_required(login_url='social_login')
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    follower_profiles = Profile.objects.filter(following=profile_user)

    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    is_following = user_profile.following.filter(id=profile_user.id).exists()

    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'user_posts': user_posts,
        'followers': follower_profiles,
        'is_following': is_following
    })

@login_required(login_url='social_login')
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    if target_user != request.user:
        if user_profile.following.filter(id=target_user.id).exists():
            user_profile.following.remove(target_user)
        else:
            user_profile.following.add(target_user)

    return redirect('social_profile', username=username)

# Registration View
def social_register(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            error_message = "Username is already taken."
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('social_feed')

    return render(request, 'social/register.html', {'error_message': error_message})

def social_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('social_feed')
        else:
            error_message = "Invalid username or password."

    return render(request, 'social/login.html', {'error_message': error_message})

def social_logout(request):
    logout(request)
    return redirect('social_login')
