
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class VectorStoreBuilder:
    """
    A utility class to build and load a Chroma vector store
    from CSV documents using HuggingFace embeddings.
    """

    def __init__(self, csv_path: str, persist_dir: str = "chroma_db"):
        """
        Args:
            csv_path (str): Path to the CSV file containing documents.
            persist_dir (str): Directory where the Chroma DB will be stored.
        """
        self.csv_path = csv_path
        self.persist_dir = persist_dir

        # Initialize HuggingFace embedding model
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vectorstore(self):
        """
        Loads documents from CSV, splits them into chunks,
        embeds them, and saves them to a persistent Chroma DB.
        """
        # Load CSV documents
        loader = CSVLoader(file_path=self.csv_path, encoding="utf-8", metadata_columns=[])
        documents = loader.load()

        # Split text into manageable chunks
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=True)
        chunks = splitter.split_documents(documents)

        # Create and persist Chroma vector store
        vector_db = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.persist_dir)
        vector_db.persist()

    def load_vector_store(self):
        """
        Loads an existing Chroma vector store from disk.

        Returns:
            Chroma: The loaded vector store instance.
        """
        return Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding)

