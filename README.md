# 🎬 CineMatch AI - Advanced Movie Recommendation System

A sophisticated, AI-powered movie recommendation platform with beautiful animations, personalized recommendations, and intelligent features built with Streamlit and Google Gemini AI.

## ✨ Features

### 🎯 Core Features
- **Content-Based Recommendations**: Advanced TF-IDF and cosine similarity algorithms
- **Hybrid Recommendations**: Combines content-based and collaborative filtering
- **AI-Powered Analysis**: Google Gemini 2.5 Flash integration for intelligent insights
- **Beautiful UI/UX**: Modern animations, gradients, and responsive design
- **User Authentication**: Secure login/signup system with profile management
- **Watchlist Management**: Save and organize your favorite movies

### 🤖 AI Assistant Features
- **Movie Analysis**: Deep AI analysis of movies including themes and audience
- **Personalized Recommendations**: AI-curated suggestions based on your preferences
- **Movie Comparison**: Compare any two movies with AI insights
- **Mood-Based Recommendations**: Get movies based on your current mood
- **AI Chat Interface**: Interactive movie concierge with persistent chat history

### 🎨 Visual Features
- **Animated Backgrounds**: Dynamic gradient backgrounds with particle effects
- **Interactive Elements**: Hover effects, transitions, and micro-interactions
- **Responsive Design**: Perfectly optimized for desktop and mobile
- **Dark Theme**: Professional dark theme with vibrant accents
- **Movie Posters**: Automatic poster fetching from TMDB API

### 📊 Analytics & Insights
- **Movie Database**: 4,803 movies with comprehensive metadata
- **Visual Analytics**: Interactive charts and graphs
- **Genre Analysis**: Detailed genre statistics and trends
- **Rating Distribution**: Visual representation of movie ratings
- **Year Trends**: Movie release patterns over time

## � Technology Stack

### Backend
- **Python 3.11**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Scikit-learn**: Machine learning algorithms
- **Google Generative AI**: Gemini 2.5 Flash integration

### Frontend
- **HTML5/CSS3**: Modern web technologies
- **JavaScript**: Interactive animations and effects
- **Plotly**: Interactive data visualizations
- **CSS Animations**: Smooth transitions and effects

### Data Sources
- **TMDB API**: Movie posters and metadata
- **Kaggle TMDB Dataset**: 4,803 movies with rich features
- **IMDb Integration**: Additional movie information

## 📁 Dataset

### Required Files
- `tmdb_5000_movies.csv` – Movie metadata (title, overview, genres, keywords, etc.)
- `tmdb_5000_credits.csv` – Cast and crew information

### Movie Database Statistics
- **Total Movies**: 4,803
- **Time Period**: 1916 - 2017
- **Features**: 20+ columns including genres, keywords, budget, revenue
- **Languages**: Multiple languages with English dominance
- **Genres**: 20+ genre categories

### Popular Movies in Database
Avatar, Pirates of the Caribbean series, The Dark Knight Rises, Avengers series, 
Harry Potter, Spider-Man, Jurassic World, Star Trek, and many more blockbusters.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Git (for cloning)
- Internet connection (for API calls)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd "c:\Movie recomendation"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download Dataset
1. Visit [Kaggle TMDB Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
2. Download `tmdb_5000_movies.csv`
3. Place it in the project root directory

### Step 4: Run Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 🎮 User Guide

### Getting Started
1. **Login/Signup**: Create an account or login with existing credentials
2. **Explore Home**: View featured movies and dashboard statistics
3. **Discover Movies**: Browse and search the movie database
4. **Get Recommendations**: Select movies to get personalized suggestions
5. **Use AI Assistant**: Leverage AI for advanced movie insights

### Navigation
- **🏠 Home**: Dashboard with featured movies and statistics
- **🔍 Discover**: Browse and search the movie database
- **⭐ Recommendations**: Get personalized movie suggestions
- **📊 Analytics**: View detailed movie analytics and trends
- **🤖 AI Assistant**: Access AI-powered features

### Key Features Usage

#### Movie Recommendations
1. Navigate to **⭐ Recommendations**
2. Select a movie from dropdown or search
3. View side-by-side recommendation cards
4. Add movies to watchlist
5. Access quick links to IMDb, TMDB, and trailers

#### AI Assistant
1. Go to **🤖 AI Assistant**
2. Choose from 5 AI features:
   - **🎬 Movie Analysis**: Deep analysis of any movie
   - **🎯 Personalized Recs**: AI-curated recommendations
   - **⚖️ Movie Comparison**: Compare two movies
   - **😊 Mood-Based**: Get mood-specific suggestions
   - **💬 AI Chat**: Interactive movie concierge

#### Analytics Dashboard
1. Visit **📊 Analytics**
2. Explore different chart types:
   - Rating Distribution
   - Genre Analysis
   - Year Trends
3. Interactive visualizations with detailed insights

## 🧠 Algorithm Details

### Content-Based Filtering
1. **Feature Engineering**: Combine genres, keywords, overview, cast, crew
2. **TF-IDF Vectorization**: Convert text to numerical vectors
3. **Cosine Similarity**: Calculate similarity between movies
4. **Recommendation Generation**: Top 10 most similar movies

### Hybrid Approach
- **Content-Based**: Movie similarity using metadata
- **Collaborative**: User ratings and preferences
- **Weighted Combination**: Balanced recommendation strategy

### AI Integration
- **Google Gemini 2.5 Flash**: Advanced language model
- **Natural Language Processing**: Understand user preferences
- **Contextual Recommendations**: Mood and situation-based suggestions
- **Real-time Analysis**: Instant movie insights

## 🎨 UI/UX Features

### Animations & Effects
- **Floating Elements**: Smooth floating animations
- **Gradient Backgrounds**: Dynamic color transitions
- **Particle System**: Interactive background particles
- **Hover Effects**: Scale and glow on interaction
- **Slide-in Animations**: Staggered content appearance

### Responsive Design
- **Mobile Optimized**: Perfect on all screen sizes
- **Touch Friendly**: Large buttons and touch targets
- **Flexible Grid**: Adaptive layout system
- **Performance Optimized**: Smooth 60fps animations

### Accessibility
- **High Contrast**: Clear text and backgrounds
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: Semantic HTML structure
- **Color Blind Friendly**: Accessible color schemes

## 🔧 Configuration

### API Keys
- **Google Gemini**: Set `GEMINI_API_KEY` in `app.py`
- **TMDB API**: Optional for poster images

### Customization
- **Color Scheme**: Modify CSS gradients
- **Animation Speed**: Adjust timing variables
- **Layout**: Change column configurations
- **Features**: Enable/disable specific modules

## 📊 Performance

### Optimization Features
- **Caching**: Similarity matrix cached for fast startup
- **Lazy Loading**: Content loaded on demand
- **Image Optimization**: Compressed poster images
- **Database Indexing**: Fast movie lookups

### Metrics
- **Startup Time**: ~3-5 seconds
- **Recommendation Speed**: <1 second
- **Memory Usage**: ~500MB
- **API Response**: <2 seconds

## 🚀 Future Enhancements

### Planned Features
- **Real-time Collaborations**: Watch parties with friends
- **Social Features**: Share recommendations with friends
- **Advanced Filters**: Year, rating, genre filters
- **Export Features**: Save recommendations to PDF
- **Mobile App**: Native iOS/Android applications

### Technical Improvements
- **Machine Learning**: Advanced recommendation algorithms
- **Microservices**: Scalable architecture
- **Database Integration**: PostgreSQL/MongoDB
- **Cloud Deployment**: AWS/Azure hosting

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes with proper testing
4. Submit pull request

### Code Style
- **PEP 8**: Python style guidelines
- **Type Hints**: Function annotations
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit tests for all functions

## 📄 License

This project is developed as a proof of concept for educational purposes. Please ensure proper licensing for datasets and APIs used.

## 📞 Support

### Common Issues
- **Dataset Missing**: Download from Kaggle link
- **API Errors**: Check Gemini API key
- **Performance**: Clear cache and restart
- **Login Issues**: Check session storage

### Contact
For issues and suggestions, please create an issue in the repository.

---

## 🏆 Acknowledgments

- **TMDB**: For providing the movie dataset
- **Google**: For Gemini AI capabilities
- **Streamlit**: For the amazing web framework
- **Kaggle**: For hosting the dataset

---

**Developed with ❤️ using cutting-edge AI technologies and modern web development practices.**

*Version 2.0 - AI-Powered Movie Recommendation System*



