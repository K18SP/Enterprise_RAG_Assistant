from langchain_groq import ChatGroq

from .base_llm import BaseLLM
from .prompt_builder import PromptBuilder

from config.settings import settings
from config.constants import (
    LLM_MODEL,
    TEMPERATURE
)

from utils.logger import setup_logger
from exceptions.llm_exception import LLMError

logger = setup_logger(__name__)

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

        logger.info(f"Generating LLM response using {LLM_MODEL}")

        prompt = PromptBuilder.build_prompt(query = query, context = context)


        try:

            response = self.llm.invoke(prompt)

            logger.info("LLM response generated successfully.")

            return response.content

        except Exception as e:

            logger.exception("Failed to generate response from the language model")
            raise LLMError("Failed to generate response from the language model") from e
