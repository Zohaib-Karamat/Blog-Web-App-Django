from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileForm, UserUpdateForm
from blog.models import Post


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'blog:home')
                return redirect(next_page)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog:home')


@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user)
    context = {
        'user_posts': user_posts,
        'total_posts': user_posts.count(),
        'published_posts': user_posts.filter(status='published').count(),
        'draft_posts': user_posts.filter(status='draft').count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def dashboard(request):
    if not request.user.profile.is_author:
        messages.error(request, 'You need to be an author to access the dashboard.')
        return redirect('blog:home')
    
    user_posts = Post.objects.filter(author=request.user)
    context = {
        'total_posts': user_posts.count(),
        'published_posts': user_posts.filter(status='published').count(),
        'draft_posts': user_posts.filter(status='draft').count(),
        'recent_posts': user_posts[:5],
    }
    return render(request, 'accounts/dashboard.html', context)

