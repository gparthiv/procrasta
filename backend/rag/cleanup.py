from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

from rag.resources import qdrant_client, COLLECTION_NAME


def delete_user_data(user_id: str):

    result = qdrant_client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(
                        value=user_id
                    ),
                )
            ]
        ),
        wait=True,
    )

    return {
        "status": "deleted",
        "user_id": user_id,
    }