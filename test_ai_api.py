import os
import google.generativeai as genai

# Hardcoded key from settings.py
KEY = 'AIzaSyAdLnsPwpIuzVJPH2tvQoY0pbNRcKWWpBE'

def test_api():
    print(f"Testing API with Key: {KEY}")
    genai.configure(api_key=KEY)
    
    try:
        model = genai.GenerativeModel('models/gemini-pro')
        response = model.generate_content('Say hello')
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == '__main__':
    test_api()
