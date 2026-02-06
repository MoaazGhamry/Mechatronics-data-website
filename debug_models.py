
import google.generativeai as genai
import os

# Hardcoding the key from settings.py for the test script to ensure we test the exact same credential
API_KEY = 'AIzaSyAdLnsPwpIuzVJPH2tvQoY0pbNRcKWWpBE'

print(f"Checking models with key: {API_KEY[:5]}...{API_KEY[-5:]}")

try:
    genai.configure(api_key=API_KEY)
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
