import streamlit as st
import pandas as pd
import numpy as np
from recommender import (
    load_data, clean_data, create_similarity, get_recommendations, hybrid_recommendations
)
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
import google.generativeai as genai

# Initialize Gemini AI
GEMINI_API_KEY = "AIzaSyAgLkdBzGflleYl5hnn-V1RpoydIbU0pAg"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

# Enhanced CSS with beautiful animations
st.markdown("""
<style>
/* Global animations and styles */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
    50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.8); }
}

@keyframes rainbow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

/* Animated background */
.stApp {
    background: linear-gradient(-45deg, #0a0a0a, #1a1a2e, #16213e, #0f3460, #533483) !important;
    background-size: 400% 400% !important;
    animation: gradientBG 20s ease infinite !important;
}

/* Enhanced header */
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border-radius: 20px;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    animation: float 6s ease-in-out infinite;
}

.movie-title {
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c) !important;
    background-size: 300% 300% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: rainbow 4s ease infinite !important;
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    text-shadow: 0 0 30px rgba(102, 126, 234, 0.5) !important;
}

.subtitle {
    color: #e2e8f0 !important;
    font-size: 1.2rem !important;
    animation: fadeInUp 1s ease-out;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
}

/* Navigation enhancements */
.nav-container {
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.4), rgba(26, 32, 44, 0.6)) !important;
    border-radius: 20px !important;
    border: 2px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3) !important;
    animation: slideInLeft 0.8s ease-out;
}

.nav-button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 1rem 1.2rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    text-align: center !important;
    position: relative !important;
    overflow: hidden !important;
}

.nav-button::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
    transition: left 0.5s !important;
}

.nav-button:hover::before {
    left: 100% !important;
}

.nav-button:hover {
    transform: translateY(-5px) scale(1.05) !important;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6) !important;
    background: linear-gradient(135deg, #764ba2, #667eea) !important;
}

/* Sidebar enhancements */
.sidebar-header {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    padding: 1.5rem !important;
    border-radius: 15px !important;
    margin-bottom: 1rem !important;
    text-align: center !important;
    animation: slideInRight 0.8s ease-out;
}

.sidebar-header h2 {
    color: white !important;
    margin: 0 !important;
    font-size: 1.3rem !important;
}

.sidebar-header p {
    color: rgba(255, 255, 255, 0.8) !important;
    margin: 0.5rem 0 0 0 !important;
    font-size: 0.9rem !important;
}

/* Metric cards with animations */
.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    padding: 1.5rem !important;
    border-radius: 15px !important;
    text-align: center !important;
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.metric-card::after {
    content: "" !important;
    position: absolute !important;
    top: -50% !important;
    left: -50% !important;
    width: 200% !important;
    height: 200% !important;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
    animation: shimmer 3s infinite !important;
}

.metric-card:hover {
    transform: translateY(-5px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.5) !important;
}

/* Movie cards with advanced animations */
.movie-card {
    background: linear-gradient(135deg, #2d3748, #1a202c) !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    transition: all 0.4s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.movie-card::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}

.movie-card:hover::before {
    opacity: 1 !important;
}

.movie-card:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4) !important;
    border-color: rgba(102, 126, 234, 0.5) !important;
}

/* Floating elements */
.floating {
    animation: float 6s ease-in-out infinite !important;
}

.pulse {
    animation: pulse 2s ease-in-out infinite !important;
}

.glow {
    animation: glow 2s ease-in-out infinite !important;
}

/* Enhanced buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.5) !important;
    background: linear-gradient(135deg, #764ba2, #667eea) !important;
}

/* Enhanced input fields */
.stTextInput > div > div > input {
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.9), rgba(26, 32, 44, 0.9)) !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.4) !important;
    background: rgba(45, 55, 72, 1) !important;
}

/* Enhanced selectbox */
.stSelectbox > div > div > select {
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.9), rgba(26, 32, 44, 0.9)) !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    color: white !important;
}

/* Enhanced tabs */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.8), rgba(26, 32, 44, 0.9)) !important;
    border-radius: 15px !important;
    padding: 0.5rem !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    color: white !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    transform: scale(1.05) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
}

/* Loading animations */
.loading-spinner {
    width: 50px !important;
    height: 50px !important;
    border: 4px solid rgba(255, 255, 255, 0.1) !important;
    border-top: 4px solid #667eea !important;
    border-radius: 50% !important;
    animation: spin 1s linear infinite !important;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Success and error messages */
.stSuccess {
    background: linear-gradient(135deg, #28a745, #20c997) !important;
    border-left: 4px solid #28a745 !important;
}

.stError {
    background: linear-gradient(135deg, #dc3545, #c82333) !important;
    border-left: 4px solid #dc3545 !important;
}

.stInfo {
    background: linear-gradient(135deg, #17a2b8, #138496) !important;
    border-left: 4px solid #17a2b8 !important;
}

/* Chart styling */
.js-plotly-plot {
    background: rgba(0, 0, 0, 0) !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .movie-title {
        font-size: 2.5rem !important;
    }
    
    .nav-container {
        padding: 1rem !important;
    }
    
    .nav-button {
        padding: 0.8rem 0.5rem !important;
        font-size: 0.85rem !important;
    }
}

/* Particle background enhancement */
.particle-bg {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    pointer-events: none !important;
    z-index: -1 !important;
}

.particle {
    position: absolute !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 50% !important;
    animation: float 20s infinite ease-in-out !important;
}
</style>
""", unsafe_allow_html=True)

# Create enhanced particle background
def create_particle_background():
    particles_html = """
    <div class="particle-bg" id="particles"></div>
    <script>
        function createParticles() {
            const container = document.getElementById('particles');
            const particleCount = 100;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                // Random size
                const size = Math.random() * 4 + 1;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                
                // Random position
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                
                // Random animation
                particle.style.animationDuration = (Math.random() * 20 + 10) + 's';
                particle.style.animationDelay = Math.random() * 20 + 's';
                
                // Random opacity
                particle.style.opacity = Math.random() * 0.5 + 0.1;
                
                // Random color
                const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4ecdc4'];
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                
                container.appendChild(particle);
            }
        }
        
        // Mouse interaction
        document.addEventListener('mousemove', (e) => {
            const particles = document.querySelectorAll('.particle');
            particles.forEach(particle => {
                const rect = particle.getBoundingClientRect();
                const distance = Math.sqrt(
                    Math.pow(e.clientX - (rect.left + rect.width / 2), 2) +
                    Math.pow(e.clientY - (rect.top + rect.height / 2), 2)
                );
                
                if (distance < 100) {
                    particle.style.transform = `scale(${2 - distance / 100})`;
                    particle.style.opacity = 1;
                } else {
                    particle.style.transform = 'scale(1)';
                    particle.style.opacity = particle.style.opacity || 0.5;
                }
            });
        });
        
        setTimeout(createParticles, 100);
    </script>
    """
    st.markdown(particles_html, unsafe_allow_html=True)

# Enhanced loading animation
def show_loading_animation():
    loading_html = """
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <div class="loading-spinner"></div>
    </div>
    """
    st.markdown(loading_html, unsafe_allow_html=True)

# cache to speed up
@st.cache_data(ttl=3600)
def load_model():
    with st.spinner("🎬 Loading movie database..."):
        df = load_data()
        df = clean_data(df)
        cosine_sim = create_similarity(df)
    return df, cosine_sim

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'recommendations_history' not in st.session_state:
    st.session_state.recommendations_history = []
# User profiles system
if 'user_profiles' not in st.session_state:
    st.session_state.user_profiles = {}
if 'current_profile' not in st.session_state:
    st.session_state.current_profile = None
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
# Authentication state
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'login'  # 'login' or 'signup'

# AI-Powered Functions
def get_ai_movie_analysis(movie_title, movie_data):
    """Get AI analysis of a movie"""
    try:
        prompt = f"""
        Analyze the movie "{movie_title}" with this information:
        - Overview: {movie_data.get('overview', 'No overview available')}
        - Genres: {movie_data.get('genres', 'Unknown')}
        - Rating: {movie_data.get('vote_average', 'N/A')}
        - Release Date: {movie_data.get('release_date', 'N/A')}
        
        Provide a brief analysis including:
        1. Main themes and mood
        2. Target audience
        3. Similar movie recommendations
        4. Fun facts or trivia
        Keep it concise and engaging.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Analysis temporarily unavailable: {str(e)}"

def get_ai_personalized_recommendations(user_ratings, user_preferences):
    """Get AI-powered personalized recommendations"""
    try:
        rated_movies = list(user_ratings.keys())[:5]  # Get top 5 rated movies
        preferences = user_preferences.get('favorite_genres', [])
        
        prompt = f"""
        Based on this user's movie preferences:
        - Highly rated movies: {', '.join(rated_movies)}
        - Favorite genres: {', '.join(preferences) if preferences else 'Not specified'}
        
        Suggest 5 movies they would love, considering:
        1. Similar themes to their highly rated movies
        2. Their preferred genres
        3. Mix of popular and hidden gems
        Format as a numbered list with brief reasons.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Recommendations temporarily unavailable: {str(e)}"

def get_ai_movie_comparison(movie1, movie2):
    """Compare two movies using AI"""
    try:
        prompt = f"""
        Compare these two movies:
        Movie 1: {movie1}
        Movie 2: {movie2}
        
        Provide a comparison covering:
        1. Which has better entertainment value
        2. Different target audiences
        3. Which to watch based on mood
        4. Key differences in style/theme
        Keep it balanced and helpful for decision making.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Comparison temporarily unavailable: {str(e)}"

def get_ai_mood_recommendations(mood):
    """Get movie recommendations based on mood"""
    try:
        prompt = f"""
        Suggest 5 perfect movies for someone feeling {mood}.
        Consider:
        1. Movies that match this emotional state
        2. Uplifting or comforting options if needed
        3. Different genres for variety
        4. Both popular and lesser-known choices
        Format as a numbered list with brief explanations.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Mood Recommendations temporarily unavailable: {str(e)}"
def show_login_page():
    """Display full-screen colorful login page"""
    # Hide sidebar and apply colorful background
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    .main-header {display: none !important;}
    
    /* Black dark theme login background */
    .stApp {
        background: linear-gradient(-45deg, #0a0a0a, #1a1a2e, #16213e, #0f3460) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 15s ease infinite !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Dark login card */
    .login-card {
        background: rgba(20, 20, 30, 0.95) !important;
        border-radius: 30px !important;
        padding: 3rem !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
    }
    
    /* White title */
    .animated-title {
        background: linear-gradient(45deg, #ffffff, #e0e0e0, #ffffff) !important;
        background-size: 300% 300% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: rainbow 3s ease infinite !important;
        font-weight: 800 !important;
    }
    
    @keyframes rainbow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Dark tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%) !important;
        border-radius: 20px !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #333333, #555555) !important;
        color: white !important;
        transform: scale(1.05) !important;
    }
    
    /* Dark input fields */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(30,30,40,0.95), rgba(20,20,30,0.9)) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
        background: rgba(40,40,50,1) !important;
    }
    
    /* White/Gray buttons */
    .stButton > button[kind="primaryFormSubmit"] {
        background: linear-gradient(45deg, #333333, #555555, #777777) !important;
        background-size: 200% 200% !important;
        animation: buttonGradient 3s ease infinite !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    @keyframes buttonGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton > button[kind="primaryFormSubmit"]:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Floating animation for elements */
    .float-element {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Glowing border effect */
    .glow-border {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5),
                    0 0 40px rgba(118, 75, 162, 0.3),
                    0 0 60px rgba(255, 107, 107, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form with colorful container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Animated colorful title
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;" class="float-element">
            <h1 class="animated-title" style="font-size: 3.5rem; margin-bottom: 0.5rem;">
                🎬 CineMatch AI
            </h1>
            <p style="font-size: 1.3rem; color: rgba(255,255,255,0.9); font-weight: 500; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                Your Personal Movie Recommendation System
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login/Signup tabs with colorful icons
        tab1, tab2 = st.tabs(["🔐 **LOGIN**", "📝 **SIGN UP**"])
        
        with tab1:
            st.markdown("""
            <h3 style='text-align: center; color: #ffffff; 
                       font-weight: 700; margin-bottom: 1.5rem;'>
                👋 Welcome Back!
            </h3>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    submitted = st.form_submit_button("� LOGIN", use_container_width=True)
                
                if submitted:
                    if not username or not password:
                        st.error("⚠️ Please enter both username and password")
                    elif username in st.session_state.user_profiles:
                        stored_user = st.session_state.user_profiles[username]
                        if stored_user.get('password') == password:
                            st.session_state.logged_in_user = username
                            st.session_state.current_profile = username
                            st.session_state.user_ratings = stored_user.get('ratings', {})
                            st.session_state.watchlist = stored_user.get('watchlist', [])
                            st.success(f"✅ Welcome back, {stored_user.get('name', username)}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password")
                    else:
                        st.error("❌ User not found. Please sign up first.")
        
        with tab2:
            st.markdown("""
            <h3 style='text-align: center; color: #ffffff; 
                       font-weight: 700; margin-bottom: 1.5rem;'>
                🎉 Create Your Account
            </h3>
            """, unsafe_allow_html=True)
            
            with st.form("signup_form"):
                new_username = st.text_input("👤 Choose Username", placeholder="Pick a unique username")
                new_name = st.text_input("✨ Full Name", placeholder="Enter your full name")
                new_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm your password")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    submitted = st.form_submit_button("✨ SIGN UP", use_container_width=True)
                
                if submitted:
                    if not new_username or not new_password or not new_name:
                        st.error("⚠️ Please fill in all fields")
                    elif new_username in st.session_state.user_profiles:
                        st.error("❌ Username already exists")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 4:
                        st.error("❌ Password must be at least 4 characters")
                    else:
                        # Create new user profile
                        st.session_state.user_profiles[new_username] = {
                            'name': new_name,
                            'password': new_password,
                            'avatar': random.choice(['🎭', '🎬', '🎪', '🎨', '🎸', '🎮', '🌟', '�', '💫', '🚀']),
                            'favorite_genres': [],
                            'watchlist': [],
                            'ratings': {},
                            'preferences': {
                                'language': 'All',
                                'min_rating': 5.0,
                                'duration': 'All'
                            }
                        }
                        st.session_state.logged_in_user = new_username
                        st.session_state.current_profile = new_username
                        st.success(f"🎉 Account created! Welcome, {new_name}!")
                        time.sleep(1)
                        st.rerun()
        
        # Colorful features showcase at bottom - black theme
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; 
                    background: rgba(20,20,30,0.9); border-radius: 20px;
                    backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);">
            <p style="color: #ffffff; margin: 0; font-size: 1.1rem; font-weight: 600;">
                🎬 Discover movies tailored just for you
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
                <span style="background: linear-gradient(45deg, #333333, #555555); padding: 0.5rem 1rem; 
                             border-radius: 20px; color: white; font-weight: 600; font-size: 0.85rem;">✨ AI-Powered</span>
                <span style="background: linear-gradient(45deg, #444444, #666666); padding: 0.5rem 1rem; 
                             border-radius: 20px; color: white; font-weight: 600; font-size: 0.85rem;">📊 Analytics</span>
                <span style="background: linear-gradient(45deg, #555555, #777777); padding: 0.5rem 1rem; 
                             border-radius: 20px; color: white; font-weight: 600; font-size: 0.85rem;">📝 Watchlist</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def logout():
    """Logout the current user"""
    # Save current user data
    if st.session_state.logged_in_user:
        st.session_state.user_profiles[st.session_state.logged_in_user]['ratings'] = st.session_state.user_ratings
        st.session_state.user_profiles[st.session_state.logged_in_user]['watchlist'] = st.session_state.watchlist
    
    st.session_state.logged_in_user = None
    st.session_state.current_profile = None
    st.session_state.user_ratings = {}
    st.session_state.watchlist = []
    st.session_state.page = 'home'
    st.rerun()


# Check if user is logged in
if st.session_state.logged_in_user is None:
    create_particle_background()
    show_login_page()
    st.stop()  # Stop execution here if not logged in

# User is logged in - continue with main app
# load once
try:
    movies_df, cosine_sim = load_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# Initialize session state for user ratings
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}

# Create background with animations
create_particle_background()

# Enhanced header with animation
st.markdown("""
<div class="main-header header-animation">
    <h1 class="movie-title">🎬 CineMatch AI</h1>
    <p class="subtitle">Discover Your Next Favorite Movie with AI-Powered Recommendations</p>
</div>
""", unsafe_allow_html=True)

# Navigation with proper layout and styling
st.markdown("""
<style>
.nav-container {
    margin: 1rem 0;
    padding: 1rem;
    background: rgba(45, 55, 72, 0.3);
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

.nav-button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    text-align: center !important;
}

.nav-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    background: linear-gradient(135deg, #764ba2, #667eea) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-container">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2])
with col1:
    if st.button("🏠 **Home**", key="nav_home", use_container_width=True):
        st.session_state.page = 'home'
with col2:
    if st.button("🔍 **Discover**", key="nav_discover", use_container_width=True):
        st.session_state.page = 'discover'
with col3:
    if st.button("⭐ **Recommendations**", key="nav_recs", use_container_width=True):
        st.session_state.page = 'recommendations'
with col4:
    if st.button("📊 **Analytics**", key="nav_analytics", use_container_width=True):
        st.session_state.page = 'analytics'
with col5:
    if st.button("🤖 **AI Assistant**", key="nav_ai", use_container_width=True):
        st.session_state.page = 'ai_assistant'

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    # User Profile Section
    current_user = st.session_state.user_profiles.get(st.session_state.logged_in_user, {})
    user_name = current_user.get('name', st.session_state.logged_in_user)
    user_avatar = current_user.get('avatar', '👤')
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{user_avatar}</div>
        <h3 style="color: white; margin: 0; font-size: 1.2rem;">{user_name}</h3>
        <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">@{st.session_state.logged_in_user}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sidebar-header">
        <h2>🎬 CineMatch AI</h2>
        <p>Movie Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Favorite Genres Management
    st.markdown("""
    <div class="sidebar-header">
        <h2>🎭 Favorite Genres</h2>
        <p>Personalize your recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Genre selection
    if 'genres' in movies_df.columns:
        all_genres = sorted(movies_df['genres'].dropna().unique())
        current_favorites = st.session_state.user_profiles[st.session_state.current_profile]['favorite_genres']
        
        selected_genres = st.multiselect(
            "Select your favorite genres:",
            options=all_genres,
            default=current_favorites,
            key="favorite_genres"
        )
        
        # Update profile if changed
        if selected_genres != current_favorites:
            st.session_state.user_profiles[st.session_state.current_profile]['favorite_genres'] = selected_genres
            st.success("🎭 Favorite genres updated!")
            st.rerun()
        
        # Display favorite genres
        if selected_genres:
            st.markdown("#### 🌟 Your Favorite Genres:")
            for genre in selected_genres:
                # Get genre stats
                genre_movies = movies_df[movies_df['genres'] == genre]
                avg_rating = genre_movies['vote_average'].mean() if 'vote_average' in genre_movies.columns else 0
                count = len(genre_movies)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                           color: white; padding: 0.8rem; border-radius: 10px; margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{genre}</strong>
                        <div style="text-align: right;">
                            <div style="font-size: 0.9rem;">⭐ {avg_rating:.1f}</div>
                            <div style="font-size: 0.8rem; opacity: 0.8;">{count} movies</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎭 Select your favorite genres to get personalized recommendations!")
    
    st.markdown("---")
    
    st.markdown("### 📊 Your Ratings")
    st.caption("Rate movies you've watched to get personalized recommendations")
    
    # Enhanced sidebar with better formatting (no debug info)
    st.markdown("""
    <div class="sidebar-header">
        <h2>🎯 Your Profile</h2>
        <p>Personalize your movie experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced ratings display with animations
    if st.session_state.user_ratings:
        st.markdown("""
        <div class="sidebar-header">
            <h2>📊 Your Ratings Summary</h2>
            <p>Track your movie preferences</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate statistics
        ratings_list = list(st.session_state.user_ratings.values())
        avg_rating = np.mean(ratings_list)
        total_ratings = len(ratings_list)
        
        # Animated metrics display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="animation: slideInLeft 0.6s ease-out;">
                <div style="font-size: 1.8rem; font-weight: bold; color: #667eea;">{total_ratings}</div>
                <div style="color: #b3b3b; font-size: 0.9rem;">Movies Rated</div>
            </div>
            <style>
            .metric-card {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 1.2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                transition: transform 0.3s ease;
            }}
            @keyframes slideInLeft {{
                from {{ opacity: 0; transform: translateX(-30px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            </style>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="animation: slideInRight 0.6s ease-out 0.2s;">
                <div style="font-size: 1.8rem; font-weight: bold; color: #4ecdc4;">{avg_rating:.1f}</div>
                <div style="color: #b3b3b; font-size: 0.9rem;">Average Rating</div>
            </div>
            <style>
            @keyframes slideInRight {{
                from {{ opacity: 0; transform: translateX(30px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            </style>
            """, unsafe_allow_html=True)
        
        # Animated ratings list
        st.markdown("#### 📈 Your Rated Movies:")
        for title, rating in sorted(st.session_state.user_ratings.items(), key=lambda x: x[1], reverse=True):
            stars = "⭐" * rating + "☆" * (5 - rating)
            st.markdown(f"""
            <div class="rating-item-animated" style="animation: fadeInUp 0.5s ease-out {len(st.session_state.user_ratings) * 0.1}s both;">
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.8rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 0.5rem;">
                    <div style="flex: 1;">
                        <strong style="color: #667eea; font-size: 0.9rem;">{title[:25]}{'...' if len(title) > 25 else ''}</strong>
                    </div>
                    <div style="flex: 1;">
                        <span style="font-size: 1.2rem; cursor: pointer;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">{stars}</span>
                    </div>
                </div>
                <div style="width: 100%; background: rgba(255,255,255,0.1); border-radius: 10px; height: 6px; margin-top: 5px;">
                    <div style="width: {rating*20}%; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
                </div>
            </div>
            <style>
            .rating-item-animated {{
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.5s ease;
            }}
            @keyframes fadeInUp {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            </style>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All Ratings"):
            st.session_state.user_ratings = {}
            st.success("🗑️ All ratings cleared!")
            time.sleep(1)
            st.rerun()
    else:
        st.markdown("""
        <div class="sidebar-header">
            <h2>📊 Your Ratings</h2>
            <p>Start rating movies to get personalized recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🎬 No ratings yet! Start rating movies to get personalized recommendations.")
    
    # Enhanced quick stats
    st.markdown("""
    <div class="sidebar-header">
        <h2>� Quick Stats</h2>
        <p>Your movie database overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    total_movies = len(movies_df)
    rated_percentage = (len(st.session_state.user_ratings) / total_movies) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #28a745, #20c997);">
            <div style="font-size: 1.5rem; font-weight: bold; color: white;">{total_movies:,}</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem;">Total Movies</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #dc3545, #c82333);">
            <div style="font-size: 1.5rem; font-weight: bold; color: white;">{rated_percentage:.1f}%</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem;">Rated</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Watchlist Management
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-header">
        <h2>📝 My Watchlist</h2>
        <p>Movies you want to watch</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add to watchlist
    with st.expander("➕ Add to Watchlist", expanded=False):
        movie_to_add = st.selectbox(
            "Select movie:",
            movies_df['title'].sort_values().unique(),
            key="watchlist_add"
        )
        if st.button("Add to Watchlist"):
            if movie_to_add not in st.session_state.watchlist:
                st.session_state.watchlist.append(movie_to_add)
                # Update current profile
                st.session_state.user_profiles[st.session_state.current_profile]['watchlist'] = st.session_state.watchlist
                st.success(f"✅ '{movie_to_add}' added to watchlist!")
                st.rerun()
            else:
                st.warning("⚠️ Movie already in watchlist!")
    
    # Display watchlist
    if st.session_state.watchlist:
        st.markdown(f"#### 📋 {len(st.session_state.watchlist)} Movies")
        
        for i, movie_title in enumerate(st.session_state.watchlist):
            col_movie, col_remove = st.columns([3, 1])
            with col_movie:
                st.markdown(f"🎬 **{movie_title}**")
            with col_remove:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.watchlist.remove(movie_title)
                    st.session_state.user_profiles[st.session_state.current_profile]['watchlist'] = st.session_state.watchlist
                    st.rerun()
    else:
        st.info("📝 Your watchlist is empty. Add movies to watch later!")
    
    # Enhanced recommendation history
    if st.session_state.recommendations_history:
        st.markdown("""
        <div class="sidebar-header">
            <h2>🕐 Recent Searches</h2>
            <p>Your movie exploration history</p>
        </div>
        """, unsafe_allow_html=True)
        
        for movie in st.session_state.recommendations_history[-5:]:
            st.markdown(f"""
            <div class="history-item" style="animation: slideIn 0.3s ease-out;">
                <button onclick="window.location.href='#recommendations'" style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 0.8rem 1rem;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                    width: 100%;
                    text-align: left;
                    font-size: 0.9rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
                ">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span>🎬 {movie[:20]}{'...' if len(movie) > 20 else ''}</span>
                        <span style="font-size: 0.8rem;">→</span>
                    </div>
                </button>
            </div>
            <style>
            .history-item {{
                opacity: 0;
                transform: translateY(10px);
                margin-bottom: 0.5rem;
            }}
            .history-item button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }}
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            </style>
            """, unsafe_allow_html=True)

# Page-based navigation with enhanced animations
if st.session_state.page == 'home':
    user_name = st.session_state.user_profiles.get(st.session_state.logged_in_user, {}).get('name', 'Movie Lover')
    
    # Animated welcome section
    st.markdown(f"""
    <div class="floating" style="text-align: center; padding: 2rem 0; animation: fadeInUp 1s ease-out;">
        <h2 style="font-size: 2.5rem; color: white; margin-bottom: 0.5rem; text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);">
            🏠 Welcome back, {user_name}!
        </h2>
        <p style="color: #e2e8f0; font-size: 1.2rem; animation: pulse 2s ease-in-out infinite;">
            ✨ Discover your next favorite movie
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Animated stats cards
    st.markdown("#### 📊 Your Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="animation: slideInLeft 0.6s ease-out;">
            <div style="font-size: 2rem; font-weight: bold;">{len(movies_df):,}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">🎬 Total Movies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rating = movies_df['vote_average'].mean() if 'vote_average' in movies_df.columns else 0
        st.markdown(f"""
        <div class="metric-card" style="animation: slideInLeft 0.8s ease-out 0.2s;">
            <div style="font-size: 2rem; font-weight: bold;">{avg_rating:.1f}/10</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">⭐ Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_genres = len(movies_df['genres'].unique()) if 'genres' in movies_df.columns else 0
        st.markdown(f"""
        <div class="metric-card" style="animation: slideInLeft 1s ease-out 0.4s;">
            <div style="font-size: 2rem; font-weight: bold;">{total_genres}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">🎭 Genres</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="animation: slideInLeft 1.2s ease-out 0.6s;">
            <div style="font-size: 2rem; font-weight: bold;">{len(st.session_state.user_ratings)}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">📊 Your Ratings</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Featured movies with enhanced animations
    st.markdown("#### 🌟 Featured Movies")
    featured_movies = movies_df.sample(6)
    cols = st.columns(3)
    
    for i, (idx, movie) in enumerate(featured_movies.iterrows()):
        with cols[i % 3]:
            # Get poster URL
            poster_url = ""
            if 'poster_path' in movie and pd.notna(movie['poster_path']) and movie['poster_path']:
                poster_url = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
            
            # Animated movie card
            st.markdown(f"""
            <div class="movie-card floating" style="animation: fadeInUp {0.8 + i * 0.2}s ease-out;">
            """, unsafe_allow_html=True)
            
            if poster_url:
                st.image(poster_url, use_container_width=True, caption=movie['title'])
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px;">
                    <h4 style="color: white; margin: 0;">{movie['title']}</h4>
                    <div style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">⭐ {movie.get('vote_average', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"**{movie['title']}**")
            st.markdown(f"⭐ {movie.get('vote_average', 'N/A')}")
            
            # Enhanced action buttons
            col_link1, col_link2 = st.columns(2)
            with col_link1:
                if st.button(f"🎬 Details", key=f"featured_{idx}", use_container_width=True):
                    st.session_state.selected_movie = movie['title']
                    st.session_state.page = 'recommendations'
                    st.rerun()
            with col_link2:
                if st.button(f"� Watchlist", key=f"watchlist_{idx}", use_container_width=True):
                    if movie['title'] not in st.session_state.watchlist:
                        st.session_state.watchlist.append(movie['title'])
                        st.success(f"✅ '{movie['title']}' added to watchlist!")
                    else:
                        st.warning(f"⚠️ '{movie['title']}' already in watchlist")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Popular genres with animated chart
    if 'genres' in movies_df.columns:
        st.markdown("#### 🎭 Popular Genres")
        genre_counts = movies_df['genres'].value_counts().head(10)
        
        fig = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            title="Top 10 Movie Genres",
            color=genre_counts.values,
            color_continuous_scale=['#667eea', '#764ba2', '#f093fb', '#f5576c']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=20,
            title_font_color='white',
            showlegend=False
        )
        
        # Animated chart container
        st.markdown('<div class="glow">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions section
    st.markdown("#### � Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Random Movie", use_container_width=True):
            random_movie = movies_df.sample(1).iloc[0]
            st.session_state.selected_movie = random_movie['title']
            st.session_state.page = 'recommendations'
            st.rerun()
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = 'analytics'
            st.rerun()
    
    with col3:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.page = 'ai_assistant'
            st.rerun()
    
    # Personalized recommendations teaser
    if st.session_state.user_ratings:
        st.markdown("#### � Based on Your Ratings")
        
        # Get top rated movies
        top_rated = sorted(st.session_state.user_ratings.items(), key=lambda x: x[1], reverse=True)[:3]
        
        if top_rated:
            st.markdown("Your highest rated movies:")
            for title, rating in top_rated:
                stars = "⭐" * rating
                st.markdown(f"• **{title}** {stars}")
            
            if st.button("🎬 Get Personalized Recommendations", use_container_width=True):
                st.session_state.page = 'ai_assistant'
                st.rerun()

elif st.session_state.page == 'discover':
    st.markdown("### 🔍 Discover Movies")
    
    # Simple search
    search_query = st.text_input(
        "🔍 Search movies...",
        placeholder="Enter movie title..."
    )
    
    # Apply search filter
    if search_query:
        filtered_movies = movies_df[
            movies_df['title'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_movies = movies_df
    
    # Display results
    st.markdown(f"#### 🎬 Found {len(filtered_movies)} Movies")
    
    if len(filtered_movies) == 0:
        st.warning("🔍 No movies found. Try a different search!")
    else:
        # Display in grid
        cols = st.columns(3)
        for i, (idx, movie) in enumerate(filtered_movies.head(12).iterrows()):
            with cols[i % 3]:
                # Get poster URL
                poster_url = ""
                if 'poster_path' in movie and pd.notna(movie['poster_path']) and movie['poster_path']:
                    poster_url = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
                
                if poster_url:
                    st.image(poster_url, use_container_width=True, caption=movie['title'])
                else:
                    st.markdown(f"""
                    <div class="movie-card">
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2);">
                            <h4 style="color: white; margin: 0;">{movie['title']}</h4>
                            <div class="rating">⭐ {movie.get('vote_average', 'N/A')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"**{movie['title']}**")
                st.markdown(f"⭐ {movie.get('vote_average', 'N/A')}")
                st.write(movie.get('overview', 'No overview available')[:100] + "...")
                
                # Add homepage link if available
                if 'homepage' in movie and pd.notna(movie['homepage']) and movie['homepage']:
                    st.markdown(f"🔗 [Visit Movie Page]({movie['homepage']})")
                else:
                    st.write("📽️ No homepage available")
                
                # Add IMDb link (create from title)
                imdb_title = movie['title'].replace(' ', '+').replace(':', '').replace(' ', '+')
                st.markdown(f"🎬 [IMDb Page](https://www.imdb.com/find?q={imdb_title})")
                
                # Add TMDB link
                if 'id' in movie:
                    st.markdown(f"🎭 [TMDB Details](https://www.themoviedb.org/movie/{movie['id']})")
                
                # Add trailer search link
                st.markdown(f"🎥 [Search Trailer](https://www.youtube.com/results?search_query={movie['title']}+trailer)")
                
                # Add inline recommendations for searched movie
                if search_query and search_query.lower() in movie['title'].lower():
                    st.markdown("---")
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #2d3748, #1a202c); 
                               padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); 
                               margin: 1rem 0;">
                        <h4 style="color: white; margin: 0; font-size: 1.1rem;">🎯 Recommendations for '{movie['title']}'</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("🤖 Finding similar movies..."):
                        if st.session_state.user_ratings:
                            recommendations = hybrid_recommendations(
                                movie['title'], movies_df, cosine_sim,
                                user_ratings=st.session_state.user_ratings
                            )
                        else:
                            recommendations = get_recommendations(movie['title'], movies_df, cosine_sim)
                    
                    if recommendations:
                        # Show top 3 recommendations inline with better alignment
                        st.markdown("""
                        <div style="margin: 1rem 0;">
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                        """, unsafe_allow_html=True)
                        
                        for j, rec_movie in enumerate(recommendations[:3]):
                            rec_data = movies_df[movies_df['title'] == rec_movie].iloc[0]
                            
                            # Get poster URL
                            rec_poster_url = ""
                            if 'poster_path' in rec_data and pd.notna(rec_data['poster_path']) and rec_data['poster_path']:
                                rec_poster_url = f"https://image.tmdb.org/t/p/w300{rec_data['poster_path']}"
                            
                            st.markdown(f"""
                            <div style="background: rgba(45, 55, 72, 0.8); border: 1px solid rgba(255,255,255,0.1); 
                                       border-radius: 10px; padding: 1rem; text-align: center;">
                            """, unsafe_allow_html=True)
                            
                            if rec_poster_url:
                                st.image(rec_poster_url, use_container_width=True, caption=rec_movie)
                            else:
                                st.markdown(f"""
                                <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #2d3748, #1a202c); 
                                           border-radius: 8px; margin-bottom: 0.5rem;">
                                    <h5 style="color: white; margin: 0; font-size: 0.9rem;">{rec_movie}</h5>
                                    <div style="color: #e2e8f0; font-size: 0.8rem; margin-top: 0.5rem;">⭐ {rec_data.get('vote_average', 'N/A')}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown(f"**{rec_movie}**")
                            st.markdown(f"⭐ {rec_data.get('vote_average', 'N/A')}")
                            
                            if st.button(f"View Details", key=f"inline_rec_{idx}_{j}", use_container_width=True):
                                st.session_state.selected_movie = rec_movie
                                st.session_state.page = 'recommendations'
                                st.rerun()
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.markdown("""
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("📌 No recommendations found for this movie")
                
                if st.button(f"Get Recommendations", key=f"disc_{idx}"):
                    st.session_state.selected_movie = movie['title']
                    st.session_state.page = 'recommendations'
                    st.rerun()
        st.markdown("#### 🎲 Random Movies")
        random_movies = movies_df.sample(6)
        cols = st.columns(3)
        for i, (idx, movie) in enumerate(random_movies.iterrows()):
            with cols[i % 3]:
                # Get poster URL
                poster_url = ""
                if 'poster_path' in movie and pd.notna(movie['poster_path']) and movie['poster_path']:
                    poster_url = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
                
                if poster_url:
                    st.image(poster_url, use_container_width=True, caption=movie['title'])
                else:
                    st.markdown(f"""
                    <div class="movie-card pulse">
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ff6b6b, #4ecdc4);">
                            <h4 style="color: white; margin: 0;">{movie['title']}</h4>
                            <div class="rating">⭐ {movie.get('vote_average', 'N/A')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"**{movie['title']}**")
                st.markdown(f"⭐ {movie.get('vote_average', 'N/A')}")

elif st.session_state.page == 'recommendations':
    # Animated header
    st.markdown("""
    <div class="floating" style="text-align: center; padding: 2rem 0; animation: fadeInUp 1s ease-out;">
        <h2 style="font-size: 2.5rem; color: white; margin-bottom: 0.5rem; text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);">
            ⭐ Movie Recommendations
        </h2>
        <p style="color: #e2e8f0; font-size: 1.2rem; animation: pulse 2s ease-in-out infinite;">
            🎬 Get personalized movie suggestions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Movie selection with enhanced styling
    st.markdown("#### 🎬 Select a Movie")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.selected_movie:
            selected = st.selectbox(
                "🎬 Choose a movie to get recommendations:",
                movies_df['title'].sort_values().unique(),
                index=list(movies_df['title'].sort_values().unique()).index(st.session_state.selected_movie) if st.session_state.selected_movie in movies_df['title'].values else 0
            )
        else:
            selected = st.selectbox(
                "🎬 Choose a movie to get recommendations:",
                movies_df['title'].sort_values().unique()
            )
    
    with col2:
        search_mode = st.radio(
            "🔍 Search Mode",
            ["📋 Dropdown", "🔍 Search"],
            horizontal=True
        )
        
        if search_mode == "🔍 Search":
            search_query = st.text_input("Search movies...")
            if search_query:
                search_results = movies_df[
                    movies_df['title'].str.contains(search_query, case=False, na=False)
                ]['title'].tolist()
                if search_results:
                    selected = st.selectbox("Results:", search_results)
                else:
                    st.warning("No movies found")
    
    if selected:
        # Add to history
        if selected not in st.session_state.recommendations_history:
            st.session_state.recommendations_history.append(selected)
        
        # Get recommendations with loading animation
        with st.spinner("🤖 AI is analyzing your preferences..."):
            time.sleep(1)  # Simulate processing
            
            if st.session_state.user_ratings:
                recommendations = hybrid_recommendations(
                    selected, movies_df, cosine_sim,
                    user_ratings=st.session_state.user_ratings
                )
                st.info("💡 Using your ratings to personalize recommendations")
            else:
                recommendations = get_recommendations(selected, movies_df, cosine_sim)
                st.info("📌 Content-based recommendations (rate movies for personalized results!)")
        
        if not recommendations:
            st.warning("⚠️ No recommendations found for this movie")
        else:
            # Success message with animation
            st.markdown(f"""
            <div class="glow" style="text-align: center; padding: 1rem; margin: 1rem 0;">
                <h3 style="color: white; margin: 0;">
                    🎯 Found {len(recommendations)} recommendations for '{selected}'
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display selected movie details with enhanced styling
            st.markdown("#### 🎬 Selected Movie")
            movie_data = movies_df[movies_df['title'] == selected].iloc[0]
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if 'poster_path' in movie_data and pd.notna(movie_data['poster_path']):
                    img_url = f"https://image.tmdb.org/t/p/w300{movie_data['poster_path']}"
                    st.image(img_url, use_container_width=True, caption=selected)
                else:
                    st.markdown(f"""
                    <div class="movie-card glow" style="text-align: center; padding: 2rem;">
                        <h3 style="color: white;">{selected}</h3>
                        <div style="color: #e2e8f0;">⭐ {movie_data.get('vote_average', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="movie-card" style="padding: 1.5rem;">
                    <h3 style="color: white; margin-top: 0;">{selected}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if 'overview' in movie_data and pd.notna(movie_data['overview']):
                    st.write(movie_data['overview'])
                
                # Movie info cards
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    if 'genres' in movie_data:
                        st.markdown(f"**🎭 Genres:** {movie_data['genres']}")
                    if 'release_date' in movie_data and pd.notna(movie_data['release_date']):
                        st.markdown(f"**📅 Release:** {movie_data['release_date']}")
                    if 'runtime' in movie_data and pd.notna(movie_data['runtime']):
                        st.markdown(f"**⏱️ Runtime:** {int(movie_data['runtime'])} min")
                
                with info_col2:
                    if 'vote_average' in movie_data:
                        st.markdown(f"**⭐ Rating:** {movie_data['vote_average']}/10")
                    if 'vote_count' in movie_data and pd.notna(movie_data['vote_count']):
                        st.markdown(f"**🗳️ Votes:** {int(movie_data['vote_count']):,}")
                    if 'budget' in movie_data and pd.notna(movie_data['budget']):
                        st.markdown(f"**💰 Budget:** ${movie_data['budget']:,}")
                
                # Enhanced links section
                st.markdown("#### 🎬 Movie Links")
                
                link_col1, link_col2 = st.columns(2)
                
                with link_col1:
                    # Official Homepage
                    if 'homepage' in movie_data and pd.notna(movie_data['homepage']) and movie_data['homepage']:
                        st.markdown(f"""
                        <div class="movie-card" style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;">
                            <h4 style="color: white; margin: 0; font-size: 1rem;">🌐 Official Website</h4>
                            <a href="{movie_data['homepage']}" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">
                                Visit Website
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # IMDb Link
                    imdb_title = movie_data['title'].replace(' ', '+').replace(':', '').replace(' ', '+')
                    st.markdown(f"""
                    <div class="movie-card" style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;">
                        <h4 style="color: white; margin: 0; font-size: 1rem;">🎬 IMDb Page</h4>
                        <a href="https://www.imdb.com/find?q={imdb_title}" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">
                            View on IMDb
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
                with link_col2:
                    # TMDB Details
                    if 'id' in movie_data:
                        st.markdown(f"""
                        <div class="movie-card" style="background: linear-gradient(135deg, #28a745, #20c997); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;">
                            <h4 style="color: white; margin: 0; font-size: 1rem;">🎭 TMDB Details</h4>
                            <a href="https://www.themoviedb.org/movie/{movie_data['id']}" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">
                                View on TMDB
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Trailer Search
                    st.markdown(f"""
                    <div class="movie-card" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;">
                        <h4 style="color: white; margin: 0; font-size: 1rem;">🎥 Watch Trailer</h4>
                        <a href="https://www.youtube.com/results?search_query={movie_data['title']}+trailer" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">
                            Search on YouTube
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display recommendations with side-by-side layout
            st.markdown("#### 🎯 Top Recommended Movies")
            
            # Calculate number of rows needed (3 movies per row)
            movies_per_row = 3
            num_rows = (len(recommendations) + movies_per_row - 1) // movies_per_row
            
            for row in range(num_rows):
                # Get movies for this row
                start_idx = row * movies_per_row
                end_idx = min(start_idx + movies_per_row, len(recommendations))
                row_movies = recommendations[start_idx:end_idx]
                
                # Create columns for this row
                cols = st.columns(movies_per_row)
                
                for col_idx, movie_title in enumerate(row_movies):
                    actual_idx = start_idx + col_idx
                    
                    with cols[col_idx]:
                        movie_data = movies_df[movies_df['title'] == movie_title].iloc[0]
                        
                        # Get poster URL
                        poster_url = ""
                        if 'poster_path' in movie_data and pd.notna(movie_data['poster_path']) and movie_data['poster_path']:
                            poster_url = f"https://image.tmdb.org/t/p/w300{movie_data['poster_path']}"
                        
                        # Animated movie card
                        st.markdown(f"""
                        <div class="movie-card glow floating" style="animation: fadeInUp {1 + actual_idx * 0.1}s ease-out; padding: 1.5rem; margin: 0.5rem 0;">
                            <h4 style="color: white; text-align: center; margin: 0 0 1rem 0;">
                                🏆 #{actual_idx + 1}
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Movie poster or placeholder
                        if poster_url:
                            st.image(poster_url, use_container_width=True, caption=f"#{actual_idx + 1} {movie_title}")
                        else:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; margin-bottom: 1rem;">
                                <h4 style="color: white; margin: 0;">#{actual_idx + 1}</h4>
                                <div style="color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-weight: bold;">{movie_title}</div>
                                <div style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">⭐ {movie_data.get('vote_average', 'N/A')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Movie title and basic info
                        st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 0.5rem;">
                            <h5 style="color: white; margin: 0;">{movie_title}</h5>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**⭐ {movie_data.get('vote_average', 'N/A')}/10**")
                        
                        # Movie genres (shortened)
                        if 'genres' in movie_data:
                            genres = movie_data['genres']
                            if len(genres) > 30:
                                genres = genres[:27] + "..."
                            st.markdown(f"🎭 {genres}")
                        
                        # Release year
                        if 'release_date' in movie_data and pd.notna(movie_data['release_date']):
                            year = movie_data['release_date'][:4]
                            st.markdown(f"📅 {year}")
                        
                        # Action buttons
                        button_col1, button_col2 = st.columns(2)
                        
                        with button_col1:
                            if st.button(f"🎬", key=f"rec_details_{actual_idx}", use_container_width=True, help="View Details"):
                                st.session_state.selected_movie = movie_title
                                st.rerun()
                        
                        with button_col2:
                            if st.button(f"📋", key=f"rec_watchlist_{actual_idx}", use_container_width=True, help="Add to Watchlist"):
                                if movie_title not in st.session_state.watchlist:
                                    st.session_state.watchlist.append(movie_title)
                                    st.success(f"✅ Added to watchlist!", icon="✅")
                                else:
                                    st.warning(f"⚠️ Already in watchlist", icon="⚠️")
                        
                        # Quick links (expandable)
                        with st.expander("🔗 Quick Links", expanded=False):
                            imdb_title = movie_data['title'].replace(' ', '+').replace(':', '').replace(' ', '+')
                            st.markdown(f"""
                            **🎬 Movie Links:**
                            - [🎭 TMDB Details](https://www.themoviedb.org/movie/{movie_data.get('id', '')})
                            - [🎬 IMDb Page](https://www.imdb.com/find?q={imdb_title})
                            - [🎥 Watch Trailer](https://www.youtube.com/results?search_query={movie_data['title']}+trailer)
                            """)
                        
                        # Close movie card
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # Add separator between rows (except last row)
                if row < num_rows - 1:
                    st.markdown("---")
                    st.markdown("")

elif st.session_state.page == 'analytics':
    st.markdown("### 📊 Movie Analytics")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Movies", f"{len(movies_df):,}", "🎬")
    with col2:
        if 'vote_average' in movies_df.columns:
            avg_rating = movies_df['vote_average'].mean()
            st.metric("Average Rating", f"{avg_rating:.2f}/10", "⭐")
    with col3:
        if 'vote_count' in movies_df.columns:
            total_votes = movies_df['vote_count'].sum()
            st.metric("Total Votes", f"{total_votes:,}", "🗳️")
    with col4:
        st.metric("Your Ratings", len(st.session_state.user_ratings), "📊")
    
    # Enhanced charts section (without rating patterns)
    st.markdown("#### 📈 Visualizations")
    
    chart_type = st.selectbox(
        "Select Chart:",
        ["Rating Distribution", "Genre Analysis", "Year Trends"]
    )
    
    if chart_type == "Rating Distribution":
        if 'vote_average' in movies_df.columns:
            fig = px.histogram(
                movies_df, 
                x='vote_average',
                nbins=20,
                title="Movie Rating Distribution",
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Genre Analysis":
        if 'genres' in movies_df.columns:
            genre_stats = movies_df.groupby('genres').agg({
                'vote_average': 'mean',
                'title': 'count'
            }).reset_index()
            genre_stats.columns = ['Genre', 'Avg Rating', 'Count']
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Average Rating by Genre', 'Movie Count by Genre'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            fig.add_trace(
                go.Bar(x=genre_stats['Genre'], y=genre_stats['Avg Rating'], name='Avg Rating'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=genre_stats['Genre'], y=genre_stats['Count'], name='Count'),
                row=1, col=2
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Year Trends":
        if 'release_date' in movies_df.columns:
            movies_df['year'] = pd.to_datetime(movies_df['release_date'], errors='coerce').dt.year
            year_stats = movies_df.groupby('year').size().reset_index(name='count')
            year_stats = year_stats.dropna()
            
            fig = px.line(
                year_stats,
                x='year',
                y='count',
                title="Movies Released by Year",
                color_discrete_sequence=['#4ecdc4']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # End of application

elif st.session_state.page == 'ai_assistant':
    st.markdown("### 🤖 AI Movie Assistant")
    
    # AI Feature Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎬 Movie Analysis", "🎯 Personalized Recs", "⚖️ Movie Comparison", "😊 Mood-Based", "💬 AI Chat"])
    
    with tab1:
        st.markdown("#### 🎬 AI Movie Analysis")
        
        selected_movie = st.selectbox("Select a movie to analyze:", movies_df['title'].sort_values().unique())
        
        if st.button("🔍 Analyze Movie", use_container_width=True):
            with st.spinner("🤖 AI is analyzing the movie..."):
                movie_data = movies_df[movies_df['title'] == selected_movie].iloc[0]
                analysis = get_ai_movie_analysis(selected_movie, movie_data)
                
                analysis_formatted = analysis.replace('\n', '<br>')
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2d3748, #1a202c); 
                           padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                    <h4 style="color: white; margin: 0 0 1rem 0;">🎬 {selected_movie}</h4>
                    <div style="color: #e2e8f0; line-height: 1.6;">
                        {analysis_formatted}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### 🎯 AI Personalized Recommendations")
        
        if st.button("🚀 Get My AI Recommendations", use_container_width=True):
            with st.spinner("🤖 AI is creating personalized recommendations..."):
                user_profile = st.session_state.user_profiles.get(st.session_state.current_profile, {})
                recommendations = get_ai_personalized_recommendations(st.session_state.user_ratings, user_profile)
                
                recommendations_formatted = recommendations.replace('\n', '<br>')
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                           padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                    <h4 style="color: white; margin: 0 0 1rem 0;">🎯 Your Personalized Picks</h4>
                    <div style="color: white; line-height: 1.6;">
                        {recommendations_formatted}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### ⚖️ AI Movie Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            movie1 = st.selectbox("First Movie:", movies_df['title'].sort_values().unique(), key="movie1")
        with col2:
            movie2 = st.selectbox("Second Movie:", movies_df['title'].sort_values().unique(), key="movie2")
        
        if st.button("⚖️ Compare Movies", use_container_width=True):
            with st.spinner("🤖 AI is comparing the movies..."):
                comparison = get_ai_movie_comparison(movie1, movie2)
                
                comparison_formatted = comparison.replace('\n', '<br>')
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4ecdc4, #44a08d); 
                           padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                    <h4 style="color: white; margin: 0 0 1rem 0;">⚖️ {movie1} vs {movie2}</h4>
                    <div style="color: white; line-height: 1.6;">
                        {comparison_formatted}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("#### 😊 Mood-Based Recommendations")
        
        moods = ["Happy", "Sad", "Excited", "Relaxed", "Stressed", "Romantic", "Adventurous", "Nostalgic"]
        selected_mood = st.selectbox("How are you feeling?", moods)
        
        if st.button("🎭 Get Mood Recommendations", use_container_width=True):
            with st.spinner("🤖 AI is finding perfect movies for your mood..."):
                mood_recs = get_ai_mood_recommendations(selected_mood)
                
                mood_recs_formatted = mood_recs.replace('\n', '<br>')
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); 
                           padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                    <h4 style="color: white; margin: 0 0 1rem 0;">😊 Movies for {selected_mood} Mood</h4>
                    <div style="color: white; line-height: 1.6;">
                        {mood_recs_formatted}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("#### 💬 AI Movie Chat")
        st.markdown("Ask me anything about movies! I'm your personal movie concierge.")
        
        # Initialize chat history
        if 'ai_chat_history' not in st.session_state:
            st.session_state.ai_chat_history = []
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.ai_chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="text-align: right; margin: 0.5rem 0;">
                        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                   color: white; padding: 0.8rem 1rem; border-radius: 10px; 
                                   display: inline-block; max-width: 70%;">
                            <div style="font-weight: bold;">👤 You:</div>
                            <div>{message['content']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: left; margin: 0.5rem 0;">
                        <div style="background: rgba(45, 55, 72, 0.8); 
                                   color: white; padding: 0.8rem 1rem; border-radius: 10px; 
                                   display: inline-block; max-width: 70%;">
                            <div style="font-weight: bold;">🤖 AI:</div>
                            <div>{message['content']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_message = st.text_input("Ask me about movies...", key="ai_chat_input")
        
        with col2:
            if st.button("📤 Send", key="send_ai_chat"):
                if user_message:
                    # Add user message
                    st.session_state.ai_chat_history.append({'role': 'user', 'content': user_message})
                    
                    # Get AI response
                    with st.spinner("🤖 Thinking..."):
                        try:
                            prompt = f"""
                            As a movie expert assistant, respond to this question: {user_message}
                            
                            Be helpful, knowledgeable, and engaging. If asking about specific movies,
                            provide insights about themes, recommendations, or interesting facts.
                            Keep responses concise but informative.
                            """
                            
                            response = gemini_model.generate_content(prompt)
                            ai_response = response.text
                            
                            # Add AI response
                            st.session_state.ai_chat_history.append({'role': 'assistant', 'content': ai_response})
                            
                        except Exception as e:
                            st.session_state.ai_chat_history.append({'role': 'assistant', 'content': f"Sorry, I'm having trouble responding right now: {str(e)}"})
                    
                    st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.ai_chat_history = []
            st.rerun()
        
        # Quick suggestions
        st.markdown("#### 💡 Quick Questions:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎬 Best sci-fi movies?"):
                st.session_state.ai_chat_history.append({'role': 'user', 'content': "What are the best sci-fi movies?"})
                st.rerun()
        
        with col2:
            if st.button("😂 Funny comedies?"):
                st.session_state.ai_chat_history.append({'role': 'user', 'content': "Can you recommend some really funny comedies?"})
                st.rerun()
        
        with col3:
            if st.button("❤️ Romantic movies?"):
                st.session_state.ai_chat_history.append({'role': 'user', 'content': "What are some good romantic movies?"})
                st.rerun()
