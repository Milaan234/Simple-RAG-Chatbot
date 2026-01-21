from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "photosynthesis-rag-chatbot"
EMBEDDINGS_MODEL = "multilingual-e5-large"

# generate embedding for the given text
def generate_embedding(pc, query_text):
    return pc.inference.embed(
        model=EMBEDDINGS_MODEL,
        inputs=[query_text],
        parameters={"input_type": "query"}
    )

# get relevant text from DB based on query embedding
def get_relevant_text(index, query_embedding):
    return index.query(
        vector=query_embedding[0]['values'],
        top_k=3,
        include_metadata=True
    )

def search_db(query_text):
    # create pinecone object and index object
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)

    # generate embedding for query text and get relevant results
    query_embedding = generate_embedding(pc, query_text)

    results = get_relevant_text(index, query_embedding)

    # exit if no relevant results
    if not results['matches']:
        print('No relevant matches found.')
        return ""

    # return top result
    top_match = results['matches'][0]['metadata']['text']
    return top_match


def get_top_match_from_db(query_text=""):
    #query_text = "What gas is released into the atmosphere as a byproduct of photosynthesis?"
    if not query_text:
        print("No text received. Exiting.")
        return ""
    
    #print("Searching for relevant text in Pinecone DB!")
    top_match = search_db(query_text)
    #print("Finished searching for relevant text in Pinecone DB!")
    return top_match

if __name__ == "__main__":
    get_top_match_from_db()