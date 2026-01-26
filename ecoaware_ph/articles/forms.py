from django import forms
from .models import Article, Category, Tag, Comment


# =========================================================
# ARTICLE FORM
# =========================================================
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # Author, slug, views, timestamps are excluded (set automatically)
        fields = ['title', 'content', 'excerpt', 'featured_image', 'category', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title',
            }),
            # CKEditor 5 will handle 'content' automatically — no need for Textarea widget
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary (optional)',
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


# =========================================================
# CATEGORY FORM
# =========================================================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description',
            }),
        }


# =========================================================
# TAG FORM
# =========================================================
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag name',
            }),
        }


# =========================================================
# COMMENT FORM
# =========================================================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Join the discussion...',
            }),
        }

