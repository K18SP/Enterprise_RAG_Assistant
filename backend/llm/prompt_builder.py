class PromptBuilder:

    @staticmethod
    def build_prompt(query:str,context:str)->str:

        prompt = f"""
You are an AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
respond with:

"I don't know based on the provided documents."

Context: 

{context}

Question: 

{query}

Answer:

"""
        return prompt