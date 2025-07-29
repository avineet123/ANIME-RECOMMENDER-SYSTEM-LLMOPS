from langchain.chains import RetrievalQA  # make QA chain
from langchain_groq import ChatGroq  # Use to intialize GROQ LLM
from src.prompt_template import get_anime_prompt  # Fetch Prompt Template


class AnimeRecommender:
    def __init__(self, retriever: str, api_key: str, model_name: str):  # constructor
        self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0)
        self.prompt = get_anime_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt},
        )

    def get_recommendation(self, query: str):
        result = self.qa_chain({"query": query})
        return result["result"]
