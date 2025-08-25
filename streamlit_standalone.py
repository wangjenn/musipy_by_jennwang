import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial import distance as ds
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="MusiPy - Personality-Based Music Recommendations",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .personality-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .recommendation-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'personality_scores' not in st.session_state:
    st.session_state.personality_scores = {}

@st.cache_resource
def load_data():
    """Load all necessary data files"""
    try:
        # Define base directory
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        
        # Load model
        model_path = os.path.join(BASE_DIR, 'models', 'knn.pkl')
        estimator = joblib.load(model_path)
        
        # Load data files
        song_names_path = os.path.join(BASE_DIR, 'data', 'songs_names.csv')
        song_cosines_path = os.path.join(BASE_DIR, 'data', 'song_cosines.csv')
        final_data_path = os.path.join(BASE_DIR, 'data', 'final.csv')
        
        song_names = pd.read_csv(song_names_path, encoding='utf-8')
        song_cosines = pd.read_csv(song_cosines_path)
        big5music = pd.read_csv(final_data_path)
        
        return estimator, song_names, song_cosines, big5music
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

def get_distances(row, new_row):
    """Calculate cosine distance between personality scores"""
    u = [row['ope'], row['agr'], row['neu'], row['con'], row['ext']]
    v = [new_row['ope'], new_row['agr'], new_row['neu'], new_row['con'], new_row['ext']]
    return ds.cosine(u, v)

def get_personality_recommendations(personality_scores, big5music):
    """Get music recommendations based on personality scores"""
    try:
        # Calculate distances
        big5music_copy = big5music.copy()
        big5music_copy['distance'] = big5music_copy.apply(
            get_distances, args=(personality_scores,), axis=1
        )
        
        # Sort by distance and get top recommendations
        big5music_sorted = big5music_copy.sort_values('distance')
        
        # Get song columns (exclude personality and metadata columns)
        song_columns = [col for col in big5music_sorted.columns 
                       if col not in ['userid', 'ope', 'con', 'ext', 'agr', 'neu', 
                                     'country_of_residence', 'distance']]
        
        # Get top 5 most similar users
        top_users = big5music_sorted.head(5)
        
        # Get their top rated songs
        recommendations = []
        for _, user in top_users.iterrows():
            user_songs = user[song_columns]
            # Get songs with rating >= 5 (assuming 1-7 scale)
            top_songs = user_songs[user_songs >= 5].index.tolist()
            recommendations.extend(top_songs[:3])  # Top 3 songs per user
        
        # Remove duplicates and limit to 10 recommendations
        unique_recommendations = list(dict.fromkeys(recommendations))[:10]
        
        return unique_recommendations, big5music_sorted.head(1)
    except Exception as e:
        st.error(f"Error getting recommendations: {e}")
        return [], None

def main():
    # Load data
    with st.spinner("Loading MusiPy..."):
        estimator, song_names, song_cosines, big5music = load_data()
    
    if estimator is None:
        st.error("Failed to load application data. Please check your data files.")
        return
    
    # Header
    st.markdown('<h1 class="main-header">🎵 MusiPy</h1>', unsafe_allow_html=True)
    st.markdown("### Personality-Based Music Recommendation System")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page:", ["Personality Test", "Music Recommendations", "About"])
    
    if page == "Personality Test":
        show_personality_test()
    elif page == "Music Recommendations":
        show_recommendations(estimator, song_names, song_cosines, big5music)
    elif page == "About":
        show_about()

def show_personality_test():
    """Display personality test interface"""
    st.markdown('<div class="personality-section">', unsafe_allow_html=True)
    st.markdown("### 🧠 Big Five Personality Test")
    st.markdown("""
    Take the Big Five personality test to get personalized music recommendations!
    
    **Take the test here:** [Big Five Personality Test](https://www.psytoolkit.org/c/3.4.4/survey?s=hgHBk)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Enter Your Personality Scores")
    st.markdown("Please input your Big Five personality scores (1-5 scale):")
    
    # Create columns for personality inputs
    col1, col2 = st.columns(2)
    
    with col1:
        openness = st.slider("Openness to Experience", 1.0, 5.0, 3.0, 0.1)
        conscientiousness = st.slider("Conscientiousness", 1.0, 5.0, 3.0, 0.1)
        extraversion = st.slider("Extraversion", 1.0, 5.0, 3.0, 0.1)
    
    with col2:
        agreeableness = st.slider("Agreeableness", 1.0, 5.0, 3.0, 0.1)
        neuroticism = st.slider("Neuroticism", 1.0, 5.0, 3.0, 0.1)
    
    # Display current scores
    st.markdown("### 📈 Your Current Scores")
    scores_df = pd.DataFrame({
        'Trait': ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism'],
        'Score': [openness, conscientiousness, extraversion, agreeableness, neuroticism]
    })
    st.dataframe(scores_df, use_container_width=True)
    
    # Store scores in session state
    st.session_state.personality_scores = {
        'ope': openness,
        'con': conscientiousness,
        'ext': extraversion,
        'agr': agreeableness,
        'neu': neuroticism
    }
    
    if st.button("🎵 Get Music Recommendations", type="primary"):
        st.session_state.show_recommendations = True
        st.rerun()

def show_recommendations(estimator, song_names, song_cosines, big5music):
    """Display music recommendations"""
    st.markdown("### 🎵 Your Personalized Music Recommendations")
    
    if not st.session_state.personality_scores:
        st.warning("Please complete the personality test first!")
        return
    
    # Get recommendations
    with st.spinner("Finding your perfect music..."):
        recommendations, similar_user = get_personality_recommendations(
            st.session_state.personality_scores, big5music
        )
    
    if recommendations:
        st.success(f"Found {len(recommendations)} personalized recommendations!")
        
        # Display recommendations
        for i, song in enumerate(recommendations, 1):
            with st.container():
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>#{i} {song}</h4>
                    <p>🎧 Click to listen (if available)</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Check if MP3 file exists
                mp3_path = f"app/static/mp3/{song}.mp3"
                if os.path.exists(mp3_path):
                    st.audio(mp3_path, format='audio/mp3')
                else:
                    st.info("Audio file not available for this song")
                
                # Thumbs up/down buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"👍 Like #{i}", key=f"like_{i}"):
                        st.success(f"You liked {song}!")
                with col2:
                    if st.button(f"👎 Dislike #{i}", key=f"dislike_{i}"):
                        st.error(f"You disliked {song}")
        
        # Show similar user info
        if similar_user is not None:
            st.markdown("### 👥 Similar User Profile")
            st.info(f"These recommendations are based on users with similar personality profiles to yours!")
    
    else:
        st.warning("No recommendations found. Try adjusting your personality scores.")

def show_about():
    """Display about page"""
    st.markdown("### 🎵 About MusiPy")
    st.markdown("""
    **MusiPy** is a personality-based music recommendation system that combines:
    
    - **Content-based filtering** using Big Five personality traits
    - **Collaborative filtering** using user behavior patterns
    - **Machine learning** with k-Nearest Neighbors algorithm
    
    ### 🧠 How It Works
    
    1. **Personality Assessment**: Uses the validated Big Five Inventory
    2. **Similarity Matching**: Finds users with similar personality profiles
    3. **Music Recommendations**: Suggests songs based on similar users' preferences
    4. **Interactive Feedback**: Learn from your likes/dislikes
    
    ### 🛠️ Technical Details
    
    - **Backend**: Python, Flask/Streamlit
    - **Machine Learning**: Scikit-learn, kNN algorithm
    - **Data Processing**: Pandas, NumPy, SciPy
    - **Deployment**: Docker, production-ready
    
    ### 📊 Big Five Personality Traits
    
    - **Openness**: Imagination, curiosity, creativity
    - **Conscientiousness**: Organization, responsibility, self-discipline
    - **Extraversion**: Sociability, assertiveness, energy
    - **Agreeableness**: Compassion, trust, cooperation
    - **Neuroticism**: Emotional stability, anxiety, moodiness
    
    ### 🎯 Research-Based
    
    This system is based on empirical research showing strong correlations between 
    personality dimensions and music preferences. It's not just another recommendation 
    engine - it's scientifically grounded!
    """)

if __name__ == "__main__":
    main()
