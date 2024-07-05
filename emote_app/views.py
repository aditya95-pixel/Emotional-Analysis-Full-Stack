from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import pandas as pd
import joblib
from django.views.decorators.csrf import ensure_csrf_cookie
import numpy as np
import cv2
from deepface import DeepFace 
# Load the Keras model
pipe_lr = joblib.load(open("emote_app/emotion_classifier_pipe_lr.pkl", "rb"))
@csrf_exempt
def voice_analysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recognized_text = data.get('recognized_text', '')
            string=str(pipe_lr.predict([recognized_text]))
            string=string[2:]
            string=string[:-2]
            print(f"Recognized Emotion: {string}")
            return JsonResponse({'message': 'Text received','recognized_text': "You said "+recognized_text+" Analysis Result: "+string})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return render(request,'voice_analysis.html')

@csrf_exempt
def text_analysis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_text = data.get('user_text', '')
        # Process the text as needed
        string=str(pipe_lr.predict([user_text]))
        string=string[2:]
        string=string[:-2]
        print(f"This is the {string} in terminal")
        return JsonResponse({'message': 'Text received', 'text': string})
    return render(request, 'text_analysis.html')

@ensure_csrf_cookie
def image_analysis(request):
    return render(request, 'image_analysis.html')


def upload_image(request):
    if request.method == 'POST':
        # Handle the image upload logic here
        image_file = request.FILES.get('imageFile')
        if image_file:
            # Convert the uploaded image file to a format OpenCV can use
            nparr = np.fromstring(image_file.read(), np.uint8)
            img1 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Analyze the image using DeepFace library
            result = DeepFace.analyze(img1, actions=['emotion'])
            
            # Prepare response JSON with the analyzed emotion
            response_data = {
                'message': 'Image uploaded and analyzed successfully.',
                'emotion': result[0]['dominant_emotion']
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'No image file received.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def tools(request):
    return render(request, 'tools.html')
def terms_of_service(request):
    return render(request, 'terms_of_service.html')
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    # Your about view logic here
    return render(request, 'about.html')
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Create a new user
            user = User.objects.create_user(username=cd['username'], password=cd['password'])
            user.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    error_message = 'Disabled account'
            else:
                error_message = 'Invalid login'
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error_message})
