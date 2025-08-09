#!/usr/bin/env python3
"""
VERONIKA AI - Simple Working Version
Fixed and ready to use!
"""

print("LOADING MODIFIED SIMPLE_VERONIKA.PY FILE")

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import json

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')

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
    return app.send_static_file('index.html')

@app.route('/veronika_standalone.html')
def standalone():
    """Serve the standalone version"""
    return app.send_static_file('veronika_standalone.html')

@app.route('/go_live_veronika.html')
def go_live():
    """Serve the Go Live version"""
    return app.send_static_file('go_live_veronika.html')

@app.route('/index_go_live.html')
def index_go_live():
    """Serve the index Go Live version"""
    return app.send_static_file('index_go_live.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        # Get the message from the request
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        print("\n==== CHAT REQUEST RECEIVED =====")
        print(f"REQUEST DATA: {data}")
        
        # Debug logging to console only
        # No file logging to keep things simple
        
        if not user_message:
            return jsonify({'response': 'Please enter a message!'})
        
        print(f"📨 User: {user_message}")
        
        # Check for exact phrases - convert to lowercase for case-insensitive comparison
        user_message_lower = user_message.lower()
        print(f"📝 Lowercase message: {user_message_lower}")
        
        # Check for exact phrases
        if user_message_lower == "say yourself" or user_message_lower == "who are you" or user_message_lower == "introduce yourself":
            print("✅ Exact phrase match detected")
            return jsonify({'response': 'I am VERONIKA, an BABE AI chatbot powered by the AV Ecosystem. I am designed to be helpful and engaging.'})
        
        # Check for phrases contained in the message
        if "say yourself" in user_message_lower or "who are you" in user_message_lower or "introduce yourself" in user_message_lower:
            print("✅ Phrase contained in message detected")
            return jsonify({'response': 'I am VERONIKA, an BABE AI chatbot powered by the AV Ecosystem. I am designed to be helpful and engaging.'})
        
        print("❌ No special phrases detected, using AI response")
        
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
