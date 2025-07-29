from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)


class AnimeRecommendationPipeline:
    def __init__(self, persist_dir="chroma_db"):
        """
        Initializes the anime recommendation pipeline by loading
        the vector store and setting up the AnimeRecommender.
        """
        try:
            logger.info("Initializing Recommendation Pipeline")

            # Initialize vector retriever (pre-built from processed anime data)
            vector_builder = VectorStoreBuilder(csv_path="", persist_dir=persist_dir)
            retriever = vector_builder.load_vector_store().as_retriever()

            # Set up the recommender system using the retriever and LLM
            self.recommender = AnimeRecommender(retriever, GROQ_API_KEY, MODEL_NAME)

            logger.info("Pipeline Initialized Successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {str(e)}")
            raise CustomException("Error During Pipeline Initialization", e)

    def recommend(self, query: str):
        """
        Generates a recommendation based on the input query string.
        """
        try:
            logger.info(f"Received a Query: {query}")

            recommendation = self.recommender.get_recommendation(query)

            logger.info("Recommendation Generated Successfully")

            return recommendation
        except Exception as e:
            logger.error(f"Failed to get recommendation: {str(e)}")
            raise CustomException("Error During Getting Recommendation", e)
