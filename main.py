"""
Setup:
- Add 'input.txt' file
- python -m venv .venv
- source .venv/bin/activate
- pip install pinecone google-genai langchain-text-splitters python-dotenv
"""

from add import add_text_to_DB
from search import get_top_match_from_db
from ai import get_ai_response

# runs the RAG chatbot
def chatbot():
    # gets user query
    query_text = str(input("\nUser: "))
    while query_text and query_text != "exit":
        # finds top match in DB
        top_match = get_top_match_from_db(query_text)

        # calls ai with query and top match
        ai_response = get_ai_response(query_text, top_match)
        print('\nAI:', ai_response)

        query_text = str(input("\nUser: "))


def main():
    print("Welcome to the RAG Chatbot!")
    user_choice = input("What would you like to do?\n 1. Add text to Pinecone DB\n 2. Open RAG Chatbot\nUser: ")
    while user_choice and user_choice != "exit":
        # if wanting to add text to DB
        if user_choice == "1":
            add_text_to_DB()
        elif user_choice == "2":
            chatbot()
        else:
            print('Invalid choice')

        user_choice = input("What would you like to do?\n 1. Add text to Pinecone DB\n 2. Open RAG Chatbot\nUser: ")


if __name__ == "__main__":
    main()
