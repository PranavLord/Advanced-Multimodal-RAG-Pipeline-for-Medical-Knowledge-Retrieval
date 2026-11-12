from pinecone import Pinecone

from config.settings import settings


class PineconeManager:

    def __init__(self):

        pc = Pinecone(
            api_key=settings.PINECONE_API_KEY
        )

        self.index = pc.Index(
            settings.PINECONE_INDEX_NAME
        )

    # --------------------------------------------------
    # Upsert Vectors
    # --------------------------------------------------

    def upsert(
        self,
        vectors
    ):

        self.index.upsert(
            vectors=vectors
        )

    # --------------------------------------------------
    # Describe Index
    # --------------------------------------------------

    def describe(self):

        return self.index.describe_index_stats()

    # --------------------------------------------------
    # Search Vectors
    # --------------------------------------------------

    def search(
        self,
        query_embedding,
        top_k=5,
        session_id=None
    ):
        """
        Search Pinecone for the most relevant vectors.

        If a session_id is provided, retrieval is restricted
        to vectors belonging to that upload session.
        """

        query_kwargs = {

            "vector": query_embedding,

            "top_k": top_k,

            "include_metadata": True

        }

        if session_id is not None:

            query_kwargs["filter"] = {

                "session_id": {

                    "$eq": session_id

                }

            }

        results = self.index.query(
            **query_kwargs
        )

        return results

    # --------------------------------------------------
    # Delete Session Vectors
    # --------------------------------------------------

    def delete_by_session(
        self,
        session_id: str
    ):
        """
        Delete every vector belonging to a session.
        """

        self.index.delete(

            filter={

                "session_id": {

                    "$eq": session_id

                }

            }

        )

        return {

            "success": True,

            "session_id": session_id

        }