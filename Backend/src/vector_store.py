import os
import json

import faiss
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

VECTOR_DB_DIR = os.path.join(
    BASE_DIR,
    "..",
    "vector_db"
)

INDEX_PATH = os.path.join(
    VECTOR_DB_DIR,
    "knowledge_base.index"
)

DOCUMENTS_PATH = os.path.join(
    VECTOR_DB_DIR,
    "documents.json"
)


# ============================================================
# VECTOR STORE
# ============================================================

class VectorStore:

    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.documents = []


    # ========================================================
    # ADD DOCUMENTS
    # ========================================================

    def add(
        self,
        embeddings,
        documents
    ):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        if len(embeddings) == 0:
            return

        # Check dimension
        if embeddings.shape[1] != self.dimension:

            raise ValueError(
                f"Embedding dimension mismatch. "
                f"Expected {self.dimension}, "
                f"got {embeddings.shape[1]}"
            )

        self.index.add(
            embeddings
        )

        self.documents.extend(
            documents
        )


    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query_embedding,
        k=5
    ):

        if self.index.ntotal == 0:

            return []


        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )


        # Do not request more vectors
        # than are actually stored

        k = min(
            k,
            self.index.ntotal
        )


        distances, indices = self.index.search(
            query_embedding,
            k
        )


        results = []


        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue


            document = self.documents[index].copy()


            document["distance"] = float(
                distance
            )


            results.append(
                document
            )


        return results


    # ========================================================
    # SAVE VECTOR DATABASE
    # ========================================================

    def save(self):

        os.makedirs(
            VECTOR_DB_DIR,
            exist_ok=True
        )


        faiss.write_index(
            self.index,
            INDEX_PATH
        )


        with open(
            DOCUMENTS_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.documents,
                file,
                indent=4,
                ensure_ascii=False
            )


        print(
            f"Vector database saved to:"
            f"\n{VECTOR_DB_DIR}"
        )


    # ========================================================
    # LOAD VECTOR DATABASE
    # ========================================================

    @classmethod
    def load(cls):

        if not os.path.exists(
            INDEX_PATH
        ):

            raise FileNotFoundError(
                "FAISS index not found. "
                "Create the vector database first."
            )


        if not os.path.exists(
            DOCUMENTS_PATH
        ):

            raise FileNotFoundError(
                "documents.json not found."
            )


        index = faiss.read_index(
            INDEX_PATH
        )


        with open(
            DOCUMENTS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            documents = json.load(
                file
            )


        store = cls(
            index.d
        )


        store.index = index

        store.documents = documents


        return store


# ============================================================
# LOAD ALL TXT FILES
# ============================================================

def load_all_txt_files():

    documents = []


    print("\n" + "=" * 70)
    print("LOADING KNOWLEDGE BASE")
    print("=" * 70)


    if not os.path.exists(
        DATA_DIR
    ):

        raise FileNotFoundError(
            f"Data directory not found:\n{DATA_DIR}"
        )


    # --------------------------------------------------------
    # Walk through ALL folders
    # --------------------------------------------------------

    for root, dirs, files in os.walk(
        DATA_DIR
    ):

        for filename in files:

            if not filename.lower().endswith(
                ".txt"
            ):

                continue


            file_path = os.path.join(
                root,
                filename
            )


            # Category = folder name
            category = os.path.basename(
                root
            )


            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()


                if not text.strip():

                    print(
                        f"SKIPPED EMPTY: "
                        f"{filename}"
                    )

                    continue


                document = {

                    "text": text,

                    "source": file_path,

                    "filename": filename,

                    "category": category,

                    "document_type": category

                }


                documents.append(
                    document
                )


                print(
                    f"Loaded: "
                    f"{category}/{filename}"
                )


            except Exception as error:

                print(
                    f"ERROR loading "
                    f"{file_path}: {error}"
                )


    print("\n" + "-" * 70)

    print(
        f"Total TXT files loaded: "
        f"{len(documents)}"
    )

    print("-" * 70)


    return documents


# ============================================================
# TEST VECTOR STORE
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("FAISS VECTOR STORE TEST")
    print("=" * 70)


    # --------------------------------------------------------
    # Load ALL files
    # --------------------------------------------------------

    documents = load_all_txt_files()


    if not documents:

        print(
            "\nNo documents found."
        )

        exit()


    # --------------------------------------------------------
    # IMPORTANT
    # --------------------------------------------------------
    #
    # For testing FAISS without embeddings.py,
    # create random vectors.
    #
    # Later replace this section with:
    #
    # embeddings = create_embeddings(texts)
    #
    # --------------------------------------------------------

    dimension = 384


    np.random.seed(42)


    embeddings = np.random.rand(
        len(documents),
        dimension
    ).astype(
        "float32"
    )


    # --------------------------------------------------------
    # Create vector store
    # --------------------------------------------------------

    store = VectorStore(
        dimension=dimension
    )


    # --------------------------------------------------------
    # Add ALL documents
    # --------------------------------------------------------

    store.add(
        embeddings,
        documents
    )


    print("\n" + "=" * 70)

    print(
        f"Vectors stored: "
        f"{store.index.ntotal}"
    )

    print(
        f"Documents stored: "
        f"{len(store.documents)}"
    )

    print("=" * 70)


    # --------------------------------------------------------
    # Show every stored document
    # --------------------------------------------------------

    print("\nSTORED DOCUMENTS")
    print("-" * 70)


    for i, document in enumerate(
        store.documents,
        start=1
    ):

        print(
            f"{i}. "
            f"{document['category']}/"
            f"{document['filename']}"
        )


    # --------------------------------------------------------
    # Test search
    # --------------------------------------------------------

    query_embedding = np.random.rand(
        dimension
    ).astype(
        "float32"
    )


    results = store.search(
        query_embedding,
        k=5
    )


    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)


    for result in results:

        print(
            f"\nSource: "
            f"{result['filename']}"
        )

        print(
            f"Category: "
            f"{result['category']}"
        )

        print(
            f"Distance: "
            f"{result['distance']}"
        )

        print(
            f"Text: "
            f"{result['text'][:150]}"
        )


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    store.save()


    print("\n" + "=" * 70)
    print("FAISS VECTOR STORE TEST COMPLETE")
    print("=" * 70)