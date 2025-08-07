#!/usr/bin/env python3
"""
VERONIKA AI - Simple Working Version
Fixed and ready to use!
"""

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import json

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini AI with the working API key
API_KEY = "AIzaSyAHDyynI_EveM7Aic2gVleGv9JBJebARNU"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

print("✅ VERONIKA AI initialized successfully!")
print(f"🔑 API Key: {API_KEY[:20]}...")
print("🤖 Model: Gemini 1.5 Flash")

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        # Get the message from the request
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Please enter a message!'})
        
        print(f"📨 User: {user_message}")
        
        # Generate AI response
        response = model.generate_content(user_message)
        ai_response = response.text
        
        print(f"🤖 VERONIKA: {ai_response[:100]}...")
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({'response': 'Sorry, I encountered an error. Please try again!'})

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'VERONIKA AI is running!',
        'model': 'Gemini 1.5 Flash',
        'working': True
    })

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 STARTING VERONIKA AI CHATBOT")
    print("="*60)
    print("📍 URL: http://127.0.0.1:5000")
    print("🌟 Ready to chat!")
    print("="*60)
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,  # Disable debug to avoid reload issues
        threaded=True
    )
