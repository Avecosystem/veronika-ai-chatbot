# VERONIKA - BABE AI Chatbot

VERONIKA is a fully functional AI chatbot powered by Google's Gemini API. It features a stylish neon and black multi-color UI and provides quick, user-friendly responses to user queries.

## Features

- Modern UI with neon and black multi-color combination
- Integration with Google's Gemini API for intelligent responses
- User-friendly interface with edit, resend, and copy functionality
- Quick response times
- Easy deployment on web platforms like Netlify

## Prerequisites

- Python 3.7 or higher
- Flask
- Google Generative AI Python SDK

## Installation

1. Clone this repository or download the files

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. The API key is already included in the app.py file. If you want to use your own API key, replace the existing one in app.py:

```python
API_KEY = "YOUR_GEMINI_API_KEY"
```

## Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

## Deployment

To deploy this application on Netlify or other platforms:

1. Create a `netlify.toml` file with the following content:

```toml
[build]
  command = "pip install -r requirements.txt"
  publish = "."

[build.environment]
  PYTHON_VERSION = "3.9"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. Connect your repository to Netlify and follow their deployment instructions.

## Usage

1. Type your message in the input field
2. Click the "Send" button or press Enter
3. View the AI's response
4. Use the action buttons to:
   - Edit your last message
   - Resend your last message
   - Copy the AI's response

## License

© 2023 AV Ecosystem. All rights reserved.

## Credits

Powered by AV Ecosystem and Google's Gemini API.