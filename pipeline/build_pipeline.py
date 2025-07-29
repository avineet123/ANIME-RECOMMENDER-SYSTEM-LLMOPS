## This file Used to create vectore Store
from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting to Build Pipeline..")

        loader = AnimeDataLoader(
            original_csv="data/anime_with_synopsis.csv",
            processed_csv="data/anime_updated.csv",
        )

        processed_csv = loader.load_and_process()

        logger.info("Data Loaded And Processed .....")

        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()  # build and save vector store

        logger.info("Vector Store Build Successfully....")

        logger.info("Pipeline Built Successfully....")

    except Exception as e:
        logger.error(f"failed to execute pipeline {str(e)}")
        raise CustomException("Error During Pipeline", e)


if __name__ == "__main__":
    main()
