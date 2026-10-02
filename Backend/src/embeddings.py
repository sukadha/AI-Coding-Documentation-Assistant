from sentence_transformers import SentenceTransformer
import numpy as np


# ============================================================
# EMBEDDING MODEL
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

print("=" * 70)
print("LOADING EMBEDDING MODEL")
print("=" * 70)

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(texts):
    """
    Convert text chunks into numerical vectors.

    Works with chunks from:
        - Python
        - SQL
        - Machine Learning
        - Git
        - API
    """

    if not texts:
        return np.array([])

    # --------------------------------------------------------
    # Make sure every item is a string
    # --------------------------------------------------------

    cleaned_texts = []

    for text in texts:

        if text is None:
            continue

        text = str(text).strip()

        if text:
            cleaned_texts.append(text)

    if not cleaned_texts:
        return np.array([])

    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    embeddings = model.encode(
        cleaned_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings


# ============================================================
# CREATE EMBEDDING FOR ONE TEXT
# ============================================================

def create_embedding(text):
    """
    Create an embedding for a single text.
    """

    if not text:
        return None

    embedding = model.encode(
        [str(text)],
        convert_to_numpy=True
    )

    return embedding[0]


# ============================================================
# EMBEDDING DIMENSION
# ============================================================

def get_embedding_dimension():
    """
    Return the size of the embedding vector.
    """

    return model.get_sentence_embedding_dimension()


# ============================================================
# EMBED DOCUMENT CHUNKS
# ============================================================

def embed_chunks(chunks):
    """
    Create embeddings while preserving chunk metadata.

    Expected input:

    [
        {
            "text": "...",
            "source": "...",
            "category": "python",
            "filename": "python_basics.txt",
            "chunk_id": 0
        }
    ]

    Returns:

    [
        {
            "text": "...",
            "source": "...",
            "category": "python",
            "filename": "python_basics.txt",
            "chunk_id": 0,
            "embedding": [...]
        }
    ]
    """

    if not chunks:
        return []

    texts = []

    valid_chunks = []

    for chunk in chunks:

        if not isinstance(chunk, dict):
            continue

        text = chunk.get("text", "")

        if not text:
            continue

        texts.append(str(text))
        valid_chunks.append(chunk)

    if not texts:
        return []

    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    embeddings = create_embeddings(texts)

    # --------------------------------------------------------
    # Attach embeddings to metadata
    # --------------------------------------------------------

    embedded_chunks = []

    for chunk, embedding in zip(
        valid_chunks,
        embeddings
    ):

        new_chunk = chunk.copy()

        new_chunk["embedding"] = embedding.tolist()

        embedded_chunks.append(new_chunk)

    return embedded_chunks


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("EMBEDDINGS TEST")
    print("=" * 70)

    print(
        "\nEmbedding model:",
        MODEL_NAME
    )

    print(
        "Embedding dimension:",
        get_embedding_dimension()
    )

    # --------------------------------------------------------
    # Test chunks from all your knowledge-base categories
    # --------------------------------------------------------

    test_chunks = [

        {
            "text": "Python lists are mutable collections.",
            "source": "python_basics.txt",
            "category": "python",
            "filename": "python_basics.txt",
            "chunk_id": 0
        },

        {
            "text": "INNER JOIN returns matching rows from two tables.",
            "source": "sql_joins.txt",
            "category": "sql",
            "filename": "sql_joins.txt",
            "chunk_id": 0
        },

        {
            "text": "Linear regression predicts a continuous target variable.",
            "source": "regression.txt",
            "category": "machine_learning",
            "filename": "regression.txt",
            "chunk_id": 0
        },

        {
            "text": "Git branches allow developers to work on separate lines of development.",
            "source": "git_branching.txt",
            "category": "git",
            "filename": "git_branching.txt",
            "chunk_id": 0
        },

        {
            "text": "REST APIs use HTTP methods such as GET, POST, PUT and DELETE.",
            "source": "rest_api.txt",
            "category": "api",
            "filename": "rest_api.txt",
            "chunk_id": 0
        }
    ]

    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    print("\nCreating embeddings...")

    embedded_chunks = embed_chunks(
        test_chunks
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print(
        "\nNumber of embedded chunks:",
        len(embedded_chunks)
    )

    for chunk in embedded_chunks:

        print("\n" + "-" * 70)

        print(
            "Category:",
            chunk.get("category")
        )

        print(
            "File:",
            chunk.get("filename")
        )

        print(
            "Chunk ID:",
            chunk.get("chunk_id")
        )

        embedding = chunk.get(
            "embedding",
            []
        )

        print(
            "Embedding dimension:",
            len(embedding)
        )

        print(
            "First 5 values:",
            embedding[:5]
        )

    # --------------------------------------------------------
    # Single text test
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SINGLE TEXT EMBEDDING TEST")
    print("=" * 70)

    text = "Explain TypeError in Python."

    embedding = create_embedding(text)

    print("\nText:")
    print(text)

    print(
        "\nEmbedding dimension:",
        len(embedding)
    )

    print(
        "First 5 values:",
        embedding[:5]
    )

    print("\n" + "=" * 70)
    print("EMBEDDINGS TEST COMPLETE")
    print("=" * 70)