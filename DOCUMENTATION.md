# CineMatch AI - Movie Recommendation System

## Overview

CineMatch AI is an intelligent movie recommendation platform built with Python and Streamlit. It uses content-based filtering and collaborative filtering techniques to provide personalized movie recommendations to users.

## Features

### 🎬 Core Features
- **AI-Powered Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **Hybrid Recommendations**: Combines content-based and collaborative filtering
- **User Authentication**: Secure login/signup system with session management
- **Personalized Dashboard**: User-specific movie recommendations and analytics
- **Movie Database**: Access to 4,803+ movies from TMDB dataset

### 👤 User Features
- **User Profiles**: Create and manage personal profiles
- **Movie Ratings**: Rate movies to improve recommendations
- **Watchlist**: Save movies to watch later
- **Favorites**: Mark favorite genres for personalized suggestions
- **Search History**: Track recently viewed movies

### 📊 Analytics Features
- **Rating Statistics**: View your average ratings and movie count
- **Genre Analysis**: Explore movies by genre preferences
- **Popular Movies**: Browse trending and featured movies
- **Movie Details**: Comprehensive movie information with external links

## Technology Stack

### Backend
- **Python 3.11**: Core programming language
- **Streamlit**: Web application framework for data science
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms

### Machine Learning
- **TF-IDF Vectorization**: Text feature extraction for movie metadata
- **Cosine Similarity**: Content similarity measurement
- **Content-Based Filtering**: Recommendation based on movie features
- **Collaborative Filtering**: Recommendation based on user ratings

### Data
- **TMDB 5000 Movies Dataset**: Movie metadata including:
  - Movie titles, overviews, genres
  - Cast and crew information
  - Keywords and tags
  - Ratings and popularity scores

## Installation

### Prerequisites
```bash
Python 3.11+
pip package manager
```

### Required Dependencies
```bash
pip install streamlit pandas numpy scikit-learn protobuf cryptography urllib3 certifi packaging
```

### Data Setup
1. Download the TMDB 5000 Movies dataset
2. Place `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in the project directory
3. Ensure files are in the correct location for the application to load

## Project Structure

```
Movie recommendation/
├── app.py                 # Main Streamlit application
├── recommender.py         # Recommendation engine logic
├── style.css             # Custom CSS styling
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── movie/                # Movie data folder
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
└── .streamlit/          # Streamlit configuration
    └── config.toml
```

## Running the Application

### Start the Server
```bash
python -m streamlit run app.py
```

### Access the Application
- **Local URL**: http://localhost:8501
- **Network URL**: http://10.83.19.179:8501 (accessible on local network)

## How It Works

### Recommendation Algorithm

1. **Data Loading**: Load and merge movie data from CSV files
2. **Data Preprocessing**:
   - Parse JSON columns (genres, keywords, cast, crew)
   - Extract features (overview, genres, cast, director, keywords)
   - Create a text "soup" combining all features

3. **TF-IDF Vectorization**:
   - Convert movie features into numerical vectors
   - Use TF-IDF to capture word importance

4. **Cosine Similarity**:
   - Calculate similarity between movie vectors
   - Generate recommendations based on highest similarity scores

5. **Hybrid Approach**:
   - Blend content-based scores with user ratings
   - Weight recommendations based on user preferences

### Authentication Flow

1. **Landing Page**: Full-screen login page with animated background
2. **Login/Signup**: Tab-based authentication interface
3. **Session Management**: Secure user sessions with state persistence
4. **Profile Management**: User-specific data storage and retrieval

## UI/UX Design

### Login Page
- **Dark Theme**: Modern black/gray color scheme
- **Animated Background**: Gradient animation effect
- **Responsive Layout**: Centered login form with tabs
- **Smooth Transitions**: CSS animations for enhanced UX

### Main Dashboard
- **Navigation**: Home, Discover, Recommendations, Analytics
- **Sidebar**: User profile, favorite genres, watchlist, ratings
- **Movie Cards**: Visual movie display with posters and ratings
- **Interactive Elements**: Buttons, sliders, and forms

## API Endpoints & External Links

### Movie Data Sources
- **TMDB API**: Movie posters and metadata
- **IMDb Search**: External movie information
- **YouTube Trailers**: Movie trailer search

### Generated Links
- Movie homepages (when available)
- IMDb search pages
- TMDB detail pages
- YouTube trailer searches

## Performance Optimization

### Caching
- **Data Loading**: `@st.cache_data` for movie database
- **Model Loading**: Cached similarity matrix computation
- **Session State**: Persistent user data across reruns

### Speed Improvements
- Removed artificial delays from loading functions
- Optimized data processing pipelines
- Efficient similarity matrix calculations

## User Data Management

### Session State Variables
- `logged_in_user`: Current authenticated user
- `user_profiles`: User account information
- `user_ratings`: Movie ratings by user
- `watchlist`: User's saved movies
- `recommendations_history`: Recently viewed movies

### Data Persistence
- User profiles stored in session state
- Ratings and watchlists saved per user
- Automatic data synchronization on logout

## Customization Options

### Styling
- **CSS Customization**: Modify `style.css` for visual changes
- **Color Themes**: Adjustable color schemes
- **Animations**: CSS animations for interactive elements

### Configuration
- **Genre Preferences**: Select favorite genres
- **Rating Thresholds**: Minimum rating filters
- **Language Preferences**: Filter by movie language

## Troubleshooting

### Common Issues

#### Module Not Found Errors
```bash
# Install missing dependencies
pip install [package-name]
```

#### Data Loading Errors
- Verify CSV files are in the correct location
- Check file permissions
- Ensure proper file encoding (UTF-8)

#### Port Conflicts
- Change default port: `streamlit run app.py --server.port 8502`
- Kill existing processes using port 8501

### Performance Issues
- Clear Streamlit cache: `streamlit cache clear`
- Restart the application
- Check system resources (RAM/CPU)

## Future Enhancements

### Planned Features
- [ ] Real-time movie database updates
- [ ] Social sharing of recommendations
- [ ] Advanced filtering options
- [ ] Mobile app version
- [ ] API for third-party integrations
- [ ] Machine learning model improvements
- [ ] User review and comment system

### Technical Improvements
- [ ] Database backend (PostgreSQL/MongoDB)
- [ ] User authentication with JWT tokens
- [ ] Cloud deployment (AWS/GCP)
- [ ] Containerization with Docker
- [ ] CI/CD pipeline setup

## Development Team

**Developer**: Sudheer  
**Contact**: [Your Email]  
**GitHub**: [Your GitHub Profile]

## License

This project is developed as a proof of concept for educational purposes.

## Acknowledgments

- **TMDB**: For providing the movie dataset
- **Streamlit**: For the excellent web framework
- **Scikit-learn**: For machine learning tools
- **Pandas**: For data manipulation capabilities

## Version History

### v1.0.0 - Initial Release
- Basic content-based recommendations
- User authentication system
- Movie rating and watchlist features

### v1.1.0 - UI Enhancements
- Colorful login page design
- Dark theme implementation
- Performance optimizations

### v1.2.0 - Future Release
- Planned hybrid recommendation improvements
- Database integration
- Cloud deployment

---

**Last Updated**: March 8, 2026  
**Status**: Active Development  
**Version**: 1.1.0
