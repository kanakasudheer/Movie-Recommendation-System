# Environment Setup Guide

## 📋 Environment Variables Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Environment File
Create a `.env` file in the project root with your API keys:

```env
# Google Gemini AI API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: TMDB API Key for movie posters
TMDB_API_KEY=your_tmdb_api_key_here
```

### Step 3: Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key
5. Add it to your `.env` file

### Step 4: Verify Setup
Run the application to verify everything works:

```bash
streamlit run app.py
```

### 🔧 Troubleshooting

#### API Key Not Found
If you see "GEMINI_API_KEY not found" error:
1. Ensure `.env` file exists in project root
2. Check the API key is correctly formatted
3. Make sure there are no extra spaces or quotes

#### Encoding Issues
If you encounter encoding errors:
1. Delete and recreate the `.env` file
2. Use UTF-8 encoding without BOM
3. Ensure no special characters in the file

#### Dependencies Missing
If you see import errors:
```bash
pip install python-dotenv
```

### 📁 File Structure
```
c:\Movie recomendation\
├── .env                    # Your API keys (not tracked by Git)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
├── app.py                 # Main application
├── recommender.py         # Recommendation algorithms
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

### 🔒 Security Notes
- Never commit `.env` file to version control
- Use `.env.example` as a template for others
- Keep your API keys secure and private
- Consider using environment-specific keys for production

### 🚀 Quick Start
```bash
# Clone repository
git clone https://github.com/kanakasudheer/Movie-Recommendation-System.git
cd Movie-Recommendation-System

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the application
streamlit run app.py
```

Your CineMatch AI application is now ready! 🎬✨
