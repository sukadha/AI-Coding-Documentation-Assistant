import os
import sys


# ============================================================
# ALLOW IMPORTS WHEN RUNNING:
#
# python src/retriever.py
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BACKEND_DIR = os.path.dirname(
    CURRENT_DIR
)

if BACKEND_DIR not in sys.path:
    sys.path.insert(
        0,
        BACKEND_DIR
    )


# ============================================================
# IMPORT EMBEDDING MODEL
# ============================================================

from embeddings import create_embedding


# ============================================================
# IMPORT VECTOR STORE
# ============================================================

from vector_store import VectorStore


# ============================================================
# RETRIEVER
# ============================================================

class Retriever:

    def __init__(
        self,
        top_k=5
    ):
        """
        Initialize the retriever.

        top_k:
            Number of relevant chunks to retrieve.
        """

        self.top_k = top_k

        # ----------------------------------------------------
        # Load existing FAISS vector database
        # ----------------------------------------------------

        self.vector_store = VectorStore.load()

        print(
            f"Retriever initialized."
        )

        print(
            f"Documents in vector store: "
            f"{len(self.vector_store.documents)}"
        )

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        question
    ):
        """
        Convert the question into an embedding
        and retrieve the most relevant documents.
        """

        if not question:
            return []

        question = question.strip()

        if not question:
            return []

        # ----------------------------------------------------
        # Create embedding for user question
        # ----------------------------------------------------

        query_embedding = create_embedding(
            question
        )

        # ----------------------------------------------------
        # Search FAISS
        # ----------------------------------------------------

        results = self.vector_store.search(
            query_embedding,
            k=self.top_k
        )

        return results


# ============================================================
# SIMPLE FUNCTION
# ============================================================

def retrieve_documents(
    question,
    top_k=5
):
    """
    Simple function that can be used
    directly by rag_pipeline.py.
    """

    retriever = Retriever(
        top_k=top_k
    )

    return retriever.retrieve(
        question
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RETRIEVER TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Create retriever
    # --------------------------------------------------------

    retriever = Retriever(
        top_k=5
    )

    # --------------------------------------------------------
    # Test questions
    # --------------------------------------------------------

    questions = [

        "How does INNER JOIN work?",

        "What is a TypeError in Python?",

        "What is supervised learning?",

        "How does REST API work?",

        "How do Git branches work?"

    ]

    # --------------------------------------------------------
    # Run searches
    # --------------------------------------------------------

    for question in questions:

        print("\n" + "=" * 70)

        print(
            f"QUESTION:\n{question}"
        )

        print("=" * 70)

        results = retriever.retrieve(
            question
        )

        if not results:

            print(
                "No relevant documents found."
            )

            continue

        print(
            f"\nRetrieved {len(results)} documents:"
        )

        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        for i, result in enumerate(
            results,
            start=1
        ):

            print(
                "\n" + "-" * 70
            )

            print(
                f"Result {i}"
            )

            print(
                f"Source: "
                f"{result.get('filename', 'Unknown')}"
            )

            print(
                f"Category: "
                f"{result.get('category', 'Unknown')}"
            )

            print(
                f"Distance: "
                f"{result.get('distance', 'Unknown')}"
            )

            print(
                "\nText:"
            )

            print(
                result.get(
                    "text",
                    ""
                )[:500]
            )

    print("\n" + "=" * 70)
    print("RETRIEVER TEST COMPLETE")
    print("=" * 70)