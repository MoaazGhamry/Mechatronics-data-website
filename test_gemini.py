
import os
import google.generativeai as genai

# Using the new key for verification
api_key = 'AIzaSyDovpPwE_CHzNtNO1sZszpbyM3_N04axCo'

print(f"Testing Gemini API with key: {api_key[:10]}...")
print("Attempting to use transport='rest' to bypass gRPC issues...")

try:
    # Note: In some versions transport is set in configure, in others in GenerativeModel
    genai.configure(api_key=api_key, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello world' if you can hear me.")
    print("SUCCESS!")
    print(f"Response: {response.text}")
except Exception as e:
    print("FAILED!")
    print(f"Error: {e}")
