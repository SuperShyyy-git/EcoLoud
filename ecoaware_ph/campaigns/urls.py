from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.campaign_create, name='campaign_create'),
    path('<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('<int:pk>/edit/', views.campaign_update, name='campaign_update'),
    path('<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),
    
    # Suggestion
    path('suggest/', views.campaign_suggest, name='campaign_suggest'),
    path('suggestion/<int:suggestion_id>/convert/', views.campaign_convert, name='campaign_convert'),
]
