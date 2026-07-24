from langchain_core.documents import Document


class ContextBuilder:

    @staticmethod
    def build_context(
        documents: list[Document]
    ) -> str:

        if not documents:
            return ""

        parts = []

        for i, doc in enumerate(documents, start=1):

            parts.append(
                f"""Document {i}

Source: {doc.metadata.get("source","Unknown")}
Page: {doc.metadata.get("page","N/A")}

Content:
{doc.page_content}
"""
            )

        return "\n\n" + ("-" * 80 + "\n\n").join(parts)