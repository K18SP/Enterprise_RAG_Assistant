from .groq_llm import GroqLLM
from config.constants import LLM_PROVIDER

class LLMFactory:

    @staticmethod
    def get_llm(provider:str=LLM_PROVIDER):

        provider = provider.lower()

        if provider == 'groq':

            return GroqLLM() 

        raise ValueError(f'Unsupported LLM Provider: {provider}')