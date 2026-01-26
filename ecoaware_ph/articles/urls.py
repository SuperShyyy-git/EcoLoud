from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # Article List & Create
    path('', views.article_list, name='article_list'),
    path('create/', views.article_create, name='article_create'),
    
    # Category management (MUST be before article slug to avoid shadowing)
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<slug:slug>/edit/', views.category_edit, name='category_edit'),
    path('categories/<slug:slug>/delete/', views.category_delete, name='category_delete'),

    # Article Detail, Update, Delete (Catch-all for slugs)
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('<slug:slug>/edit/', views.article_update, name='article_update'),
    path('<slug:slug>/delete/', views.article_delete, name='article_delete'),

    # Comments
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
