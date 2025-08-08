from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import time
import random
import json
import re
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the Gemini API with environment variables
# Get API keys from environment variables for security
API_KEY = os.getenv("GEMINI_API_KEY")
# Add the Google Gemini API key for fallback
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure with the primary API key only if it exists
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Warning: Failed to configure Gemini API: {e}")

# Define available models in order of preference (using newer, more compatible models)
AVAILABLE_MODELS = [
    'gemini-1.5-flash',             # Latest and fastest model
    'gemini-1.5-pro',               # More powerful model
    'models/gemini-1.0-pro',        # Stable fallback
    'claude-3-5-sonnet-20241022',   # Latest Claude model
    'claude-3-opus-20240229',       # Claude fallback
    'claude-3-haiku-20240307',      # Fast Claude model
]

# Initialize with the first model
CURRENT_MODEL_INDEX = 0
model = None

# Only initialize the Gemini model if API key exists and first model is Gemini
if API_KEY and not AVAILABLE_MODELS[CURRENT_MODEL_INDEX].startswith('claude'):
    try:
        model = genai.GenerativeModel(AVAILABLE_MODELS[CURRENT_MODEL_INDEX])
        print(f"Successfully initialized model: {AVAILABLE_MODELS[CURRENT_MODEL_INDEX]}")
    except Exception as e:
        print(f"Failed to initialize model {AVAILABLE_MODELS[CURRENT_MODEL_INDEX]}: {e}")
        model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Simple test endpoint to verify server connectivity"""
    return jsonify({
        'status': 'Server is running!',
        'method': request.method,
        'api_key_present': bool(API_KEY),
        'timestamp': time.time()
    })

def generate_with_retry(user_input, max_retries=3):
    """Generate content with retry logic and model fallback"""
    global CURRENT_MODEL_INDEX, model
    
    # Check if API key is available
    if not API_KEY:
        return {'success': False, 'error': 'No API key provided. Please set a valid API key in the environment variables or in the code.'}
    
    # Start with current model
    current_retry = 0
    base_wait_time = 2  # Base wait time in seconds
    
    while current_retry < max_retries:
        try:
            current_model_name = AVAILABLE_MODELS[CURRENT_MODEL_INDEX]
            
            # Check if it's a Claude model
            if current_model_name.startswith('claude'):
                # For Claude models, we need to use a different approach
                # This is a simplified example - in a real implementation, you would use the Claude API
                try:
                    import anthropic
                    claude_client = anthropic.Anthropic(api_key=API_KEY)
                    message = claude_client.messages.create(
                        model=current_model_name,
                        max_tokens=1000,
                        messages=[
                            {"role": "user", "content": user_input}
                        ]
                    )
                    return {'success': True, 'response': message.content[0].text}
                except Exception as claude_error:
                    print(f"Claude API error: {str(claude_error)}")
                    raise claude_error
            else:
                # For Gemini models, use the existing approach
                response = model.generate_content(user_input)
                return {'success': True, 'response': response.text}
        
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a rate limit error (429), invalid API key (400), or any other error that suggests we should try another model
            if "429" in error_str or "400" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower() or "api key not valid" in error_str.lower() or "api_key_invalid" in error_str.lower():
                # Try switching to a different model
                if CURRENT_MODEL_INDEX < len(AVAILABLE_MODELS) - 1:
                    CURRENT_MODEL_INDEX += 1
                    # If it's a Gemini model, update the model variable
                    if not AVAILABLE_MODELS[CURRENT_MODEL_INDEX].startswith('claude'):
                        model = genai.GenerativeModel(AVAILABLE_MODELS[CURRENT_MODEL_INDEX])
                    print(f"Switched to model: {AVAILABLE_MODELS[CURRENT_MODEL_INDEX]}")
                    continue  # Try again with new model
                
                # If we've tried all models, try using the Google API key for Gemini models if available
                if GOOGLE_API_KEY:
                    try:
                        print("Trying with Google API key...")
                        # Temporarily configure with Google API key
                        genai.configure(api_key=GOOGLE_API_KEY)
                        # Use gemini-1.0-pro with Google API key (more compatible)
                        google_model = genai.GenerativeModel('models/gemini-1.0-pro')
                        response = google_model.generate_content(user_input)
                        # Restore original API key
                        genai.configure(api_key=API_KEY)
                        return {'success': True, 'response': response.text}
                    except Exception as google_api_error:
                        print(f"Google API error: {str(google_api_error)}")
                        # Restore original API key
                        genai.configure(api_key=API_KEY)
                else:
                    print("No Google API fallback key available")
                
                # Implement exponential backoff
                wait_time = base_wait_time * (2 ** current_retry) + random.uniform(0, 1)
                print(f"Rate limit hit. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                # For non-rate-limit errors, return the error
                return {'success': False, 'error': error_str}
        
        current_retry += 1
    
    # If we've exhausted all retries
    return {'success': False, 'error': 'Maximum retries reached. Please try again later.'}

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
        
    except Exception as e:
        return jsonify({'response': f'Error processing request: {str(e)}'})
    
    # Use the retry function
    result = generate_with_retry(user_input)
    
    if result['success']:
        return jsonify({'response': result['response']})
    else:
        return jsonify({'response': f'Error: {result["error"]}'})
@app.route('/status', methods=['GET'])
def status():
    """Return the current model status and available models"""
    try:
        # Try to list available Gemini models
        gemini_models = []
        try:
            models = genai.list_models()
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    gemini_models.append(m.name)
        except Exception as e:
            gemini_models = ["Error listing Gemini models: " + str(e)]
        
        # Try to list available Claude models
        claude_models = []
        try:
            # In a real implementation, you would use the Claude API to list models
            # This is a simplified example
            claude_models = [
                'claude-3-opus-20240229',
                'claude-3-sonnet-20240229',
                'claude-3-haiku-20240307'
            ]
        except Exception as e:
            claude_models = ["Error listing Claude models: " + str(e)]
        
        # Check if Google API key is available as fallback
        has_google_fallback = GOOGLE_API_KEY is not None and GOOGLE_API_KEY != ""
        
        return jsonify({
            'current_model': AVAILABLE_MODELS[CURRENT_MODEL_INDEX],
            'available_models_configured': AVAILABLE_MODELS,
            'available_models_api': {
                'gemini': gemini_models,
                'claude': claude_models
            },
            'has_google_fallback': has_google_fallback,
            'fallback_model': 'gemini-1.0-pro (Google API)' if has_google_fallback else None
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Print initial model information
    print(f"Starting with model: {AVAILABLE_MODELS[CURRENT_MODEL_INDEX]}")
    print(f"Available models: {AVAILABLE_MODELS}")
    
    # Check API keys
    if not API_KEY:
        print("WARNING: No primary API key provided. The chatbot will not function correctly.")
        print("Please set a valid API key in the GEMINI_API_KEY environment variable or in the code.")
    
    print(f"Google API fallback available: {'Yes' if GOOGLE_API_KEY else 'No'}")
    if not GOOGLE_API_KEY:
        print("Note: No Google API fallback key provided. Fallback functionality will not be available.")
    
    app.run(debug=True)