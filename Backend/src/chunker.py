# ============================================================
# CHUNKER
# ============================================================
#
# Splits cleaned documentation into smaller overlapping chunks.
#
# Supports:
#   - Python
#   - SQL
#   - Machine Learning
#   - Git
#   - REST API
#   - GraphQL
#
# Expected input from text_cleaner.py:
#
# [
#     {
#         "text": "...",
#         "source": "...",
#         "category": "...",
#         "filename": "...",
#         "document_type": "..."
#     }
# ]
#
# ============================================================


# ============================================================
# DEFAULT CHUNK SETTINGS
# ============================================================

DEFAULT_CHUNK_SIZE = 800
DEFAULT_OVERLAP = 100


# ============================================================
# CHUNK SINGLE TEXT
# ============================================================

def chunk_text(
    text,
    chunk_size=DEFAULT_CHUNK_SIZE,
    overlap=DEFAULT_OVERLAP
):
    """
    Split text into overlapping chunks.

    Example:

        text
        ↓
        Chunk 1
        Chunk 2
        Chunk 3
        ...

    Parameters:
        text       : cleaned document text
        chunk_size : maximum characters per chunk
        overlap    : overlapping characters between chunks

    Returns:
        list of text chunks
    """

    if not text:
        return []

    text = str(text).strip()

    if not text:
        return []

    # --------------------------------------------------------
    # Validate chunk size
    # --------------------------------------------------------

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    # --------------------------------------------------------
    # Validate overlap
    # --------------------------------------------------------

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size."
        )

    # --------------------------------------------------------
    # If document is smaller than chunk size
    # --------------------------------------------------------

    if len(text) <= chunk_size:
        return [text]

    chunks = []

    start = 0

    step = chunk_size - overlap

    # --------------------------------------------------------
    # Create overlapping chunks
    # --------------------------------------------------------

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


# ============================================================
# IMPROVE CHUNK BOUNDARIES
# ============================================================

def split_at_natural_boundary(
    text,
    chunk_size=DEFAULT_CHUNK_SIZE,
    overlap=DEFAULT_OVERLAP
):
    """
    Create chunks while trying to avoid cutting sentences
    or code/documentation sections unnecessarily.

    The basic chunking still uses character length, but tries
    to move the end of a chunk toward a newline or sentence
    boundary.
    """

    if not text:
        return []

    text = str(text).strip()

    if len(text) <= chunk_size:
        return [text]

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    chunks = []

    start = 0

    while start < len(text):

        target_end = start + chunk_size

        # Last chunk
        if target_end >= len(text):

            chunk = text[start:].strip()

            if chunk:
                chunks.append(chunk)

            break

        # ----------------------------------------------------
        # Look for a natural boundary
        # ----------------------------------------------------

        search_start = max(
            start,
            target_end - 150
        )

        boundary_candidates = [

            text.rfind("\n\n", search_start, target_end),

            text.rfind("\n", search_start, target_end),

            text.rfind(". ", search_start, target_end),

            text.rfind("; ", search_start, target_end)

        ]

        boundary = max(boundary_candidates)

        # ----------------------------------------------------
        # If no suitable boundary was found,
        # use the original chunk size.
        # ----------------------------------------------------

        if boundary <= start:

            end = target_end

        else:

            if text[boundary:boundary + 2] == "\n\n":

                end = boundary + 2

            elif text[boundary:boundary + 1] == "\n":

                end = boundary + 1

            else:

                end = boundary + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # ----------------------------------------------------
        # Calculate next starting point
        # ----------------------------------------------------

        next_start = end - overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


# ============================================================
# CHUNK DOCUMENTS
# ============================================================

def chunk_documents(
    documents,
    chunk_size=DEFAULT_CHUNK_SIZE,
    overlap=DEFAULT_OVERLAP
):
    """
    Chunk all cleaned documents.

    Metadata from each document is preserved.

    Input:

    [
        {
            "text": "...",
            "source": "...",
            "category": "python",
            "filename": "python_basics.txt"
        }
    ]

    Output:

    [
        {
            "text": "...chunk...",
            "source": "...",
            "category": "python",
            "filename": "python_basics.txt",
            "chunk_id": 0,
            "chunk_index": 0,
            "total_chunks": 5
        }
    ]
    """

    if not documents:
        return []

    chunked_documents = []

    # --------------------------------------------------------
    # Process every document
    # --------------------------------------------------------

    for document_index, document in enumerate(documents):

        if not isinstance(document, dict):
            continue

        text = document.get(
            "text",
            ""
        )

        if not text:
            continue

        # ----------------------------------------------------
        # Create chunks
        # ----------------------------------------------------

        chunks = split_at_natural_boundary(
            text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        total_chunks = len(chunks)

        # ----------------------------------------------------
        # Store every chunk
        # ----------------------------------------------------

        for chunk_index, chunk in enumerate(chunks):

            chunk_document = document.copy()

            # Replace original text with chunk
            chunk_document["text"] = chunk

            # ------------------------------------------------
            # Chunk metadata
            # ------------------------------------------------

            chunk_document["chunk_id"] = (
                f"{document_index}_{chunk_index}"
            )

            chunk_document["chunk_index"] = chunk_index

            chunk_document["total_chunks"] = total_chunks

            chunk_document["chunk_size"] = len(chunk)

            chunked_documents.append(
                chunk_document
            )

    return chunked_documents


# ============================================================
# CHUNK KNOWLEDGE BASE
# ============================================================

def chunk_knowledge_base(
    documents,
    chunk_size=DEFAULT_CHUNK_SIZE,
    overlap=DEFAULT_OVERLAP
):
    """
    Alias used by the RAG ingestion pipeline.
    """

    return chunk_documents(
        documents,
        chunk_size=chunk_size,
        overlap=overlap
    )


# ============================================================
# GROUP CHUNKS BY CATEGORY
# ============================================================

def get_chunk_statistics(chunks):
    """
    Display statistics for the chunked knowledge base.

    Categories supported by your project:

        python
        sql
        machine_learning
        git
        api
    """

    statistics = {}

    for chunk in chunks:

        category = chunk.get(
            "category",
            "unknown"
        )

        if category not in statistics:
            statistics[category] = 0

        statistics[category] += 1

    return statistics


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("CHUNKER TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Example documents based on your project
    # --------------------------------------------------------

    test_documents = [

        {
            "text": """
Python is a high-level programming language.
Python supports functions, classes, modules,
exceptions and object-oriented programming.

Python functions allow code to be reused.
Exceptions are handled using try and except blocks.

Example:

def calculate_sum(a, b):
    return a + b
            """,

            "source": "python/python_basics.txt",

            "category": "python",

            "filename": "python_basics.txt",

            "document_type": "python"
        },

        {
            "text": """
SQL is a language used to communicate with
relational databases.

INNER JOIN combines rows from two tables
when a matching condition exists.

Example:

SELECT employees.name, departments.name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;
            """,

            "source": "sql/sql_joins.txt",

            "category": "sql",

            "filename": "sql_joins.txt",

            "document_type": "sql"
        },

        {
            "text": """
Machine learning is a branch of artificial
intelligence that allows systems to learn
patterns from data.

Regression is a supervised learning technique
used to predict continuous numerical values.

Linear regression models the relationship
between input variables and a target variable.
            """,

            "source": "machine_learning/regression.txt",

            "category": "machine_learning",

            "filename": "regression.txt",

            "document_type": "machine_learning"
        },

        {
            "text": """
Git is a distributed version control system.

Git branches allow developers to work on
different features independently.

Common commands include:

git init
git clone
git add
git commit
git push
git pull
            """,

            "source": "git/git_commands.txt",

            "category": "git",

            "filename": "git_commands.txt",

            "document_type": "git"
        },

        {
            "text": """
REST APIs use HTTP methods such as GET,
POST, PUT and DELETE.

A REST API allows applications to communicate
through HTTP requests and responses.

Example:

GET /api/users
POST /api/users
            """,

            "source": "api/rest_api.txt",

            "category": "api",

            "filename": "rest_api.txt",

            "document_type": "api"
        }

    ]

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    chunks = chunk_documents(
        test_documents,
        chunk_size=300,
        overlap=50
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print(
        f"\nOriginal documents: "
        f"{len(test_documents)}"
    )

    print(
        f"Total chunks created: "
        f"{len(chunks)}"
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    statistics = get_chunk_statistics(
        chunks
    )

    print("\nChunks by category:")

    for category, count in statistics.items():

        print(
            f"  {category}: {count}"
        )

    # --------------------------------------------------------
    # Display chunks
    # --------------------------------------------------------

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"Chunk {index}"
        )

        print(
            "Category:",
            chunk.get("category")
        )

        print(
            "Filename:",
            chunk.get("filename")
        )

        print(
            "Source:",
            chunk.get("source")
        )

        print(
            "Chunk Index:",
            chunk.get("chunk_index")
        )

        print(
            "Total Chunks:",
            chunk.get("total_chunks")
        )

        print(
            "Chunk Size:",
            chunk.get("chunk_size")
        )

        print("\nText:")

        print(
            chunk.get("text")
        )

    print("\n" + "=" * 70)
    print("CHUNKER TEST COMPLETE")
    print("=" * 70)