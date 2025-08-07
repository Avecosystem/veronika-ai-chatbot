from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure API Key - Use environment variable or fallback to working key
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAHDyynI_EveM7Aic2gVleGv9JBJebARNU")
print(f"🔑 Using API Key: {API_KEY[:20]}...")

# Configure Gemini
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    print("✅ Gemini AI configured successfully!")
except Exception as e:
    print(f"❌ Failed to configure Gemini: {e}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'api_configured': model is not None,
        'timestamp': time.time()
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get request data
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': 'Please provide a message'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'response': 'Please enter a valid message'})
        
        # Validate message length
        if len(user_message) > 1000:
            return jsonify({'response': 'Message too long. Please keep it under 1000 characters.'})
        
        # Generate AI response
        if not model:
            return jsonify({'response': 'AI service is currently unavailable. Please try again later.'})
        
        try:
            print(f"📨 Processing message: {user_message[:50]}...")
            response = model.generate_content(user_message)
            ai_response = response.text
            print(f"🤖 Generated response: {ai_response[:50]}...")
            
            return jsonify({'response': ai_response})
            
        except Exception as ai_error:
            print(f"❌ AI Generation Error: {ai_error}")
            error_msg = str(ai_error)
            
            if "quota" in error_msg.lower() or "429" in error_msg:
                return jsonify({'response': 'I\'m experiencing high demand right now. Please try again in a moment.'})
            elif "invalid" in error_msg.lower():
                return jsonify({'response': 'There\'s an issue with my configuration. Please contact support.'})
            else:
                return jsonify({'response': 'I\'m having trouble processing your request. Please try again.'})
    
    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({'response': 'Sorry, I encountered an error. Please try again.'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting VERONIKA AI Chatbot...")
    print("📍 Server URL: http://127.0.0.1:5000")
    print("🤖 AI Model: Gemini 1.5 Flash")
    print("=" * 50)
    
    if model:
        print("✅ All systems ready!")
    else:
        print("⚠️  Warning: AI model not initialized")
    
    try:
        app.run(
            debug=True,
            host='127.0.0.1',
            port=5000,
            threaded=True,
            use_reloader=False  # Prevent double initialization
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down VERONIKA AI...")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
