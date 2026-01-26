from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse

# ------------------------
# AUTHENTICATION VIEWS
# ------------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            messages.success(request, f'Account created for {username}!')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('users:user_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('users:login')


# ------------------------
# DASHBOARDS
# ------------------------

@login_required
def user_dashboard(request):
    try:
        from articles.models import Article
        from campaigns.models import Campaign
        
        # Get user's articles
        user_articles = Article.objects.filter(author=request.user).order_by('-created_at')[:5]
        total_articles = Article.objects.filter(author=request.user).count()
        
        context = {
            'user_articles': user_articles,
            'total_articles': total_articles,
            'total_views': sum(article.views for article in Article.objects.filter(author=request.user)),
            'impact_points': sum(article.views for article in Article.objects.filter(author=request.user)) + total_articles,
        }
    except:
        context = {}
    
    return render(request, 'users/dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('users:access_denied')
    
    try:
        from articles.models import Article
        from campaigns.models import Campaign, CampaignSuggestion
        
        context = {
            'total_users': User.objects.count(),
            'total_articles': Article.objects.count(),
            'total_campaigns': Campaign.objects.count(),
            'admin_users': User.objects.filter(is_staff=True).count(),
            'recent_articles': Article.objects.order_by('-created_at')[:5],
            'recent_campaigns': Campaign.objects.order_by('-created_at')[:5],
            'recent_users': User.objects.order_by('-date_joined')[:5],
            'suggestions': CampaignSuggestion.objects.order_by('-created_at')[:10],
        }
    except:
        context = {}
        
    return render(request, 'users/admin_dashboard.html', context)


# ------------------------
# USER MANAGEMENT (ADMIN)
# ------------------------

@login_required
def user_list(request):
    if not request.user.is_staff:
        return redirect('users:access_denied')
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_edit(request, user_id):
    if not request.user.is_staff:
        return redirect('users:access_denied')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'{user.username} updated successfully.')
            return redirect('users:user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'user_obj': user})


@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_staff:
        return redirect('users:access_denied')
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.info(request, f"{user.username}'s status updated.")
    return redirect('users:user_list')


@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('users:access_denied')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'{user.username} has been deleted.')
        return redirect('users:user_list')
    return render(request, 'users/user_confirm_delete.html', {'user_obj': user})


# ------------------------
# USER PROFILE
# ------------------------

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # Calculate stats
    try:
        from articles.models import Article
        user_articles_qs = Article.objects.filter(author=profile_user)
        total_articles = user_articles_qs.count()
        # Sum views, defaulting to 0 if no articles
        total_views = sum(a.views for a in user_articles_qs)
        impact_points = total_views + total_articles
    except Exception:
        total_articles = 0
        impact_points = 0
        
    context = {
        'profile_user': profile_user,
        'total_articles': total_articles,
        'impact_points': impact_points,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    from .forms import UserUpdateForm
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:user_profile', username=request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})


# ------------------------
# ACCESS DENIED PAGE
# ------------------------

def access_denied(request):
    context = {
        'user_list_url': reverse('users:user_list'),
        'admin_dashboard_url': reverse('users:admin_dashboard'),
        'user_dashboard_url': reverse('users:user_dashboard'),
        'login_url': reverse('users:login'),
    }
    return render(request, 'users/access_denied.html', context)