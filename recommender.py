"""Helper module for building a content-based and hybrid recommender system.

Expected files:
 - movie/tmdb_5000_movies.csv (contains title, overview, genres, keywords, etc.)
 - movie/tmdb_5000_credits.csv (contains cast/crew information)

If the movies file is missing the system will raise an informative error.
"""

import os
import ast
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import StandardScaler


MOVIES_CSV = os.path.join(os.path.dirname(__file__), "movie", "tmdb_5000_movies.csv")
CREDITS_CSV = os.path.join(os.path.dirname(__file__), "movie", "tmdb_5000_credits.csv")


def load_data(movies_path: str = MOVIES_CSV, credits_path: str = CREDITS_CSV) -> pd.DataFrame:
    """Load and merge the movie and credits datasets."""
    if not os.path.exists(movies_path):
        raise FileNotFoundError(
            f"movies file not found at {movies_path}.\n"
            "Please download `tmdb_5000_movies.csv` (from Kaggle or similar) "
            "and place it in the movie/ directory alongside the credits file."
        )
    if not os.path.exists(credits_path):
        raise FileNotFoundError(
            f"credits file not found at {credits_path}."
        )

    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # the credits file also has a "title" column which duplicates
    # the movie title from the movies dataframe; drop it to avoid
    # pandas adding suffixes when we merge below.
    if 'title' in credits.columns:
        credits = credits.drop(columns=['title'])

    # merge on movie_id (the credits file uses movie_id, the movies dataset uses id)
    if 'movie_id' in credits.columns and 'id' in movies.columns:
        credits = credits.rename(columns={'movie_id': 'id'})
    df = movies.merge(credits, on='id')
    return df


def _parse_json_list(x):
    """Parse a column containing a JSON-formatted list and return the list of names."""
    try:
        data = ast.literal_eval(x)
    except (ValueError, SyntaxError):
        return []
    if isinstance(data, list):
        return [item.get('name', '') for item in data if isinstance(item, dict)]
    return []


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the combined dataframe and create a `soup` of text features."""
    # genres and keywords may already be parsed in some versions of the dataset
    for col in ['genres', 'keywords', 'cast', 'crew']:
        if col in df.columns:
            df[col] = df[col].fillna('[]').astype(str).apply(_parse_json_list)

    # keep only top 3 cast members (ordered by appearance)
    if 'cast' in df.columns:
        df['cast'] = df['cast'].apply(lambda x: x[:3])

    # keep director only from crew
    if 'crew' in df.columns:
        df['crew'] = df['crew'].apply(lambda x: [name for name in x if 'Director' in name or 'director' in name])

    # convert lists to space-separated strings for TF-IDF
    for col in ['genres', 'keywords', 'cast', 'crew']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
        else:
            df[col] = ''

    # make sure overview exists
    if 'overview' not in df.columns:
        df['overview'] = ''

    # create soup feature
    df['soup'] = (
        df['overview'].fillna('') + ' ' +
        df['genres'] + ' ' +
        df['keywords'] + ' ' +
        df['cast'] + ' ' +
        df['crew']
    )
    return df


def create_similarity(df: pd.DataFrame):
    """Compute TF-IDF matrix and cosine similarity for the soup feature."""
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['soup'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def get_recommendations(title: str, df: pd.DataFrame, cosine_sim) -> list:
    """Return a list of recommended movie titles for the given title."""
    if title not in df['title'].values:
        return []
    idx = df.index[df['title'] == title][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # skip the first one (itself)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()


if __name__ == '__main__':
    # quick smoke test
    df = load_data()
    df = clean_data(df)
    cosine_sim = create_similarity(df)
    print(get_recommendations(df['title'].iloc[0], df, cosine_sim))


def build_user_ratings_matrix(ratings_dict, movies_df):
    """Build a user-movie ratings matrix from a dict of {movie_title: rating}.
    
    Returns a Series indexed by movie title with the ratings provided.
    """
    ratings = pd.Series(dtype=float)
    for title, rating in ratings_dict.items():
        if title in movies_df['title'].values:
            ratings[title] = float(rating)
    return ratings


def hybrid_recommendations(title, movies_df, cosine_sim, user_ratings=None, 
                          content_weight=0.5, collaborative_weight=0.5):
    """Return hybrid recommendations blending content-based + collaborative signals.
    
    Args:
        title: movie to get recommendations for
        movies_df: dataframe with movie info
        cosine_sim: content similarity matrix
        user_ratings: dict of {movie_title: rating} from current user
        content_weight: weight for content-based similarity (0-1)
        collaborative_weight: weight for collaborative signal (0-1)
    
    Returns:
        list of top 10 recommended movie titles
    """
    # Get base content recommendations
    content_recs = get_recommendations(title, movies_df, cosine_sim)
    
    if user_ratings is None or len(user_ratings) == 0:
        # No user ratings yet, just return content recs
        return content_recs
    
    # Get user preferences vector from ratings
    rated_titles = list(user_ratings.keys())
    rated_movies = movies_df[movies_df['title'].isin(rated_titles)].copy()
    
    if len(rated_movies) == 0:
        return content_recs
    
    # Find movies similar to user's rated favorites
    collaborative_scores = {}
    for idx, row in movies_df.iterrows():
        movie_title = row['title']
        if movie_title == title or movie_title in rated_titles:
            continue
        
        # Average similarity to movies user rated highly
        similarities = []
        for rated_title in rated_titles:
            if rated_title in movies_df['title'].values:
                rated_idx = movies_df[movies_df['title'] == rated_title].index[0]
                sim = cosine_sim[idx][rated_idx]
                rating = user_ratings[rated_title]
                # Weight similarity by user rating
                similarities.append(sim * (rating / 5.0))
        
        if similarities:
            collaborative_scores[movie_title] = np.mean(similarities)
    
    # Blend content + collaborative scores
    hybrid_scores = {}
    for rec in content_recs:
        content_score = 1.0 / (content_recs.index(rec) + 1)  # decay by rank
        collab_score = collaborative_scores.get(rec, 0.0)
        hybrid_scores[rec] = (content_weight * content_score + 
                             collaborative_weight * collab_score)
    
    # Sort by hybrid score
    sorted_recs = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    return [title for title, _ in sorted_recs[:10]]
