from langchain.chains import RetrievalQA  # For QA chain using a retriever and LLM
from langchain_groq import ChatGroq       # GROQ LLM integration
from src.prompt_template import get_anime_prompt  # Custom anime prompt template


class AnimeRecommender:
    """
    Uses a GROQ LLM and RetrievalQA to generate anime recommendations
    based on vector store retriever and a prompt template.
    """
    def __init__(self, retriever, api_key: str, model_name: str):
        self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0)
        self.prompt = get_anime_prompt()

        # Initialize Retrieval QA chain with LLM, prompt, and retriever
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt},
        )

    def get_recommendation(self, query: str) -> str:
        """
        Takes a user query and returns an anime recommendation.
        """
        result = self.qa_chain({"query": query})
        return result["result"]
