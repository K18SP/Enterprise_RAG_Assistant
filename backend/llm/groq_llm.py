from langchain_groq import ChatGroq

from .base_llm import BaseLLM
from .prompt_builder import PromptBuilder

class GroqLLM(BaseLLM):

# Here temperature is decoding parameter that controls the randomness of token selection
# Low temperature => model is more deterministic
# High temperature => Increases diversity and creativity
    def __init__(self, api_key:str, model:str = 'llama-3.3-70b-versatile',temperature: float=0.2):
        """
        Here we are creating LLM model for once 
        """
        self.llm = ChatGroq(api_key=api_key, model = model, temperature = temperature)

    def generate(self, query:str, context:str) -> str:

        prompt = PromptBuilder.build_prompt(query = query, context = context)

        response = self.llm.invoke(prompt)

        return response.content