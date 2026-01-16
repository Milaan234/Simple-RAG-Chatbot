import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "photosynthesis-rag-chatbot"
EMBEDDINGS_MODEL = "multilingual-e5-large"

# converts original text into chunks
def getChunks(originalText):
    # uses  pre-defined splitter to split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    return splitter.split_text(originalText)


# create an index in pinecone. An index is like a database
def create_pinecone_index(pc):
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    # wait until index is ready
    while not pc.describe_index(INDEX_NAME).status['ready']:
        time.sleep(1)

# generate batch embeddings
def generate_embeddings(pc, batch):
    return pc.inference.embed(
        model=EMBEDDINGS_MODEL,
        inputs=batch,
        parameters={"input_type": "passage", "truncate": "END"}
    )

# generate vectors
def generate_vectors(vectors, embeddings, batch, start_index):
    # loop through each chunk in the batch
    for j in range(len(embeddings)):
        # for each chunk, create a vector id and vector
        vector_id = f"chunk_{start_index + j}"
        
        vectors.append({
            "id": vector_id,
            "values": embeddings[j]['values'],
            "metadata": {
                "text": batch[j]
            }
        })


def add_text_to_DB(filename='input.txt'):
    #print("Adding text to Pinecone DB!")
    try:
        # opens file to read to add to db
        with open(filename, 'r') as file:
            # chunk contents of file
            content = file.read()
            chunks = getChunks(content)
            
            # create pinecone object
            pc = Pinecone(api_key=PINECONE_API_KEY)

            # check if index already exists. If not, create index
            existing_indexes = [index.name for index in pc.list_indexes()]

            if INDEX_NAME not in existing_indexes:
                create_pinecone_index(pc)
            
            # create index object
            index = pc.Index(INDEX_NAME)

            # create embeddings and vectors in chunks
            batch_size = 90
            # upload vectors to pincone in batches
            for i in range(0, len(chunks), batch_size):
                # get batch of chunks
                batch = chunks[i : i + batch_size]

                # create embeddings for the batch
                embeddings = generate_embeddings(pc, batch)

                # create vectors for the batch
                vectors = []
                generate_vectors(vectors, embeddings, batch, i)
                
                # add vectors to db
                index.upsert(vectors=vectors)
            
            print('Process of saving to DB complete')
        
    except FileNotFoundError:
        print(f"Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")    
    #print('Finished adding text to Pinecone DB!')

if __name__ == "__main__":
    add_text_to_DB()
