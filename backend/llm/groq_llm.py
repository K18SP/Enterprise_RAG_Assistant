from langchain_groq import ChatGroq

from .base_llm import BaseLLM
from .prompt_builder import PromptBuilder

from config.settings import settings
from config.constants import (
    LLM_MODEL,
    TEMPERATURE
)

class GroqLLM(BaseLLM):

# Here temperature is decoding parameter that controls the randomness of token selection
# Low temperature => model is more deterministic
# High temperature => Increases diversity and creativity
    def __init__(self):
        """
        Here we are creating LLM model for once 
        """
        self.llm = ChatGroq(api_key=settings.GROQ_API_KEY, model = LLM_MODEL, temperature = TEMPERATURE)

    def generate(self, query:str, context:str) -> str:

        prompt = PromptBuilder.build_prompt(query = query, context = context)

        response = self.llm.invoke(prompt)

        return response.content