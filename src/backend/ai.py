from google import genai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL_NAME = "gemini-3-flash-preview"

def call_ai(query='', relevant_text=''):
    if not query:
        return ''
    
    # make call to GEMINI API
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=AI_MODEL_NAME,
        config=genai.types.GenerateContentConfig(
            temperature=0.3,
            system_instruction = """
                You are a precise and helpful RAG assistant.
                
                Your Goal: Answer the user's question using ONLY the provided "Relevant Text".
                
                Rules:
                1. STRICTLY GROUNDED: Do not use your own outside knowledge. If the answer isn't in the text, do not invent it.
                2. PARTIAL ANSWERS: If the text answers *part* of the question but not all of it, answer the part you know and explicitly state: "The provided documents do not contain information about [missing part]."
                3. CITATIONS: When possible, mention the context (e.g., "According to the text...") to build trust.
                
                If the text is completely irrelevant to the question, simply state: "I cannot answer this based on the provided documents."
                Do not include markdown.
                """
        ),
        contents=f"Relevant text: {relevant_text}\n\nUser Question: {query}"
    )

    return response.text


def get_ai_response(query='', relevant_text=''):
    print("Calling GEMINI API!")
    return call_ai(query, relevant_text)
    print("Finished calling GEMINI API!")
    

if __name__ == "__main__":
    get_ai_response()