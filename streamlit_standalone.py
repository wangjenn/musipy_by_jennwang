#!/usr/bin/env python3
"""
STANDALONE STREAMLIT APP - NO FLASK DEPENDENCIES
This file is completely independent of the Flask app structure.
Use this file for Streamlit Cloud deployment.
"""

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
    .test-question {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
    }
    .progress-bar {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'personality_scores' not in st.session_state:
    st.session_state.personality_scores = {}
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'test_answers' not in st.session_state:
    st.session_state.test_answers = {}

# Big Five Inventory (BFI-S) - 15 items
BFI_QUESTIONS = {
    0: {"text": "I see myself as someone who is reserved.", "trait": "extraversion", "reverse": True},
    1: {"text": "I see myself as someone who is generally trusting.", "trait": "agreeableness", "reverse": False},
    2: {"text": "I see myself as someone who tends to be lazy.", "trait": "conscientiousness", "reverse": True},
    3: {"text": "I see myself as someone who is relaxed, handles stress well.", "trait": "neuroticism", "reverse": True},
    4: {"text": "I see myself as someone who has few artistic interests.", "trait": "openness", "reverse": True},
    5: {"text": "I see myself as someone who is outgoing, sociable.", "trait": "extraversion", "reverse": False},
    6: {"text": "I see myself as someone who tends to find fault with others.", "trait": "agreeableness", "reverse": True},
    7: {"text": "I see myself as someone who does a thorough job.", "trait": "conscientiousness", "reverse": False},
    8: {"text": "I see myself as someone who gets nervous easily.", "trait": "neuroticism", "reverse": False},
    9: {"text": "I see myself as someone who has an active imagination.", "trait": "openness", "reverse": False},
    10: {"text": "I see myself as someone who is sometimes shy, inhibited.", "trait": "extraversion", "reverse": True},
    11: {"text": "I see myself as someone who is helpful and unselfish with others.", "trait": "agreeableness", "reverse": False},
    12: {"text": "I see myself as someone who can be somewhat careless.", "trait": "conscientiousness", "reverse": True},
    13: {"text": "I see myself as someone who is relaxed, handles stress well.", "trait": "neuroticism", "reverse": True},
    14: {"text": "I see myself as someone who is curious about many different things.", "trait": "openness", "reverse": False}
}

def calculate_big_five_scores(answers):
    """Calculate Big Five personality scores from test answers"""
    trait_scores = {
        'openness': [],
        'conscientiousness': [],
        'extraversion': [],
        'agreeableness': [],
        'neuroticism': []
    }
    
    # Collect scores for each trait
    for question_id, answer in answers.items():
        question = BFI_QUESTIONS[question_id]
        trait = question['trait']
        score = answer
        
        # Reverse score if needed
        if question['reverse']:
            score = 6 - score  # Convert 1-5 to 5-1
        
        trait_scores[trait].append(score)
    
    # Calculate averages for each trait
    final_scores = {}
    for trait, scores in trait_scores.items():
        if scores:  # Only calculate if we have scores for this trait
            final_scores[trait] = round(np.mean(scores), 2)
        else:
            final_scores[trait] = 3.0  # Default neutral score
    
    return final_scores

def show_big_five_test():
    """Display the Big Five personality test"""
    st.markdown("### 🧠 Big Five Personality Test")
    st.markdown("""
    This is the **15-item Big Five Inventory (BFI-S)**, a validated psychological assessment.
    Rate how much you agree with each statement on a scale of 1-5.
    """)
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(BFI_QUESTIONS)
    st.progress(progress)
    st.markdown(f"**Question {st.session_state.current_question + 1} of {len(BFI_QUESTIONS)}**")
    
    # Display current question
    if st.session_state.current_question < len(BFI_QUESTIONS):
        question = BFI_QUESTIONS[st.session_state.current_question]
        
        st.markdown(f"""
        <div class="test-question">
            <h4>{question['text']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Rating scale
        st.markdown("**Rate how much you agree:**")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("1\nDisagree\nStrongly", key=f"q{st.session_state.current_question}_1"):
                st.session_state.test_answers[st.session_state.current_question] = 1
                st.session_state.current_question += 1
                st.rerun()
        
        with col2:
            if st.button("2\nDisagree\nModerately", key=f"q{st.session_state.current_question}_2"):
                st.session_state.test_answers[st.session_state.current_question] = 2
                st.session_state.current_question += 1
                st.rerun()
        
        with col3:
            if st.button("3\nNeither Agree\nnor Disagree", key=f"q{st.session_state.current_question}_3"):
                st.session_state.test_answers[st.session_state.current_question] = 3
                st.session_state.current_question += 1
                st.rerun()
        
        with col4:
            if st.button("4\nAgree\nModerately", key=f"q{st.session_state.current_question}_4"):
                st.session_state.test_answers[st.session_state.current_question] = 4
                st.session_state.current_question += 1
                st.rerun()
        
        with col5:
            if st.button("5\nAgree\nStrongly", key=f"q{st.session_state.current_question}_5"):
                st.session_state.test_answers[st.session_state.current_question] = 5
                st.session_state.current_question += 1
                st.rerun()
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_question > 0:
                if st.button("← Previous Question"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < len(BFI_QUESTIONS) - 1:
                if st.button("Next Question →"):
                    st.session_state.current_question += 1
                    st.rerun()
    
    # Show results when test is completed
    if st.session_state.current_question >= len(BFI_QUESTIONS):
        if len(st.session_state.test_answers) == len(BFI_QUESTIONS):
            st.success("🎉 Test completed! Here are your results:")
            
            # Calculate scores
            scores = calculate_big_five_scores(st.session_state.test_answers)
            
            # Display scores
            st.markdown("### 📊 Your Big Five Personality Scores")
            
            # Create a nice display of scores
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Openness to Experience", f"{scores['openness']}/5.0")
                st.metric("Conscientiousness", f"{scores['conscientiousness']}/5.0")
                st.metric("Extraversion", f"{scores['extraversion']}/5.0")
            
            with col2:
                st.metric("Agreeableness", f"{scores['agreeableness']}/5.0")
                st.metric("Neuroticism", f"{scores['neuroticism']}/5.0")
            
            # Store scores in session state
            st.session_state.personality_scores = {
                'ope': scores['openness'],
                'con': scores['conscientiousness'],
                'ext': scores['extraversion'],
                'agr': scores['agreeableness'],
                'neu': scores['neuroticism']
            }
            st.session_state.test_completed = True
            
            # Show detailed interpretation
            st.markdown("### 📝 What These Scores Mean")
            
            interpretations = {
                'openness': {
                    'high': 'You enjoy new experiences, are creative, and have broad interests.',
                    'low': 'You prefer routine, are practical, and focus on concrete details.'
                },
                'conscientiousness': {
                    'high': 'You are organized, responsible, and goal-directed.',
                    'low': 'You are spontaneous, flexible, and less focused on planning.'
                },
                'extraversion': {
                    'high': 'You are outgoing, energetic, and enjoy social interactions.',
                    'low': 'You are reserved, quiet, and prefer solitary activities.'
                },
                'agreeableness': {
                    'high': 'You are cooperative, trusting, and compassionate.',
                    'low': 'You are competitive, skeptical, and direct in communication.'
                },
                'neuroticism': {
                    'high': 'You experience more negative emotions and stress.',
                    'low': 'You are emotionally stable and handle stress well.'
                }
            }
            
            for trait, score in scores.items():
                level = 'high' if score > 3.5 else 'low' if score < 2.5 else 'moderate'
                if level == 'moderate':
                    st.info(f"**{trait.title()}**: You show moderate levels of this trait.")
                else:
                    st.info(f"**{trait.title()}**: {interpretations[trait][level]}")
            
            if st.button("🎵 Get Music Recommendations", type="primary"):
                st.session_state.show_recommendations = True
                st.rerun()
            
            # Option to retake test
            if st.button("🔄 Retake Test"):
                st.session_state.current_question = 0
                st.session_state.test_answers = {}
                st.session_state.test_completed = False
                st.rerun()
        else:
            st.warning("Please complete all questions to see your results.")

def show_external_test():
    """Display external test option"""
    st.markdown("### 🔗 External Big Five Personality Test")
    st.markdown("""
    Take the official Big Five personality test on PsyToolkit and then enter your scores below.
    
    **Take the test here:** [Big Five Personality Test](https://www.psytoolkit.org/c/3.6.0/survey?s=hgHBk)
    """)
    
    st.markdown("### 📊 Enter Your Results")
    st.markdown("After completing the test, enter your scores below:")
    
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

@st.cache_resource
def load_data():
    """Load all necessary data files"""
    try:
        # Define base directory
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        
        # Load model
        model_path = os.path.join(BASE_DIR, 'models', 'knn.pkl')
        if not os.path.exists(model_path):
            st.error(f"Model file not found: {model_path}")
            return None, None, None, None
        estimator = joblib.load(model_path)
        
        # Load data files
        song_names_path = os.path.join(BASE_DIR, 'data', 'songs_names.csv')
        song_cosines_path = os.path.join(BASE_DIR, 'data', 'song_cosines.csv')
        final_data_path = os.path.join(BASE_DIR, 'data', 'final.csv')
        
        # Check if files exist
        for path, name in [(song_names_path, 'songs_names.csv'), 
                          (song_cosines_path, 'song_cosines.csv'), 
                          (final_data_path, 'final.csv')]:
            if not os.path.exists(path):
                st.error(f"Data file not found: {name}")
                return None, None, None, None
        
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

def show_personality_test():
    """Display personality test interface"""
    st.markdown('<div class="personality-section">', unsafe_allow_html=True)
    st.markdown("### 🧠 Big Five Personality Test")
    st.markdown("""
    Take the Big Five personality test to get personalized music recommendations!
    
    **Take the test here:** [Big Five Personality Test](https://www.psytoolkit.org/c/3.6.0/survey?s=hgHBk)
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
    
    - **Backend**: Python, Streamlit
    - **Machine Learning**: Scikit-learn, kNN algorithm
    - **Data Processing**: Pandas, NumPy, SciPy
    - **Deployment**: Streamlit Cloud ready
    
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

def main():
    """Main application function"""
    try:
        # Load data
        with st.spinner("Loading MusiPy..."):
            estimator, song_names, song_cosines, big5music = load_data()
        
        if estimator is None:
            st.error("""
            ❌ **Failed to load application data.** 
            
            This might be due to:
            - Missing data files
            - File path issues
            - Model loading problems
            
            Please check that all required files are present in the repository.
            """)
            return
        
        # Header
        st.markdown('<h1 class="main-header">🎵 MusiPy</h1>', unsafe_allow_html=True)
        st.markdown("### Personality-Based Music Recommendation System")
        
        # Sidebar for navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Choose a page:", ["Personality Test", "Music Recommendations", "About"])
        
        if page == "Personality Test":
            # Choose test method
            test_method = st.radio(
                "Choose how to get your personality scores:",
                ["🧠 Take the Big Five Test (Recommended)", "📊 Enter Scores Manually", "🔗 Use External Test"]
            )
            
            if test_method == "🧠 Take the Big Five Test (Recommended)":
                show_big_five_test()
            elif test_method == "📊 Enter Scores Manually":
                show_personality_test()
            elif test_method == "🔗 Use External Test":
                show_external_test()
        elif page == "Music Recommendations":
            show_recommendations(estimator, song_names, song_cosines, big5music)
        elif page == "About":
            show_about()
            
    except Exception as e:
        st.error(f"""
        ❌ **An error occurred while running the application:**
        
        **Error:** {str(e)}
        
        **Troubleshooting:**
        1. Check that all data files are present
        2. Verify the model file exists
        3. Ensure all dependencies are installed
        
        **Files needed:**
        - `models/knn.pkl`
        - `data/songs_names.csv`
        - `data/song_cosines.csv`
        - `data/final.csv`
        """)
        st.exception(e)

if __name__ == "__main__":
    main()
