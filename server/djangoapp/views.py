from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# إعداد الـ Logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"username": username}
    if user is not None:
        login(request, user)
        data = {"username": username, "status": "Authenticated"}
    return JsonResponse(data)

def logout_request(request):
    username = request.user.username
    logout(request)
    data = {"username": username, "status": "Successfully logged out"}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    user_exists = False
    try:
        User.objects.get(username=username)
        user_exists = True
    except:
        logger.debug("{} is new user".format(username))
    
    if not user_exists:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"username": username, "status": "Authenticated"})
    else:
        return JsonResponse({"username": username, "error": "Already Registered"})

def get_dealerships(request, state="All"):
    # محاكاة لجلب البيانات للروبوت
    dealers = [
        {"id": 1, "city": "New York", "state": "NY", "full_name": "Best Cars"},
        {"id": 3, "city": "Wichita", "state": "Kansas", "full_name": "Kansas Motors"}
    ]
    if state == "All":
        return JsonResponse(dealers, safe=False)
    else:
        filtered_dealers = [d for d in dealers if d['state'] == state]
        return JsonResponse(filtered_dealers, safe=False)

def get_dealer_details(request, dealer_id):
    # محاكاة لبيانات تاجر محدد
    dealer = {"id": dealer_id, "city": "New York", "full_name": "Best Cars Dealership"}
    return JsonResponse(dealer)

def get_dealer_reviews(request, dealer_id):
    # محاكاة للتقييمات
    reviews = [{"id": 1, "name": "John Doe", "review": "Great service!", "sentiment": "positive"}]
    return JsonResponse(reviews, safe=False)
def analyze_review_sentiments(text):
    # محاكاة لعملية تحليل المشاعر (Sentiment Analysis)
    # في المشروع الحقيقي يتم استدعاء Microservice خارجي
    positive_words = ['good', 'great', 'fantastic', 'excellent', 'amazing']
    negative_words = ['bad', 'poor', 'terrible', 'horrible', 'expensive']
    
    sentiment = "neutral"
    if any(word in text.lower() for word in positive_words):
        sentiment = "positive"
    elif any(word in text.lower() for word in negative_words):
        sentiment = "negative"
    
    return sentiment

def get_sentiment(request, review_text):
    # Endpoint لاستدعاء التحليل (للمهمة 16)
    sentiment = analyze_review_sentiments(review_text)
    return JsonResponse({"sentiment": sentiment})
