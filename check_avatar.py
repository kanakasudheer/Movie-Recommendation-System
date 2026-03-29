import pandas as pd

# Load the movies data
try:
    movies_df = pd.read_csv('movie/tmdb_5000_movies.csv')
    print(f"Total movies: {len(movies_df)}")
    
    # Check if Avatar exists
    avatar_movies = movies_df[movies_df['title'].str.contains('avatar', case=False, na=False)]
    print(f"Movies with 'avatar' in title: {len(avatar_movies)}")
    
    if len(avatar_movies) > 0:
        print("\nAvatar movies found:")
        for idx, movie in avatar_movies.iterrows():
            print(f"- {movie['title']}")
    else:
        print("No movies found with 'avatar' in title")
        
        # Show some sample titles
        print("\nSample movie titles from database:")
        sample_titles = movies_df['title'].head(20).tolist()
        for title in sample_titles:
            print(f"- {title}")
            
    # Check exact match
    exact_avatar = movies_df[movies_df['title'] == 'Avatar']
    print(f"\nExact 'Avatar' matches: {len(exact_avatar)}")
    
except FileNotFoundError:
    print("Error: movie/tmdb_5000_movies.csv not found")
except Exception as e:
    print(f"Error: {e}")
