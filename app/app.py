import streamlit as st
from dotenv import load_dotenv
from pipeline.pipeline import AnimeRecommendationPipeline

# Set Streamlit page configuration
st.set_page_config(page_title="Anime Recommender", layout="wide")

# Load environment variables (e.g., API keys)
load_dotenv()

@st.cache_resource
def init_pipeline():
    """
    Initialize the recommendation pipeline once.
    This prevents reloading on every user interaction, improving performance.
    """
    return AnimeRecommendationPipeline()

# Initialize the pipeline
pipeline = init_pipeline()

# App Title
st.title("Anime Recommender System")

# User input: query based on anime preferences
query = st.text_input("Enter your anime preferences (e.g., 'light-hearted anime with school settings')")

# On user submission
if query:
    with st.spinner("Fetching recommendations for you..."):
        try:
            response = pipeline.recommend(query)
            st.markdown("### Recommendations")
            st.write(response)
        except Exception as e:
            st.error(f"Failed to generate recommendations. Error: {str(e)}")
