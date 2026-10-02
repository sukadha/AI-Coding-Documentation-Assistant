import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    retrieved_documents
):
    """
    Generate an answer using Gemini 2.5 Flash.

    The answer is based only on the documentation
    retrieved by the RAG retriever.
    """

    # --------------------------------------------------------
    # Check retrieved documents
    # --------------------------------------------------------

    if not retrieved_documents:

        return (
            "No relevant documentation was retrieved "
            "for this question."
        )


    # --------------------------------------------------------
    # Build retrieved context
    # --------------------------------------------------------

    context_parts = []

    for i, document in enumerate(
        retrieved_documents,
        start=1
    ):

        text = document.get(
            "text",
            ""
        )

        source = document.get(
            "source",
            document.get(
                "filename",
                "Unknown"
            )
        )

        category = document.get(
            "category",
            "Unknown"
        )

        distance = document.get(
            "distance",
            "Unknown"
        )

        context_parts.append(
            f"""
--- DOCUMENT {i} ---

Source: {source}

Category: {category}

Distance: {distance}

Content:
{text}
"""
        )


    context = "\n".join(
        context_parts
    )


    # ========================================================
    # RAG PROMPT
    # ========================================================

    prompt = f"""
You are an AI Coding Documentation Assistant.

Your job is to answer the user's question using ONLY
the retrieved documentation provided below.

The documentation may contain information about:

- Python
- SQL
- Machine Learning
- Git
- REST API
- GraphQL
- Programming concepts
- Coding errors
- Technical concepts


============================================================
IMPORTANT RULES
============================================================

1. Use the retrieved documentation as the primary source.

2. Do NOT invent information that is not supported by
   the retrieved documentation.

3. If the answer is not available in the retrieved
   documentation, clearly say:

   "The requested information was not found in the
   available documentation."

4. If the user asks about a coding error, explain:
   - What the error means
   - Why it happens
   - Which part of the code is causing it, if the code
     is present in the retrieved documentation
   - How to fix it
   - Corrected code when possible

5. Preserve programming syntax.

6. When providing corrected code, make it clear that
   it is based on the retrieved documentation and the
   user's question.

7. Do not claim that a file contains something unless
   that information appears in the retrieved context.

8. Mention the source filename when useful.

9. Keep the explanation beginner-friendly but technically
   correct.

10. If the question is asking for an example, provide
    an example only when the retrieved documentation
    supports the concept.


============================================================
RETRIEVED DOCUMENTATION
============================================================

{context}


============================================================
USER QUESTION
============================================================

{question}


============================================================
ANSWER FORMAT
============================================================

Give a clear answer.

If the question is about an error, use:

1. Error
2. Why it happens
3. Problem in the code
4. Corrected code
5. Explanation
6. Source

If the question is a general technical question,
use a suitable structure with:

- Explanation
- Example
- Important points
- Source


============================================================
FINAL INSTRUCTION
============================================================

Answer the user's question using the retrieved
documentation only.
"""


    # ========================================================
    # SEND REQUEST TO GEMINI
    # ========================================================

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return response.text


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("GEMINI 2.5 FLASH LLM TEST")
    print("=" * 70)


    # --------------------------------------------------------
    # Sample retrieved documentation
    # --------------------------------------------------------

    test_documents = [

        {
            "text": """
Python Exceptions

Common exceptions include:
TypeError, ValueError, NameError,
KeyError, IndexError and FileNotFoundError.

TypeError occurs when an operation or function
is applied to an object of an inappropriate type.

Example:

age = "20"
result = age + 5
            """,

            "source": "python_exceptions.txt",

            "filename": "python_exceptions.txt",

            "category": "python",

            "distance": 12.5
        },

        {
            "text": """
Python uses try/except to handle exceptions.

Example:

try:
    number = int(input("Enter a number: "))

except ValueError:
    print("Invalid number")
            """,

            "source": "python_exceptions.txt",

            "filename": "python_exceptions.txt",

            "category": "python",

            "distance": 15.2
        }

    ]


    # --------------------------------------------------------
    # Test question
    # --------------------------------------------------------

    question = """
Why am I getting a TypeError in Python?
Give me the correct code.
"""


    print("\nQUESTION:")
    print(question)


    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    print("\nSending request to Gemini 2.5 Flash...\n")


    try:

        answer = generate_answer(
            question,
            test_documents
        )

        print("=" * 70)
        print("GEMINI RESPONSE")
        print("=" * 70)

        print(answer)


    except Exception as e:

        print("=" * 70)
        print("GEMINI ERROR")
        print("=" * 70)

        print(e)


    print("\n" + "=" * 70)
    print("LLM TEST COMPLETE")
    print("=" * 70)