from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key and configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    print(f"✅ API Key configured: {API_KEY[:20]}...")
else:
    print("❌ No API key found")

# Initialize model
try:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    print("✅ Model initialized successfully")
except Exception as e:
    print(f"❌ Model initialization failed: {e}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({
        'status': 'Server running!',
        'api_key_present': bool(API_KEY),
        'model_initialized': model is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': 'Invalid request format'})
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'response': 'Please enter a message'})
        
        # Generate response using Gemini
        if model and API_KEY:
            try:
                response = model.generate_content(user_message)
                return jsonify({'response': response.text})
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    return jsonify({'response': 'Error: Invalid API key. Please check your Google Gemini API key.'})
                elif "quota" in error_msg.lower():
                    return jsonify({'response': 'Error: API quota exceeded. Please try again later.'})
                else:
                    return jsonify({'response': f'Error: {error_msg}'})
        else:
            return jsonify({'response': 'Error: AI model not properly configured'})
            
    except Exception as e:
        return jsonify({'response': f'Server error: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Starting VERONIKA AI Server...")
    print(f"📍 API Key present: {'Yes' if API_KEY else 'No'}")
    print(f"🤖 Model ready: {'Yes' if model else 'No'}")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
