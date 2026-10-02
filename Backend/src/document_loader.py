import os
from pathlib import Path
from pypdf import PdfReader


# ============================================================
# KNOWLEDGE BASE CONFIGURATION
# ============================================================

# Backend/src/document_loader.py
#                    ↑
# We go one level up to Backend/
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

DATA_DIR = BACKEND_DIR / "data"


# ============================================================
# SUPPORTED FILE TYPES
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".md"
}


# ============================================================
# LOAD TXT / MARKDOWN FILE
# ============================================================

def load_text_file(file_path):
    """
    Load a TXT or Markdown file.

    Returns:
        [
            {
                "text": "...",
                "source": "...",
                "page": 1
            }
        ]
    """

    documents = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            text = file.read()

        if text and text.strip():

            documents.append(
                {
                    "text": text,
                    "source": str(file_path),
                    "page": 1
                }
            )

    except Exception as e:

        print(
            f"Error loading text file {file_path}: {e}"
        )

    return documents


# ============================================================
# LOAD PDF FILE
# ============================================================

def load_pdf(file_path):
    """
    Extract text from every page of a PDF.
    """

    documents = []

    try:

        reader = PdfReader(file_path)

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text()

            if text and text.strip():

                documents.append(
                    {
                        "text": text,
                        "source": str(file_path),
                        "page": page_number
                    }
                )

    except Exception as e:

        print(
            f"Error loading PDF {file_path}: {e}"
        )

    return documents


# ============================================================
# GET CATEGORY FROM FOLDER
# ============================================================

def get_category(file_path):
    """
    Determine the knowledge category from the
    first folder inside Backend/data/.

    Example:

    data/python/python_basics.txt
        -> python

    data/sql/sql_joins.txt
        -> sql

    data/api/graphql.txt
        -> api
    """

    file_path = Path(file_path)

    try:

        relative_path = file_path.relative_to(
            DATA_DIR
        )

        # Example:
        # python/python_basics.txt
        #
        # parts:
        # ("python", "python_basics.txt")

        if len(relative_path.parts) >= 2:

            return relative_path.parts[0]

    except ValueError:

        pass

    return "unknown"


# ============================================================
# LOAD SINGLE FILE
# ============================================================

def load_file(file_path):
    """
    Load a single supported file.
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension in [".txt", ".md"]:

        return load_text_file(file_path)

    elif extension == ".pdf":

        return load_pdf(file_path)

    else:

        return []


# ============================================================
# LOAD ENTIRE KNOWLEDGE BASE
# ============================================================

def load_knowledge_base(
    data_directory=DATA_DIR
):
    """
    Automatically load every supported file from:

    Backend/data/

        api/
        git/
        machine_learning/
        python/
        sql/

    No files need to be manually specified.
    """

    data_directory = Path(
        data_directory
    )

    if not data_directory.exists():

        raise FileNotFoundError(
            f"Data directory does not exist: "
            f"{data_directory}"
        )

    all_documents = []

    print("\n" + "=" * 70)
    print("LOADING KNOWLEDGE BASE")
    print("=" * 70)

    print(
        f"\nData directory:\n{data_directory}"
    )

    # --------------------------------------------------------
    # Recursively scan every folder and file
    # --------------------------------------------------------

    for file_path in sorted(
        data_directory.rglob("*")
    ):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        # Ignore unsupported files
        if extension not in SUPPORTED_EXTENSIONS:
            continue

        # ----------------------------------------------------
        # Determine category
        # ----------------------------------------------------

        category = get_category(
            file_path
        )

        print(
            f"\nLoading [{category}]"
        )

        print(
            f"File: {file_path.name}"
        )

        # ----------------------------------------------------
        # Load file
        # ----------------------------------------------------

        documents = load_file(
            file_path
        )

        # ----------------------------------------------------
        # Add metadata
        # ----------------------------------------------------

        for document in documents:

            document["category"] = category

            document["filename"] = (
                file_path.name
            )

            document["extension"] = (
                extension
            )

            # Useful for your RAG retriever
            document["document_type"] = (
                category
            )

        all_documents.extend(
            documents
        )

        print(
            f"Loaded sections: "
            f"{len(documents)}"
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("KNOWLEDGE BASE LOADING COMPLETE")
    print("=" * 70)

    print(
        f"\nTotal document sections: "
        f"{len(all_documents)}"
    )

    return all_documents


# ============================================================
# KNOWLEDGE BASE SUMMARY
# ============================================================

def print_summary(documents):
    """
    Print a summary of loaded documents.
    """

    print("\n" + "=" * 70)
    print("KNOWLEDGE BASE SUMMARY")
    print("=" * 70)

    categories = {}

    files = set()

    for document in documents:

        category = document.get(
            "category",
            "unknown"
        )

        filename = document.get(
            "filename",
            "unknown"
        )

        categories[category] = (
            categories.get(category, 0) + 1
        )

        files.add(filename)

    print("\nCategories:")

    for category, count in sorted(
        categories.items()
    ):

        print(
            f"  {category}: "
            f"{count} document section(s)"
        )

    print(
        f"\nUnique files loaded: "
        f"{len(files)}"
    )

    print(
        f"Total sections/pages: "
        f"{len(documents)}"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("DOCUMENT LOADER TEST")
    print("=" * 70)

    try:

        documents = load_knowledge_base()

        print_summary(
            documents
        )

        # ----------------------------------------------------
        # Show loaded files
        # ----------------------------------------------------

        print("\n" + "=" * 70)
        print("LOADED FILES")
        print("=" * 70)

        loaded_files = set()

        for document in documents:

            loaded_files.add(
                (
                    document.get(
                        "category",
                        "unknown"
                    ),
                    document.get(
                        "filename",
                        "unknown"
                    )
                )
            )

        for category, filename in sorted(
            loaded_files
        ):

            print(
                f"[{category}] {filename}"
            )

        # ----------------------------------------------------
        # Show first document preview
        # ----------------------------------------------------

        if documents:

            first_document = documents[0]

            print("\n" + "=" * 70)
            print("FIRST DOCUMENT PREVIEW")
            print("=" * 70)

            print(
                "\nCategory:",
                first_document.get(
                    "category"
                )
            )

            print(
                "Filename:",
                first_document.get(
                    "filename"
                )
            )

            print(
                "Page:",
                first_document.get(
                    "page"
                )
            )

            print(
                "\nText:"
            )

            print(
                first_document["text"][:1000]
            )

        else:

            print(
                "\nNo documents were loaded."
            )

    except Exception as e:

        print(
            f"\nDOCUMENT LOADER ERROR:\n{e}"
        )

    print("\n" + "=" * 70)
    print("DOCUMENT LOADER TEST COMPLETE")
    print("=" * 70)