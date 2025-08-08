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
        
        print("\n==== CHAT REQUEST RECEIVED =====")
        print(f"REQUEST DATA: {data}")
        
        # Write to a debug log file
        try:
            with open('debug_log.txt', 'a') as f:
                f.write(f"\n==== CHAT REQUEST RECEIVED =====\n")
                f.write(f"REQUEST DATA: {data}\n")
        except Exception as log_error:
            print(f"Debug log error: {str(log_error)}")
        
        if not user_message:
            return jsonify({'response': 'Please enter a message!'})
        
        print(f"📨 User: {user_message}")
        
        # Write to debug log
        try:
            with open('debug_log.txt', 'a') as f:
                f.write(f"📨 User: {user_message}\n")
        except Exception as log_error:
            print(f"Debug log error: {str(log_error)}")
        
        # Check for exact phrases - convert to lowercase for case-insensitive comparison
        user_message_lower = user_message.lower()
        print(f"📝 Lowercase message: {user_message_lower}")
        
        # Write to debug log
        try:
            with open('debug_log.txt', 'a') as f:
                f.write(f"📝 Lowercase message: {user_message_lower}\n")
        except Exception as log_error:
            print(f"Debug log error: {str(log_error)}")
        
        # Check for exact phrases
        if user_message_lower == "say yourself" or user_message_lower == "who are you" or user_message_lower == "introduce yourself":
            print("✅ Exact phrase match detected")
            try:
                with open('debug_log.txt', 'a') as f:
                    f.write("✅ Exact phrase match detected\n")
            except Exception as log_error:
                print(f"Debug log error: {str(log_error)}")
            return jsonify({'response': 'I am VERONIKA, an BABE AI chatbot powered by the AV Ecosystem. I am designed to be helpful and engaging.'})
        
        # Check for phrases contained in the message
        if "say yourself" in user_message_lower or "who are you" in user_message_lower or "introduce yourself" in user_message_lower:
            print("✅ Phrase contained in message detected")
            try:
                with open('debug_log.txt', 'a') as f:
                    f.write("✅ Phrase contained in message detected\n")
            except Exception as log_error:
                print(f"Debug log error: {str(log_error)}")
            return jsonify({'response': 'I am VERONIKA, an BABE AI chatbot powered by the AV Ecosystem. I am designed to be helpful and engaging.'})
        
        print("❌ No special phrases detected, using AI response")
        try:
            with open('debug_log.txt', 'a') as f:
                f.write("❌ No special phrases detected, using AI response\n")
        except Exception as log_error:
            print(f"Debug log error: {str(log_error)}")
        
        # Generate AI response
        response = model.generate_content(user_message)
        ai_response = response.text
        
        print(f"🤖 VERONIKA: {ai_response[:100]}...")
        try:
            with open('debug_log.txt', 'a') as f:
                f.write(f"🤖 VERONIKA: {ai_response[:100]}...\n")
        except Exception as log_error:
            print(f"Debug log error: {str(log_error)}")
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        try:
            with open('debug_log.txt', 'a') as f:
                f.write(f"❌ {error_msg}\n")
        except Exception:
            pass  # Already logged the error
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
