from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the API key
API_KEY = os.getenv("GEMINI_API_KEY", "demo_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Simple test endpoint to verify server connectivity"""
    return jsonify({
        'status': 'Demo Server is running!',
        'method': request.method,
        'api_key_present': bool(API_KEY),
        'timestamp': time.time()
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        # Validate request data
        if not request.json:
            return jsonify({'response': 'Error: Invalid request format.'}), 400
        
        user_input = request.json.get('message', '')
        
        # Input validation
        if not user_input or not user_input.strip():
            return jsonify({'response': 'Please enter a message.'})
        
        # Limit input length to prevent abuse
        if len(user_input) > 2000:
            return jsonify({'response': 'Error: Message too long. Please limit to 2000 characters.'})
        
        # Basic sanitization
        user_input = user_input.strip()
        
        # Demo responses based on input
        responses = [
            f"Hello! I'm VERONIKA, your AI assistant. You said: '{user_input}'. How can I help you today?",
            f"Thanks for your message: '{user_input}'. I'm here to assist you with any questions!",
            f"I received your message: '{user_input}'. As VERONIKA AI, I'm ready to help with various tasks.",
            f"Great question about '{user_input}'! I'm VERONIKA, powered by the AV Ecosystem, and I'm here to help.",
            f"You asked about '{user_input}'. As an AI assistant, I can help you with information, analysis, and more!"
        ]
        
        # Add some intelligence to responses
        if "hello" in user_input.lower() or "hi" in user_input.lower():
            response_text = "Hello! I'm VERONIKA, your intelligent AI assistant powered by the AV Ecosystem. I'm here to help you with questions, provide information, assist with tasks, and have meaningful conversations. What would you like to know or discuss today?"
        elif "name" in user_input.lower():
            response_text = "My name is VERONIKA! I'm an advanced AI assistant created by the AV Ecosystem. I'm designed to be helpful, informative, and engaging. What can I help you with?"
        elif "help" in user_input.lower():
            response_text = "I'm here to help! I can assist you with:\n• Answering questions on various topics\n• Providing information and explanations\n• Helping with problem-solving\n• Creative writing and brainstorming\n• Technical support and guidance\n• General conversation and advice\n\nWhat specific area would you like help with?"
        elif "demo" in user_input.lower():
            response_text = "This is a demonstration version of VERONIKA AI. In the full version, I would be powered by Google's Gemini AI for even more intelligent responses. To activate the full version, you'll need to set up a valid Google Gemini API key. Would you like instructions on how to do that?"
        else:
            response_text = random.choice(responses)
        
        return jsonify({'response': response_text})
        
    except Exception as e:
        return jsonify({'response': f'Error processing request: {str(e)}'})

@app.route('/status', methods=['GET'])
def status():
    """Return the current demo status"""
    return jsonify({
        'current_model': 'VERONIKA Demo Mode',
        'status': 'Demo version running',
        'api_key_present': bool(API_KEY),
        'note': 'This is a demo version. For full AI capabilities, configure a valid Google Gemini API key.'
    })

if __name__ == '__main__':
    print("🚀 Starting VERONIKA AI Demo Server...")
    print("📍 Server will be available at: http://127.0.0.1:5000")
    print("💡 This is a demo version with simulated responses")
    print("🔑 To enable full AI, configure your Google Gemini API key in .env file")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
