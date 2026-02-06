import google.generativeai as genai
import os

# Using the new key
KEY = 'AIzaSyB_IY-37z4RFkP1kt1r974rk5JxSPbgi5k'

def check_key():
    print(f"Checking API Key: {KEY[:5]}...")
    genai.configure(api_key=KEY)
    try:
        model = genai.GenerativeModel('models/gemini-pro')
        response = model.generate_content("Are you working?")
        print(f"SUCCESS: API responded: {response.text}")
    except Exception as e:
        print(f"FAILURE: API Error: {e}")

if __name__ == "__main__":
    check_key()
