from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm


# =========================================================
# LIST ALL ARTICLES
# =========================================================
@login_required
def article_list(request):
    from .models import Article, Category
    
    # Get parameters
    category_slug = request.GET.get('category')
    
    # Base Query
    articles = Article.objects.all()
    
    # Filter by Category
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(articles, 9) # Show 9 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for the dropdown
    categories = Category.objects.all()
    
    context = {
        'articles': page_obj,  # Pass page_obj instead of all articles
        'categories': categories,
        'current_category': category_slug
    }
    return render(request, 'organisms/article_list.html', context)


# =========================================================
# CREATE NEW ARTICLE
# =========================================================
@login_required
def article_create(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)   # Don't save yet
            article.author = request.user       # Assign logged-in user
            article.save()                      # Save article
            form.save_m2m()                     # Save tags (ManyToMany)
            return redirect('articles:article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'organisms/article_form.html', {'form': form})


# =========================================================
# VIEW ARTICLE DETAIL
# =========================================================
@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.views += 1
    article.save(update_fields=['views'])

    # Comments Logic
    from .forms import CommentForm
    comments = article.comments.filter(is_active=True).order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('articles:article_detail', slug=article.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'organisms/article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    })


# =========================================================
# UPDATE ARTICLE
# =========================================================
@login_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug)

    # Optional: Restrict editing to the article’s author
    if article.author != request.user:
        return redirect('articles:article_detail', slug=article.slug)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'organisms/article_form.html', {'form': form})


# =========================================================
# DELETE ARTICLE
# =========================================================
@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)

    # Optional: Restrict deletion to the author
    if article.author != request.user:
        return redirect('articles:article_detail', slug=article.slug)

    if request.method == 'POST':
        article.delete()
        return redirect('articles:article_list')

    return render(request, 'organisms/article_confirm_delete.html', {'article': article})


# =========================================================
# CATEGORY MANAGEMENT
# =========================================================

@login_required
def category_list(request):
    """List all categories"""
    if not request.user.is_staff:
        return redirect('home')
    
    from .models import Category
    categories = Category.objects.all()
    return render(request, 'articles/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Create a new category"""
    if not request.user.is_staff:
        return redirect('home')
    
    from .forms import CategoryForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('articles:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'articles/category_form.html', {'form': form, 'action': 'Create'})


@login_required
def category_edit(request, slug):
    """Edit an existing category"""
    if not request.user.is_staff:
        return redirect('home')
    
    from .models import Category
    from .forms import CategoryForm
    from django.contrib import messages
    
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('articles:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'articles/category_form.html', {
        'form': form, 
        'action': 'Edit',
        'category': category
    })


@login_required
def category_delete(request, slug):
    """Delete a category"""
    if not request.user.is_staff:
        return redirect('home')
    
    from .models import Category
    from django.contrib import messages
    
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('articles:category_list')
    
    return render(request, 'articles/category_confirm_delete.html', {'category': category})


# =========================================================
# COMMENT DELETION
# =========================================================
@login_required
def comment_delete(request, pk):
    from .models import Comment
    comment = get_object_or_404(Comment, pk=pk)
    
    # Restrict deletion to the comment author
    if comment.author != request.user:
        return redirect('articles:article_detail', slug=comment.article.slug)
    
    if request.method == 'POST':
        slug = comment.article.slug
        comment.delete()
        return redirect('articles:article_detail', slug=slug)
    
    return redirect('articles:article_detail', slug=comment.article.slug)
