from .groq_llm import GroqLLM

class LLMFactory:

    @staticmethod
    def get_llm(provider:str='groq', **kwargs):

        provider = provider.lower()

        if provider == 'groq':

            return GroqLLM(**kwargs) # Here **kwargs is use because it allows any number of arguments so it will be helpful in future if we want to change the LLM model

        raise ValueError(f'Unsupported LLM Provider: {provider}')