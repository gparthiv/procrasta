from .resources import vector_store, llm
from qdrant_client.models import Filter, FieldCondition, MatchValue


def process_query(
    query: str,
    user_id: str,
):

    # 1. Retrieval
    search_results = vector_store.similarity_search(
        query,
        k=3,
        filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=user_id),
                )
            ]
        ),
    )

    # 2. Context construction
    context_blocks = []

    for x in search_results:

        source = x.metadata.get(
            "source",
            "Unknown File",
        )

        if x.metadata.get("type") == "pptx":
            location = f"Slide {x.metadata.get('slide', '?')}"
        else:
            location = f"Page {x.metadata.get('page', '?')}"

        context_blocks.append(
            f"Source: {source}\n" f"Location: {location}\n" f"{x.page_content}"
        )

    context_str = "\n\n".join(context_blocks)

    # 3. Prompt construction
    prompt = f"""
You are an AI Study Companion.

Answer ONLY from the provided context.
Do not use outside knowledge or invent information.

If the answer is not present, say:
"I couldn't find this information in your uploaded notes."

Give a concise answer and cite the relevant source and page/slide.

Context:
{context_str}

Question:
{query}
"""

    # 4. Generation
    response = llm.invoke(prompt)

    answer = response.content

    if isinstance(answer, list):
        answer = "".join(
            block.get("text", "") for block in answer if isinstance(block, dict)
        )

    return {"answer": answer}
