from .groq_llm import GroqLLM

class LLMFactory:

    @staticmethod
    def get_llm(provider:str='groq', **kwargs):

        provider = provider.lower()

        if provider == 'groq':

            return GroqLLM() 

        raise ValueError(f'Unsupported LLM Provider: {provider}')