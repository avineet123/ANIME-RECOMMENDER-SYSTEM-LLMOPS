# Logic for application
import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

st.set_page_config(page_title="Anime Recommender",layout="wide")

# during deployment , we run only app.py so it loads env 
load_dotenv()

@st.cache_resource
def init_pipeline():
    "when app start , it will initialize everything to save time, it will not run again again"
    return AnimeRecommendationPipeline()

pipeline= init_pipeline()

st.title("Anime Recommender System")

query=st.text_input("Enter your anime preferences eg: light hearted anime with school settings")

if query:
    with st.spinner("fetching recommendation for you ...."):
        response= pipeline.recommend(query)
        st.markdown("### Recommendations")
        st.write(response)












