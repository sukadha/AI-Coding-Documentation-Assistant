import os
import sys


# ============================================================
# IMPORT PATH
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
# IMPORT PROJECT MODULES
# ============================================================

from embeddings import create_embedding
from vector_store import VectorStore
from llm import generate_answer


# ============================================================
# RAG PIPELINE
# ============================================================

class RAGPipeline:

    def __init__(self, top_k=5):

        self.top_k = top_k

        print("\nInitializing RAG Pipeline...")

        # ----------------------------------------------------
        # Load FAISS vector database
        # ----------------------------------------------------

        self.vector_store = VectorStore.load()

        print(
            "Vector database loaded successfully."
        )

        print(
            f"Documents available: "
            f"{len(self.vector_store.documents)}"
        )


    # ========================================================
    # RUN RAG
    # ========================================================

    def run(self, question):

        print("\n" + "=" * 70)
        print("RAG PIPELINE")
        print("=" * 70)

        # ----------------------------------------------------
        # Validate question
        # ----------------------------------------------------

        if not question:

            return {
                "status": "error",
                "message": "Question cannot be empty.",
                "question": "",
                "answer": "",
                "sources": []
            }


        question = question.strip()


        if not question:

            return {
                "status": "error",
                "message": "Question cannot be empty.",
                "question": "",
                "answer": "",
                "sources": []
            }


        print("\nUser Question:")
        print(question)


        # ====================================================
        # STEP 1 — CREATE QUESTION EMBEDDING
        # ====================================================

        print(
            "\nCreating question embedding..."
        )

        try:

            query_embedding = create_embedding(
                question
            )

        except Exception as e:

            print(
                "\nEmbedding error:"
            )

            print(e)

            return {
                "status": "error",
                "message": "Failed to create question embedding.",
                "error": str(e),
                "question": question,
                "answer": "",
                "sources": []
            }


        print(
            "Question embedding created successfully."
        )


        # ====================================================
        # STEP 2 — SEARCH FAISS
        # ====================================================

        print(
            "\nSearching FAISS vector database..."
        )

        try:

            retrieved_documents = (
                self.vector_store.search(
                    query_embedding,
                    k=self.top_k
                )
            )

        except Exception as e:

            print(
                "\nFAISS search error:"
            )

            print(e)

            return {
                "status": "error",
                "message": "Vector database search failed.",
                "error": str(e),
                "question": question,
                "answer": "",
                "sources": []
            }


        # ====================================================
        # CHECK RETRIEVED DOCUMENTS
        # ====================================================

        if not retrieved_documents:

            print(
                "\nNo relevant documents found."
            )

            return {
                "status": "success",
                "message": "No relevant documentation found.",
                "question": question,
                "answer": (
                    "No relevant documentation was found "
                    "for this question."
                ),
                "sources": []
            }


        print(
            f"\nRetrieved "
            f"{len(retrieved_documents)} "
            f"relevant documents."
        )


        # ====================================================
        # DISPLAY RETRIEVED DOCUMENTS
        # ====================================================

        print(
            "\nRetrieved Sources:"
        )

        for i, document in enumerate(
            retrieved_documents,
            start=1
        ):

            print(
                "\n" + "-" * 60
            )

            print(
                f"Result {i}"
            )

            print(
                "Source:",
                document.get(
                    "source",
                    document.get(
                        "filename",
                        "Unknown"
                    )
                )
            )

            print(
                "Category:",
                document.get(
                    "category",
                    "Unknown"
                )
            )

            print(
                "Distance:",
                document.get(
                    "distance",
                    "Unknown"
                )
            )


        # ====================================================
        # STEP 3 — SEND CONTEXT TO GEMINI
        # ====================================================

        print(
            "\nSending retrieved context to "
            "Gemini 2.5 Flash..."
        )

        try:

            answer = generate_answer(
                question,
                retrieved_documents
            )

        except Exception as e:

            print(
                "\nGemini error:"
            )

            print(e)

            return {
                "status": "error",
                "message": "Gemini request failed.",
                "error": str(e),
                "question": question,
                "answer": "",
                "sources": retrieved_documents
            }


        # ====================================================
        # STEP 4 — BUILD SOURCE INFORMATION
        # ====================================================

        sources = []

        for document in retrieved_documents:

            source = {
                "source": document.get(
                    "source",
                    document.get(
                        "filename",
                        "Unknown"
                    )
                ),

                "filename": document.get(
                    "filename",
                    document.get(
                        "source",
                        "Unknown"
                    )
                ),

                "category": document.get(
                    "category",
                    "Unknown"
                ),

                "distance": document.get(
                    "distance",
                    None
                ),

                "text": document.get(
                    "text",
                    ""
                )
            }

            sources.append(
                source
            )


        # ====================================================
        # STEP 5 — FINAL RESULT
        # ====================================================

        result = {

            "status": "success",

            "message": (
                "RAG analysis completed successfully."
            ),

            "question": question,

            "answer": answer,

            "sources": sources
        }


        # ====================================================
        # DISPLAY ANSWER
        # ====================================================

        print("\n" + "=" * 70)
        print("GEMINI 2.5 FLASH ANSWER")
        print("=" * 70)

        print(answer)


        print("\n" + "=" * 70)
        print("RAG PIPELINE COMPLETE")
        print("=" * 70)


        return result


# ============================================================
# SIMPLE FUNCTION
# ============================================================

def run_rag_pipeline(question, top_k=5):

    pipeline = RAGPipeline(
        top_k=top_k
    )

    return pipeline.run(
        question
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("AI CODING DOCUMENTATION ASSISTANT")
    print("RAG PIPELINE TEST")
    print("=" * 70)


    question = input(
        "\nEnter your question: "
    ).strip()


    if not question:

        print(
            "\nQuestion cannot be empty."
        )

    else:

        result = run_rag_pipeline(
            question,
            top_k=5
        )


        print("\n" + "=" * 70)
        print("FINAL RESULT")
        print("=" * 70)


        print(
            "\nStatus:",
            result.get("status")
        )


        print(
            "\nQuestion:",
            result.get("question")
        )


        print(
            "\nAnswer:"
        )

        print(
            result.get("answer")
        )


        print(
            "\nSources:"
        )

        for source in result.get(
            "sources",
            []
        ):

            print(
                f"- "
                f"{source.get('filename')} "
                f"({source.get('category')})"
            )


        print(
            "\n" + "=" * 70
        )

        print(
            "RAG PIPELINE TEST COMPLETE"
        )

        print(
            "=" * 70
        )