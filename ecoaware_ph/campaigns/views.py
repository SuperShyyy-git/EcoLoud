from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign
from .forms import CampaignForm

# List all campaigns
@login_required
def campaign_list(request):
    from django.utils import timezone
    now = timezone.now()
    
    # Split campaigns into active and archived
    active_campaigns = Campaign.objects.filter(end_date__gte=now).order_by('end_date')
    archived_campaigns = Campaign.objects.filter(end_date__lt=now).order_by('-end_date')
    
    is_admin = request.user.is_staff  # True if the user is admin
    return render(request, 'organisms/campaign_list.html', {
        'active_campaigns': active_campaigns,
        'archived_campaigns': archived_campaigns,
        'has_archived': archived_campaigns.exists(),
        'is_admin': is_admin
    })

# Campaign detail
@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    is_admin = request.user.is_staff
    
    # Get participants with current user first if applicable
    participants = list(campaign.participants.all())
    if request.user.is_authenticated and request.user in participants:
        participants.remove(request.user)
        participants.insert(0, request.user)
        
    return render(request, 'organisms/campaign_detail.html', {
        'campaign': campaign,
        'recent_participants': participants[:5],
        'is_admin': is_admin
    })

# Create a new campaign
@login_required
def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save()
            return redirect('campaigns:campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm()
    return render(request, 'organisms/campaign_form.html', {'form': form})

# Update an existing campaign
@login_required
def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaigns:campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'organisms/campaign_form.html', {'form': form})

# Delete a campaign
@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        campaign.delete()
        return redirect('campaigns:campaign_list')
    return render(request, 'organisms/campaign_confirm_delete.html', {'campaign': campaign})
    return render(request, 'organisms/campaign_confirm_delete.html', {'campaign': campaign})


# Suggest a campaign
@login_required
def campaign_suggest(request):
    from .forms import CampaignSuggestionForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = CampaignSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            messages.success(request, 'Thank you! Your campaign suggestion has been submitted for review.')
            return redirect('campaigns:campaign_list')
    else:
        form = CampaignSuggestionForm()
    
    return render(request, 'organisms/campaign_suggestion.html', {'form': form})


@login_required
def campaign_convert(request, suggestion_id):
    if not request.user.is_staff:
        return redirect('home')
        
    from .models import CampaignSuggestion
    from .forms import CampaignForm
    from django.contrib import messages
    
    suggestion = get_object_or_404(CampaignSuggestion, pk=suggestion_id)
    
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save()
            
            # Update suggestion status
            suggestion.status = 'APPROVED'
            suggestion.save()
            
            messages.success(request, f'Campaign "{campaign.title}" created from suggestion!')
            return redirect('users:admin_dashboard')
    else:
        # Pre-fill form with suggestion data
        initial_data = {
            'title': suggestion.title,
            'description': suggestion.description,
        }
        form = CampaignForm(initial=initial_data)
    
    return render(request, 'organisms/campaign_form.html', {
        'form': form, 
        'title': f'Convert Suggestion: {suggestion.title}'
    })

@login_required
def join_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        if request.user in campaign.participants.all():
            campaign.participants.remove(request.user)
            messages.success(request, f'You have left the campaign "{campaign.title}".')
        else:
            campaign.participants.add(request.user)
            messages.success(request, f'You have successfully joined the campaign "{campaign.title}"!')
            
    return redirect('campaigns:campaign_detail', pk=pk)

@login_required
def campaign_participants(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    participants = campaign.participants.all()
    return render(request, 'organisms/campaign_participants.html', {
        'campaign': campaign,
        'participants': participants
    })
