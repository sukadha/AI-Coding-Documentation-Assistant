import re


# ============================================================
# TEXT CLEANER
# ============================================================

def clean_text(text):
    """
    Clean documentation text while preserving
    programming and technical syntax.

    Supports:
        - Python
        - SQL
        - Machine Learning
        - Git
        - REST API
        - GraphQL
    """

    if text is None:
        return ""

    text = str(text)

    # --------------------------------------------------------
    # Normalize line endings
    # --------------------------------------------------------

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # --------------------------------------------------------
    # Remove null characters
    # --------------------------------------------------------

    text = text.replace("\x00", "")

    # --------------------------------------------------------
    # Remove trailing spaces from every line
    # --------------------------------------------------------

    lines = []

    for line in text.split("\n"):
        lines.append(line.rstrip())

    text = "\n".join(lines)

    # --------------------------------------------------------
    # Replace tabs with 4 spaces
    # --------------------------------------------------------

    cleaned_lines = []

    for line in text.split("\n"):

        line = line.replace("\t", "    ")
        line = line.rstrip()

        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # --------------------------------------------------------
    # Remove excessive blank lines
    # --------------------------------------------------------

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # --------------------------------------------------------
    # Remove unnecessary spaces at document boundaries
    # --------------------------------------------------------

    text = text.strip()

    return text


# ============================================================
# CLEAN MULTIPLE DOCUMENTS
# ============================================================

def clean_documents(documents):
    """
    Clean all documents loaded by document_loader.py.

    Metadata is preserved.

    Expected input:

    [
        {
            "text": "...",
            "source": "...",
            "category": "...",
            "filename": "...",
            "document_type": "..."
        }
    ]
    """

    cleaned_documents = []

    if not documents:
        return cleaned_documents

    for document in documents:

        if not isinstance(document, dict):
            continue

        original_text = document.get(
            "text",
            ""
        )

        cleaned_text = clean_text(
            original_text
        )

        # Skip empty documents
        if not cleaned_text:
            continue

        # Preserve all metadata
        cleaned_document = document.copy()

        cleaned_document["text"] = cleaned_text

        cleaned_documents.append(
            cleaned_document
        )

    return cleaned_documents


# ============================================================
# CLEAN KNOWLEDGE BASE
# ============================================================

def clean_knowledge_base(documents):
    """
    Clean the complete knowledge base.

    This includes:

        data/python/
        data/sql/
        data/machine_learning/
        data/git/
        data/api/
    """

    return clean_documents(documents)


# ============================================================
# TEST DATA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TEXT CLEANER TEST")
    print("=" * 70)


    # ========================================================
    # 1. PYTHON
    # ========================================================

    python_text = """
    
    
def calculate_sum(a, b):


    result = a + b

    return result



print(calculate_sum(10, 20))


"""


    # ========================================================
    # 2. PYTHON EXCEPTIONS
    # ========================================================

    python_exception_text = """
    
    
try:

    number = int(input("Enter a number: "))

except ValueError:

    print("Invalid number")


"""


    # ========================================================
    # 3. SQL
    # ========================================================

    sql_text = """
    
    
SELECT *
FROM employees;


SELECT employees.name, departments.department_name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;


"""


    # ========================================================
    # 4. MACHINE LEARNING
    # ========================================================

    machine_learning_text = """
    
    
Machine Learning is a subset of Artificial Intelligence.

Supervised learning uses labelled data.

Regression is used to predict continuous values.

Classification is used to predict categories.

Common algorithms include:

Linear Regression
Logistic Regression
Decision Tree
Random Forest
Support Vector Machine
K-Nearest Neighbors


"""


    # ========================================================
    # 5. MACHINE LEARNING REGRESSION
    # ========================================================

    regression_text = """
    
    
Linear Regression is a supervised machine learning
algorithm used for predicting continuous numerical values.

The model attempts to find a relationship between
independent variables and a dependent variable.

Example:

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)


"""


    # ========================================================
    # 6. GIT
    # ========================================================

    git_text = """
    
    
Git is a distributed version control system.

Git allows developers to track changes in source code.

Common commands:

git init

git clone

git status

git add .

git commit -m "Initial commit"

git push

git pull


"""


    # ========================================================
    # 7. GIT BRANCHING
    # ========================================================

    git_branching_text = """
    
    
Git branches allow developers to work on
different features independently.

Create a branch:

git branch feature-login

Switch branch:

git checkout feature-login

Create and switch:

git checkout -b feature-login

Merge branch:

git merge feature-login


"""


    # ========================================================
    # 8. REST API
    # ========================================================

    rest_api_text = """
    
    
REST API allows applications to communicate
using HTTP requests.

Common HTTP methods:

GET
POST
PUT
DELETE

Example:

GET /api/users

POST /api/users


"""


    # ========================================================
    # 9. GRAPHQL
    # ========================================================

    graphql_text = """
    
    
GraphQL is a query language for APIs.

Clients can request exactly the data they need.

Example:

query {
    users {
        id
        name
        email
    }
}


"""


    # ========================================================
    # CREATE TEST DOCUMENTS
    # ========================================================

    test_documents = [

        # Python
        {
            "text": python_text,
            "source": "python/python_basics.txt",
            "category": "python",
            "filename": "python_basics.txt",
            "document_type": "python"
        },

        # Python Exceptions
        {
            "text": python_exception_text,
            "source": "python/python_exceptions.txt",
            "category": "python",
            "filename": "python_exceptions.txt",
            "document_type": "python"
        },

        # SQL
        {
            "text": sql_text,
            "source": "sql/sql_joins.txt",
            "category": "sql",
            "filename": "sql_joins.txt",
            "document_type": "sql"
        },

        # Machine Learning
        {
            "text": machine_learning_text,
            "source": "machine_learning/ml_basics.txt",
            "category": "machine_learning",
            "filename": "ml_basics.txt",
            "document_type": "machine_learning"
        },

        # Regression
        {
            "text": regression_text,
            "source": "machine_learning/regression.txt",
            "category": "machine_learning",
            "filename": "regression.txt",
            "document_type": "machine_learning"
        },

        # Git
        {
            "text": git_text,
            "source": "git/git_commands.txt",
            "category": "git",
            "filename": "git_commands.txt",
            "document_type": "git"
        },

        # Git Branching
        {
            "text": git_branching_text,
            "source": "git/git_branching.txt",
            "category": "git",
            "filename": "git_branching.txt",
            "document_type": "git"
        },

        # REST API
        {
            "text": rest_api_text,
            "source": "api/rest_api.txt",
            "category": "api",
            "filename": "rest_api.txt",
            "document_type": "api"
        },

        # GraphQL
        {
            "text": graphql_text,
            "source": "api/graphql.txt",
            "category": "api",
            "filename": "graphql.txt",
            "document_type": "api"
        }
    ]


    # ========================================================
    # CLEAN ALL DOCUMENTS
    # ========================================================

    cleaned_documents = clean_documents(
        test_documents
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print("\n" + "=" * 70)
    print("DOCUMENT CLEANING RESULT")
    print("=" * 70)

    print(
        f"\nOriginal documents: "
        f"{len(test_documents)}"
    )

    print(
        f"Cleaned documents: "
        f"{len(cleaned_documents)}"
    )


    # ========================================================
    # DISPLAY EACH DOCUMENT
    # ========================================================

    for document in cleaned_documents:

        print("\n" + "-" * 70)

        print(
            "Category:",
            document.get("category")
        )

        print(
            "Filename:",
            document.get("filename")
        )

        print(
            "Source:",
            document.get("source")
        )

        print(
            "\nCleaned text:"
        )

        print(
            document.get("text")
        )


    # ========================================================
    # CATEGORY SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("CATEGORY SUMMARY")
    print("=" * 70)

    category_counts = {}

    for document in cleaned_documents:

        category = document.get(
            "category",
            "unknown"
        )

        if category not in category_counts:
            category_counts[category] = 0

        category_counts[category] += 1


    for category, count in category_counts.items():

        print(
            f"{category}: {count} document(s)"
        )


    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n" + "=" * 70)
    print("TEXT CLEANER TEST COMPLETE")
    print("=" * 70)