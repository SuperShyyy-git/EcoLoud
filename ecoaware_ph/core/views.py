from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    """Homepage view"""
    try:
        from articles.models import Article
        from campaigns.models import Campaign
        
        featured_articles = Article.objects.filter(status='published', is_featured=True)[:3]
        featured_campaigns = Campaign.objects.filter(is_active=True)[:3]
        recent_articles = Article.objects.filter(status='published')[:6]
        
        context = {
            'featured_articles': featured_articles,
            'featured_campaigns': featured_campaigns,
            'recent_articles': recent_articles,
        }
    except:
        context = {
            'featured_articles': [],
            'featured_campaigns': [],
            'recent_articles': [],
        }
    
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """User dashboard view."""
    return render(request, 'core/dashboard.html')

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # 1. Get API Key from environment
            import os
            from groq import Groq
            from dotenv import load_dotenv
            
            load_dotenv() # Load .env file
            
            api_key = os.getenv("GROQ_API_KEY")
            
            if not api_key:
                return JsonResponse({
                    'reply': "I'm ready for speed! ⚡ Just add the 'GROQ_API_KEY' to your .env file."
                })

            # 2. Configure Groq
            client = Groq(api_key=api_key)
            
            # 3. Create prompt with persona
            system_instruction = (
                "You are EcoBot, the friendly AI assistant for EcoAware PH. "
                "Your goal is to help users with environmental questions, recycling tips, and navigating the site. "
                "Keep answers concise, encouraging, and emoji-friendly."
            )
            
            # 4. Generate Response (Llama 3)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction,
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            bot_reply = chat_completion.choices[0].message.content
            
            return JsonResponse({'reply': bot_reply})
            
        except Exception as e:
            print(f"Chat Error: {e}") # Log to terminal
            # Keep debug error for now so user can report if this model fails too
            return JsonResponse({'reply': f"Debug Error: {str(e)}"}, status=200)
            
    return JsonResponse({'error': 'Invalid request'}, status=405)  

@login_required
def about(request):
    """About page view"""
    return render(request, 'pages/about.html')  

@login_required
def profile(request):
    """Profile page view"""
    return render(request, 'pages/profile.html')

@login_required
def my_campaigns(request):
    """My Campaigns page view"""
    return render(request, 'pages/my_campaigns.html')
