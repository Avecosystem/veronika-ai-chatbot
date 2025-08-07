# 🔑 API Key Setup Guide for VERONIKA AI

## Quick Setup Steps

### 1. Get Your Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Set Up Your Environment
1. Open the `.env` file in your project folder
2. Replace `your_actual_api_key_here` with your real API key:
   ```
   GEMINI_API_KEY=your_copied_api_key_here
   ```
3. Save the file

### 3. Optional: Set Up Fallback Key
For better reliability, you can add a second API key:
```
GOOGLE_API_KEY=your_second_api_key_here
```

## Advanced Setup (Optional)

### Claude API (Optional)
If you want to use Claude models:
1. Go to [Anthropic Console](https://console.anthropic.com/keys)
2. Create an account and get an API key
3. Add to your `.env` file:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   ```

## Troubleshooting

### ❌ "API key not valid" Error
- Double-check your API key is correct
- Make sure there are no extra spaces
- Verify the key hasn't expired

### ❌ "Quota exceeded" Error
- Check your Google AI Studio usage limits
- Consider upgrading your plan
- Use the fallback key if configured

### ❌ Application won't start
- Make sure Python 3.7+ is installed
- Run: `pip install -r requirements.txt`
- Check that all dependencies are installed

## Security Notes
- Never commit your `.env` file to version control
- Keep your API keys private
- Rotate keys regularly for security

## Need Help?
If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is working at [Google AI Studio](https://aistudio.google.com)
3. Make sure all dependencies are installed correctly
